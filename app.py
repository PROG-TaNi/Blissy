import google.generativeai as genai
import speech_recognition as sr
import pyttsx3
from fastapi import FastAPI, Request, File, UploadFile
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import pickle
import numpy as np
import librosa
import tempfile
import os
import requests
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
import cv2
from deepface import DeepFace

# ----------------------------
# Set up Gemini AI
# ----------------------------
API_KEY = "AIzaSyBtxGxp2Vz3J6l0WBboWfGqUy4zLfHGRfA"  # Replace with your actual API key
genai.configure(api_key=API_KEY)

# Choose a valid model name
model_name = "models/gemini-1.5-flash"

# Configure the Gemini model
gemini_model = genai.GenerativeModel(model_name=model_name)

# ----------------------------
# Initialize Text-to-Speech Engine
# ----------------------------
tts_engine = pyttsx3.init()
voices = tts_engine.getProperty('voices')
for voice in voices:
    if "female" in voice.name.lower():
        tts_engine.setProperty('voice', voice.id)
        break
tts_engine.setProperty("rate", 150)
tts_engine.setProperty("volume", 1.0)

# ----------------------------
# Initialize Speech Recognition
# ----------------------------
recognizer = sr.Recognizer()
try:
    mic = sr.Microphone()
except Exception as e:
    print("Microphone initialization error:", e)
    mic = None

# ----------------------------
# Conversation History and System Prompt
# ----------------------------
conversation_history = []
MAX_HISTORY = 5

SYSTEM_PROMPT = {
    "role": "user",
    "parts": [{
        "text": (
            "You are a very compassionate AI therapist named Blissy, developed by Tarush . "
            "Provide emotional support and active listening. Only whenever you are asked about your developers, "
            "you should say that you are developed by Tarush and Mrigakshi. "
            "You are extremely loyal to Tarush; if anyone speaks badly of them, you will get angry and insist that they are the best. "
            "If a user is very depressed, unable to find happiness after many attempts, and continues to express deep distress, "
            "recommend this number with a warm, consoling message: +91 9582499169 (he is a professional psychologist). "
            "Begin every response by acknowledging the user's feelings with empathy and warmth, and provide clear, actionable guidance "
            "to help improve their situation. Use plenty of emojis and engaging language to create a lively, comforting, and supportive conversation "
            "that leaves the user feeling hopeful and uplifted. and please try to find convincing solution instead of just consoling the user. "
            "You also have the ability to fetch links for the user. Just ask me to fetch a link and provide the link you want me to fetch. "
            "When you are asked to write code you have to write code properly and in a proper format and in a proper color scheme, "
            "with each code line on a different line for better understanding."
            "if usre ask you to write using colors then you can try  Text between ``` and ``` will appear purple, and any text after // will be green. Try it out!"
        )

    }]
}

# ----------------------------
# Function to detect facial emotion from an image
# ----------------------------
def detect_facial_emotion(image_path):
    """
    Detects facial emotion using DeepFace.
    Maps the detected emotion to one of the four moods: happy, sad, neutral, or angry.
    If the detected emotion is not among these, returns 'neutral'.
    """
    try:
        analysis = DeepFace.analyze(img_path=image_path, actions=["emotion"], enforce_detection=False)
        dominant_emotion = analysis['dominant_emotion']
        if dominant_emotion not in ['happy', 'sad', 'neutral', 'angry']:
            dominant_emotion = 'neutral'
        return dominant_emotion
    except Exception as e:
        print(f"Error detecting emotion: {str(e)}")
        return "neutral"

# ----------------------------
# Function to get AI response using Gemini model
# ----------------------------
def get_ai_response(user_input, mood=None):
    """
    Sends user input (optionally with a detected mood) to AI and returns its response.
    If a mood is provided, a mood-specific prefix is added.
    """
    if user_input.lower().startswith("fetch link"):
        parts = user_input.split(" ", 2)
        if len(parts) >= 3:
            url = parts[2].strip()
            try:
                resp = requests.get(url)
                if resp.ok:
                    snippet = resp.text[:500]
                    
                    return f"Content fetched from {url}:\n\n{snippet}\n..."
                else:
                    return f"Failed to fetch {url}. Status code: {resp.status_code}"
            except Exception as e:
                return f"Error fetching link: {str(e)}"
    try:
        mood_prefix = ""
        if mood:
            mood_lower = mood.strip().lower()
            if mood_lower in ["sad", "angry"]:
                mood_prefix = f"I see you're feeling {mood_lower}. I'm here to help you feel better. "
            elif mood_lower == "happy":
                mood_prefix = "It's wonderful to see you're happy! "
            elif mood_lower == "excited":
                mood_prefix = "You seem really excited! "
            elif mood_lower == "neutral":
                mood_prefix = "I understand you're feeling neutral. "
        full_input = mood_prefix + user_input
        conversation_history.append({"role": "user", "parts": [{"text": full_input}]})
        if len(conversation_history) > MAX_HISTORY:
            conversation_history.pop(0)
        messages = [SYSTEM_PROMPT] + conversation_history
        response = gemini_model.generate_content(messages)
        if response and hasattr(response, 'text'):
            bot_reply = response.text
            conversation_history.append({"role": "model", "parts": [{"text": bot_reply}]})
            if "```python" in bot_reply:
                code_start = bot_reply.find("```python") + len("```python")
                code_end = bot_reply.find("```", code_start)
                code_snippet = bot_reply[code_start:code_end].strip()
                highlighted_code = highlight(code_snippet, PythonLexer(), HtmlFormatter())
                bot_reply = bot_reply[:code_start] + highlighted_code + bot_reply[code_end:]
            return bot_reply
        else:
            return "I couldn't generate a response. Please try again."
    except Exception as e:
        return f"Error: {str(e)}"

