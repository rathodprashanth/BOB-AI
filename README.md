<div align="center">

<img src="https://readme-typing-svg.herokuapp.com?font=Orbitron&size=30&pause=1000&color=00D4FF&center=true&vCenter=true&width=600&lines=BOB-AI+%E2%80%94+Virtual+Assistant;Jarvis-Class+Desktop+Agent;Voice+Activated+%7C+AI+Powered" alt="Typing SVG" />

<br/>

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Gemini AI](https://img.shields.io/badge/Gemini_AI-Powered-4285F4?style=for-the-badge&logo=google&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-00D4FF?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-00FFAA?style=for-the-badge)
![Version](https://img.shields.io/badge/Version-1.0_Trial-FF6B35?style=for-the-badge)
![College](https://img.shields.io/badge/College_Review-2-blueviolet?style=for-the-badge)

<br/>

> **BOB-AI** is a Jarvis-class AI-powered virtual assistant that activates via voice,
> automates WhatsApp, controls your PC, opens apps, browses the web, and answers
> anything — all hands-free.

<br/>

[![GitHub](https://img.shields.io/badge/GitHub-venkatsaiganesh23--byte-181717?style=for-the-badge&logo=github)](https://github.com/venkatsaiganesh23-byte)

</div>

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🎤 **Voice Activation** | Say *"Hey Bob"* to wake BOB up anytime |
| 🤖 **Gemini AI Brain** | Answers any question using Google Gemini 1.5 Flash |
| 💬 **WhatsApp Automation** | Sends WhatsApp messages hands-free via voice |
| 📂 **App Control** | Opens Chrome, VS Code, Notepad, Spotify & more |
| ⌨️ **Auto Typing** | Types text in any active window on command |
| 🖥️ **System Control** | Volume, screenshot, lock, minimize, close apps |
| 🌐 **Web Search** | Searches Google & plays YouTube by voice |
| 🖼️ **Sci-Fi HUD** | Always-on-top status window with real-time log |

---

## 📁 Project Structure

```
BOB-AI-Assistant/
├── main.py                  ← Entry point — run this!
├── requirements.txt         ← All Python dependencies
├── README.md
└── modules/
    ├── assistant.py         ← Core brain (voice + Gemini AI + routing)
    ├── commands.py          ← All PC automation commands
    ├── whatsapp.py          ← WhatsApp Web automation + contact book
    ├── gui.py               ← Sci-fi HUD status window (Tkinter)
    └── __init__.py
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/venkatsaiganesh23-byte/BOB-AI-Assistant.git
cd BOB-AI-Assistant
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

> ⚠️ **PyAudio on Windows** (required for microphone):
> ```bash
> pip install pipwin
> pipwin install pyaudio
> ```

### 3. Get your Gemini API Key (FREE)
- Go to 👉 [https://aistudio.google.com/](https://aistudio.google.com/)
- Create a free API key
- Open `modules/assistant.py` and replace:
```python
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"
```

### 4. Add your contacts (for WhatsApp)
Open `modules/whatsapp.py` and edit:
```python
CONTACTS = {
    "mom":  "+91XXXXXXXXXX",
    "ravi": "+91XXXXXXXXXX",
}
```

### 5. Run BOB!
```bash
python main.py
```

---

## 🎤 Voice Commands

### 💬 WhatsApp
```
"Hey Bob... Send WhatsApp to Ravi saying I'm on my way"
"Message Mom that I'll be late"
"Text Ganesh meeting at 3 PM"
```

### 📂 Open Apps
```
"Open Chrome"       → Google Chrome
"Open VS Code"      → Visual Studio Code
"Open WhatsApp"     → WhatsApp desktop
"Open Notepad"      → Notepad
"Open Spotify"      → Spotify
```

### 🌐 Web & YouTube
```
"Search for Python tutorials"
"Play Believer on YouTube"
"Google latest cricket score"
```

### ⌨️ Auto Typing
```
"Type Hello how are you"
"Type this is my college project"
```

### 🖥️ System
```
"Take a screenshot"     → Saved to Desktop
"Volume up / down"      → System volume control
"Mute"                  → Mutes audio
"Lock screen"           → Locks the PC
"Close"                 → Closes active window
"Minimize / Maximize"   → Window control
```

### 🧠 AI (Gemini fallback)
```
"What is machine learning?"
"Explain Python decorators"
"Help me write an email"
"Translate hello to Telugu"
```

---

## 🧰 Tech Stack

| Technology | Purpose |
|------------|---------|
| `Python 3.10+` | Core language |
| `SpeechRecognition` | Voice input via microphone |
| `pyttsx3` | Text-to-speech output |
| `Google Gemini AI` | AI question answering |
| `pyautogui` | Desktop automation |
| `pywhatkit` | WhatsApp Web integration |
| `tkinter` | Sci-fi HUD GUI |
| `opencv-python` | Computer vision (future) |

---

## 🔮 Roadmap

- [x] Voice activation with wake word
- [x] Gemini AI integration
- [x] WhatsApp automation
- [x] App launcher & system control
- [x] Sci-Fi HUD window
- [ ] Face recognition login (OpenCV)
- [ ] Gmail automation
- [ ] Reminder & alarm system
- [ ] Spotify music control
- [ ] Offline mode (local LLM)

---

## 👨‍💻 Author

<div align="center">

**Venkat Sai Ganesh**
[![GitHub](https://img.shields.io/badge/GitHub-venkatsaiganesh23--byte-181717?style=flat-square&logo=github)](https://github.com/venkatsaiganesh23-byte)

*Built for College Review 2 — 2026*

</div>

---

<div align="center">

**⭐ Star this repo if you found it useful!**

`BOB-AI © 2026 — Venkat Sai Ganesh`

</div>
