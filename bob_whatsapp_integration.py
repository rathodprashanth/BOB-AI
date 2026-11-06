import speech_recognition as sr
import pyttsx3
from whatsapp_bob import launch_whatsapp, search_and_send, read_last_messages

# ─── TTS Setup ───────────────────────────────────────────────────────
engine = pyttsx3.init()
engine.setProperty('rate', 170)

def speak(text):
    print(f"[BOB] {text}")
    engine.say(text)
    engine.runAndWait()

# ─── Speech Recognition ──────────────────────────────────────────────
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("[BOB] Listening...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        print(f"[You] {text}")
        return text.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError:
        speak("Speech service is unavailable.")
        return ""

# ─── Launch WhatsApp Web once at startup ─────────────────────────────
print("[BOB] Launching WhatsApp Web...")
wa_driver = launch_whatsapp()
speak("WhatsApp is ready.")

# ─── Main BOB Loop ───────────────────────────────────────────────────
def run_bob():
    while True:
        command = listen()

        if not command:
            continue

        # ── WhatsApp: Send Message ────────────────────────────────────
        if "whatsapp" in command or "send message" in command:
            speak("Who should I send the message to?")
            contact = listen()
            if not contact:
                speak("I didn't get the contact name.")
                continue

            speak("What's the message?")
            message = listen()
            if not message:
                speak("I didn't get the message.")
                continue

            speak(f"Sending message to {contact}...")
            success = search_and_send(wa_driver, contact, message)

            if success:
                speak(f"Message sent to {contact} on WhatsApp!")
            else:
                speak(f"Sorry, I couldn't find {contact} on WhatsApp.")

        # ── WhatsApp: Read Messages ───────────────────────────────────
        elif "read messages" in command or "check whatsapp" in command:
            speak("Who's chat should I read?")
            contact = listen()
            if contact:
                search_and_send(wa_driver, contact, "")  # open the chat
                msgs = read_last_messages(wa_driver, count=5)
                if msgs:
                    speak(f"Last {len(msgs)} messages from {contact}:")
                    for m in msgs:
                        speak(m)
                else:
                    speak("No messages found.")

        # ── Exit ──────────────────────────────────────────────────────
        elif "exit" in command or "stop" in command or "bye" in command:
            speak("Goodbye! Shutting down BOB AI.")
            wa_driver.quit()
            break

        else:
            speak("I didn't understand that command.")

# ─── Run ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    run_bob()