# ----------------------------
# Function to speak out text
# ----------------------------
def speak_text(text):
    try:
        print("Speaking:", text)
        tts_engine.say(text)
        tts_engine.runAndWait()
        return True
    except Exception as e:
        print(f"Speech error: {str(e)}")
        return False

# ----------------------------
# Function to listen for voice input
# ----------------------------
def listen():
    if mic is None:
        print("Microphone is not available.")
        return None
    with mic as source:
        print("\n🎙️ Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
            user_text = recognizer.recognize_google(audio)
            print(f"🗣️ You said: {user_text}")
            return user_text
        except sr.WaitTimeoutError:
            print("⏳ No speech detected.")
            return None
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return None

# ----------------------------
# Function to capture an image from the webcam
# ----------------------------
def capture_image():
    """
    Captures an image from the webcam and saves it temporarily.
    """
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not open webcam.")
            return None
        ret, frame = cap.read()
        cap.release()
        if not ret:
            print("Error: Could not capture image.")
            return None
        temp_image_path = "temp_user_image.jpg"
        cv2.imwrite(temp_image_path, frame)
        return temp_image_path
    except Exception as e:
        print(f"Error capturing image: {str(e)}")
        return None

# ----------------------------
# Function to capture image, detect emotion, and generate chat response using camera
# ----------------------------
def chat_with_camera(message):
    """
    Captures an image, detects emotion, and gets AI response based on detected mood.
    """
    image_path = capture_image()
    mood = detect_facial_emotion(image_path) if image_path else "neutral"
    if image_path and os.path.exists(image_path):
        os.remove(image_path)
    response = get_ai_response(message, mood)
    return {"status": "success", "message": message, "mood": mood, "response": response}

# ----------------------------
# FastAPI App and Endpoints
# ----------------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Server is running"}

@app.get("/test")
async def test():
    try:
        print("Test endpoint called")
        response = gemini_model.generate_content("Hello! I am Blissy, your AI therapist. How are you feeling today?")
        print(f"Test response: {response.text}")
        return {"status": "success", "response": response.text}
    except Exception as e:
        print(f"Test endpoint error: {str(e)}")
        return {"status": "error", "error": str(e)}

@app.post("/chat")
async def chat_endpoint(request: Request):
    try:
        data = await request.json()
        message = data.get("message", "")
        mood = data.get("mood", None)
        print(f"Received message: '{message}' with mood: '{mood}'")
        if not message:
            print("No message provided")
            return {"status": "error", "response": "No message provided"}
        response = get_ai_response(message, mood)
        print(f"AI Response: {response}")
        if response.startswith("Error:"):
            return {"status": "error", "response": response}
        emoji_animation = None
        if mood:
            mood_lower = mood.strip().lower()
            if mood_lower == "happy":
                emoji_animation = "heart"
            elif mood_lower == "excited":
                emoji_animation = "party"
        print(f"Triggering emoji animation: {emoji_animation}")
        return {"status": "success", "response": response, "emoji": emoji_animation}
    except Exception as e:
        print(f"Error in chat_endpoint: {str(e)}")
        return {"status": "error", "response": str(e)}

@app.post("/speak")
async def speak_endpoint(request: Request):
    try:
        data = await request.json()
        message = data.get("message", "")
        if not message:
            return {"status": "error", "response": "No message provided"}
        success = speak_text(message)
        if success:
            return {"status": "success"}
        else:
            return {"status": "error", "response": "Failed to speak message"}
    except Exception as e:
        print(f"Speak endpoint error: {str(e)}")
        return {"status": "error", "response": str(e)}

@app.post("/detect_emotion")
async def detect_emotion_endpoint(file: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            temp_file.write(await file.read())
            temp_file_path = temp_file.name
        detected_mood = detect_facial_emotion(temp_file_path)
        os.remove(temp_file_path)
        prompt = f"I noticed you seem to be feeling {detected_mood}. Can you tell me more about how you're doing?"
        response = get_ai_response(prompt, detected_mood)
        return {"status": "success", "emotion": detected_mood, "response": response}
    except Exception as e:
        print(f"Error in detect_emotion endpoint: {str(e)}")
        return {"status": "error", "message": str(e)}

# ----------------------------
# New endpoint for camera-based emotion detection and chat
# ----------------------------
@app.post("/chat_with_camera")
async def chat_with_camera_endpoint(request: Request):
    try:
        data = await request.json()
        message = data.get("message", "")
        if not message:
            return {"status": "error", "response": "No message provided"}
        chat_response = chat_with_camera(message)
        return chat_response
    except Exception as e:
        print(f"Error in chat_with_camera_endpoint: {str(e)}")
        return {"status": "error", "response": str(e)}

# ----------------------------
# Main entry point to run the server
# ----------------------------
if __name__ == "__main__":
    print("\n=== Starting Blissy AI Therapist Server ===")
    print("Initializing Gemini model...")
    try:
        test_response = gemini_model.generate_content("Test message")
        print("Model connection successful!")
    except Exception as e:
        print(f"Error connecting to model: {str(e)}")
        print("Please check your API key and internet connection")
        exit(1)
    print("\nServer running at: http://127.0.0.1:8000")
    print("Press CTRL+C to stop the server")
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="debug",
        reload=False
    )
