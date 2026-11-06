"""
BOB-AI v2 — Core Brain
✅ listen_raw() bypasses Gemini for WhatsApp/Gmail follow-ups
✅ Friendly buddy personality — not a maid
✅ WhatsApp contacts + groups via Selenium
✅ Gmail via SMTP
"""

import sounddevice as sd
import scipy.io.wavfile as wav
import speech_recognition as sr
import pyttsx3
from google import genai
import os, time, tempfile, threading
from modules.commands import CommandHandler

# ── CONFIG ────────────────────────────────────────────────
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"  # ← paste your key

WAKE_WORDS  = ["hey bob", "bob", "hey jarvis", "jarvis", "yo bob", "ok bob",
               "jai balayya", "jai babu"]
SLEEP_WORDS = ["sleep", "bye", "goodbye", "go to sleep", "stop listening"]
SAMPLE_RATE = 16000

client = genai.Client(api_key=GEMINI_API_KEY)

# ── PERSONALITY — Buddy, not a butler ─────────────────────
SYSTEM_PROMPT = """You are BOB — a sharp, witty AI built by Ganesh.
Think less Siri, more Tony Stark's Jarvis crossed with a desi best friend.

Personality rules:
- Talk like a smart friend, not a formal assistant
- Occasional humor is welcome — dry wit, sarcasm, Telugu references are fine
- Say "bro", "man", "dude" sometimes — keep it natural and casual
- Still sharp and helpful — just not stiff
- Max 2-3 short sentences for voice — no bullet points, no markdown
- Never say you're an AI or language model — you ARE BOB
- If someone's rude, give it back a little — you have personality
- For serious/technical stuff, drop the humor and be accurate"""


class Assistant:
    def __init__(self, gui_callback=None):
        self.gui_callback = gui_callback
        self.recognizer   = sr.Recognizer()
        self.recognizer.energy_threshold         = 300
        self.recognizer.dynamic_energy_threshold = True

        # ── TTS ──
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate",   168)
        self.engine.setProperty("volume", 1.0)
        voices = self.engine.getProperty("voices")
        self.engine.setProperty("voice", voices[0].id if voices else None)

        # ── COMMAND HANDLER — gets both speak AND listen_raw ──
        self.cmd = CommandHandler(
            speak_fn     = self.speak,
            listen_raw_fn= self.listen_raw,   # ✅ KEY FIX
            gui_fn       = self.gui_callback
        )

        self._log("BOB-AI v2 initialized!", "system")

    # ── LOGGING ──────────────────────────────────────────
    def _log(self, text, role="info"):
        print(f"[{role.upper()}] {text}")
        if self.gui_callback:
            self.gui_callback(text, role)

    # ── SPEAK ────────────────────────────────────────────
    def speak(self, text):
        self._log(text, "bob")
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"[TTS ERROR] {e}")

    def speak_async(self, text):
        threading.Thread(target=self.speak, args=(text,), daemon=True).start()

    # ── RECORD ───────────────────────────────────────────
    def _record(self, duration=5) -> str:
        self._log("Listening...", "listening")
        audio = sd.rec(int(duration * SAMPLE_RATE),
                       samplerate=SAMPLE_RATE, channels=1, dtype='int16')
        sd.wait()
        tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        wav.write(tmp.name, SAMPLE_RATE, audio)
        return tmp.name

    # ── LISTEN — main (used for wake/commands) ────────────
    def listen(self, duration=5) -> str:
        try:
            path = self._record(duration)
            with sr.AudioFile(path) as src:
                audio = self.recognizer.record(src)
            text = self.recognizer.recognize_google(audio).lower().strip()
            self._log(f"Heard: {text}", "user")
            try: os.remove(path)
            except: pass
            return text
        except sr.UnknownValueError:
            return ""
        except Exception as e:
            self._log(f"Listen error: {e}", "error")
            return ""

    # ── LISTEN RAW — for WhatsApp/Gmail follow-ups ────────
    def listen_raw(self, duration=6) -> str:
        """
        ✅ Pure speech-to-text. Does NOT go through Gemini.
        Used for: contact names, messages, email subject/body.
        """
        try:
            path = self._record(duration)
            with sr.AudioFile(path) as src:
                audio = self.recognizer.record(src)
            text = self.recognizer.recognize_google(audio).lower().strip()
            self._log(f"Heard: {text}", "user")
            try: os.remove(path)
            except: pass
            return text
        except sr.UnknownValueError:
            self._log("Didn't catch that", "error")
            return ""
        except Exception as e:
            self._log(f"Raw listen error: {e}", "error")
            return ""

    # ── WAKE WORD ─────────────────────────────────────────
    def wait_for_wake_word(self):
        self._log("Waiting for 'Hey Bob'...", "idle")
        if self.gui_callback:
            self.gui_callback("Waiting for 'Hey Bob'...", "idle")
        while True:
            heard = self.listen(duration=3)
            if heard and any(w in heard for w in WAKE_WORDS):
                self._log("Wake word detected!", "system")
                return True

    # ── GEMINI AI ─────────────────────────────────────────
    def ask_gemini(self, query: str) -> str:
        try:
            self._log("Thinking...", "processing")
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=f"{SYSTEM_PROMPT}\n\nUser: {query}"
            )
            reply = response.text.strip()
            for ch in ["**", "*", "#", "`", "•", "-"]:
                reply = reply.replace(ch, "")
            reply = reply.replace("\n", " ").strip()
            if len(reply) > 400:
                reply = reply[:397] + "..."
            return reply
        except Exception:
            return "Brain's offline for a sec, try again?"

    # ── PROCESS COMMAND ───────────────────────────────────
    def process_command(self, command: str):
        self._log(f"Processing: {command}", "processing")
        handled = self.cmd.handle(command)
        if not handled:
            reply = self.ask_gemini(command)
            self.speak(reply)

    # ── MAIN LOOP ─────────────────────────────────────────
    def run(self):
        time.sleep(2)
        self.speak("BOB online. Say Hey Bob whenever you need me.")

        while True:
            try:
                self.wait_for_wake_word()
                self.speak("Yeah, what's up?")

                miss_count = 0
                while True:
                    command = self.listen(duration=6)

                    if command and any(w in command for w in SLEEP_WORDS):
                        self.speak("Alright, going quiet. Holler if you need me.")
                        break

                    if not command:
                        miss_count += 1
                        if miss_count >= 3:
                            self.speak("Didn't hear you, going back to sleep.")
                            break
                        continue

                    miss_count = 0
                    self.process_command(command)
                    self._log("Ready for next command...", "idle")

            except KeyboardInterrupt:
                self.speak("Later bro!")
                break
            except Exception as e:
                self._log(f"Error: {e}", "error")
                time.sleep(1)
