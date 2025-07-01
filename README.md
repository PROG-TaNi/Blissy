# 🌟 Blissy: AI-Powered Emotional Support Web App

**Blissy** is a modern, AI-driven web application that offers emotional support through interactive, voice-enabled, and visually immersive experiences. It combines cutting-edge technologies like **Google Gemini AI**, **facial emotion recognition**, **speech interaction**, and **3D graphics** to create a supportive, engaging space for users to share and heal.

---

## 🚀 Features at a Glance

- 🤖 **AI Therapist** powered by Google Gemini
- 🎙️ Voice interaction with speech-to-text and text-to-speech
- 😊 Real-time facial emotion detection (Happy, Sad, Neutral, Angry)
- 🌈 Animated 3D chat interface using Three.js and Particles.js
- 💬 Custom mood-aware and empathetic AI responses
- ✨ Matrix rain animation with full customization
- 📷 Image and audio upload (for emotion context, planned Vision AI)
- 🎉 Emoji rain and mood dots as feedback
- 🧠 Memory-aware short conversation flow
- 🧩 Modular, highly interactive web components

---

## 🧩 Project Structure

```

Blissy/
├── backend/
│ ├── app.py # FastAPI backend (Gemini, Voice, Emotion)
│ ├── facialemotion.py # Real-time facial emotion detection
├── frontend/
│ ├── landing page.html # Parallax animated intro
│ ├── about us.html # Interactive developer info with matrix bg
│ ├── animate.html # Main chat interface
│ ├── extra cards.html # 3D animated background (Three.js)
│ └── assets/ # JS, CSS, Fonts, Images
├── README.md
└── requirements.txt

```


---

## 💻 Frontend Overview

### 🎯 Landing Page (`landing page.html`)
- Parallax animation and large typography
- "Open Blissy" CTA
- GSAP & Lenis smooth scrolling
- Footer with developer credits

![image](https://github.com/user-attachments/assets/6bc2a407-b46b-4179-9e6a-6ab57f1fe593)


### 👨‍💻 About Us (`about us.html`)
- Matrix-style animated background
- Developer card (pixel shimmer + SVG)
- Reveal dev info (name, roll no., branch)
- Toolbar to customize matrix effects

### 🗨️ Chat Interface (`animate.html`)
- 3D animated background (iframe: `extra cards.html`)
- Sidebar + chat messages + syntax highlighting
- Voice input, emoji feedback, and visual cues
- Mood-based prefixes to AI replies

### 🌌 Extra Cards (`extra cards.html`)
- 3D scene with orbit controls, particles, dynamic rings
- Mouse/keyboard interaction with shaders
- Responsive high-performance Three.js rendering

---

## 🧠 Backend Overview

### `app.py` (FastAPI)
| Endpoint              | Description                                      |
|-----------------------|--------------------------------------------------|
| `/`                  | Health check                                     |
| `/test`              | Tests Gemini connection                          |
| `/chat`              | Main AI chat logic with mood context             |
| `/speak`             | Text-to-speech (female voice using `pyttsx3`)    |
| `/detect_emotion`    | Detect emotion from uploaded image               |
| `/chat_with_camera`  | Webcam image → Mood detection → Gemini response  |

- AI: Google Gemini (`gemini-1.5-flash`)
- Voice: `speech_recognition` + `pyttsx3`
- Emotion: `DeepFace`, `OpenCV`
- Real-time support: WebSocket (planned)
- Image/audio analysis with Google Vision (planned)

---

## 💡 AI Logic & Innovations

- **Prompt Engineering**: Custom instructions for empathy, loyalty to developers, code handling, and mental health safety
- **Mood-Aware Responses**: Adds emotion prefix before AI replies
- **Crisis Handling**: Professional helpline number + warm message
- **Short-Term Memory**: Maintains conversation context
- **Code Support**: Uses `Prism.js` for code block formatting

---

## 📦 Tech Stack

### Frontend
- `HTML5`, `CSS3` (custom props, animations)
- `JavaScript (ES6+)`
- `Three.js`, `GSAP`, `Lenis`
- `Particles.js`, `Prism.js`
- `Google Fonts`, `Web Components`

### Backend
- `Python 3`, `FastAPI`, `Uvicorn`
- `google.generativeai (Gemini)`
- `DeepFace`, `OpenCV`
- `SpeechRecognition`, `pyttsx3`
- `CORS`, `Librosa`, `Requests`, `Pygments`, `Numpy`

---

## 🎯 User Flow

1. **User visits** the landing page with parallax visuals.
2. **Clicks "Open Blissy"** → enters immersive chat interface.
3. **Interacts** via:
   - 💬 Text
   - 🎙️ Voice
   - 📷 Webcam (for emotion)
   - 🖼️ Image Upload (planned)
4. **Receives mood-sensitive AI replies** + soothing UI feedback
5. **Navigates** to About Us to view developer info in matrix style.

---

## ✨ Unique Visual & Emotional Touchpoints

- **Emoji Rain** & **Mood Dots** based on user's facial expression
- **Matrix Rain Customization** – ASCII, emoji, binary, Bamum, and more
- **Immersive 3D environment** for calming interaction
- **Friendly female voice** replies with emotional support
- **Animated transitions** and backgrounds that reflect the user’s mood

---

## 📈 Planned Improvements

- [ ] Add more developer/team cards
- [ ] Add authentication and data privacy controls
- [ ] Expand image analysis (Google Vision)
- [ ] Modularize CSS/JS files
- [ ] Improve accessibility (ARIA, keyboard nav)
- [ ] Integrate WebSocket for live emotion feedback
- [ ] Add README & contributor guidelines (you're reading it!)

---

## 🧑‍💻 Developer

**Tarush Nigam**  
📍 Electronics Engineering, VJTI  
💬 Passionate about AI, emotion tech, and human-computer empathy

---

## 📄 License

MIT License – See `LICENSE` file for details.

---

## 🛠️ Setup Instructions

### 🔧 Prerequisites
- Python 3.10+
- Node.js (optional for development tools)
- Webcam + Mic enabled browser

### 🧪 Backend (FastAPI)

```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --reload
```
🌐 Frontend
Just open landing page.html or deploy using any static server.

❤️ Acknowledgements
Google Gemini AI

DeepFace Emotion Recognition

OpenCV

Three.js + GSAP + Prism.js

Everyone passionate about AI for good 

Blissy isn't just a project — it's a vision for emotionally aware digital empathy.
