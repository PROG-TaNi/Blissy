import cv2
from deepface import DeepFace

# Start video capture
cap = cv2.VideoCapture(0)  # 0 for default webcam

# Define the emotions we want to detect
valid_emotions = ["happy", "sad", "neutral", "angry"]

while True:
    ret, frame = cap.read()
    if not ret:
        break

    try:
        # Analyze the face for emotions
        result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)

        # Get the detected emotion
        detected_emotion = result[0]['dominant_emotion']

        # Check if the detected emotion is in the valid emotions list
        if detected_emotion in valid_emotions:
            emotion_display = detected_emotion.capitalize()
        else:
            emotion_display = "Neutral"  # Default to Neutral if not in our list

        # Display the detected emotion on the frame
        cv2.putText(frame, f"Emotion: {emotion_display}", (50, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    except Exception as e:
        print(f"Error: {e}")

    # Show the video output
    cv2.imshow("Facial Emotion Detection", frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
