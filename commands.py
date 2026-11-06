"""
BOB-AI v2 — Command Handler
✅ WhatsApp via Selenium — direct contact + group access, no phone number needed
✅ Gmail via SMTP with listen_raw follow-ups (bypasses Gemini)
✅ All follow-up questions use listen_raw — no more Gemini interference
✅ Friendly buddy tone throughout
"""

import os, time, datetime, webbrowser, subprocess, threading, random
import pyautogui
pyautogui.PAUSE    = 0.3
pyautogui.FAILSAFE = True

# ══════════════════════════════════════════════════════════
#  CONFIG — Fill these in
# ══════════════════════════════════════════════════════════

# Gmail SMTP — get App Password at: myaccount.google.com/apppasswords
GMAIL_ADDRESS  = "venkatsaiganesh23@gmail.com"
GMAIL_PASSWORD = "ganeshsrh"

# Email contacts (name → email address)
EMAIL_CONTACTS = {
    "bro":    "svsgtweets@gmail.com",
    "dad":    "dad@gmail.com",
    "ganesh": "ganesh@gmail.com",
    # add more
}

JOKES = [
    "Why do programmers prefer dark mode? Because light attracts bugs!",
    "I told my computer I needed a break. Now it won't stop sending me KitKat ads.",
    "Why was the Python dev so calm? He knew how to handle exceptions.",
    "How do you comfort a JavaScript dev? You console them.",
    "My code doesn't have bugs. It has surprise features.",
]

ROASTS = [
    "Bro asked me a dumb question and still expects a smart answer.",
    "Even my loading screen is smarter than that question.",
    "I'm an AI and even I felt that one.",
]


class CommandHandler:
    def __init__(self, speak_fn, listen_raw_fn=None, gui_fn=None):
        self.speak      = speak_fn
        self.listen_raw = listen_raw_fn   # ✅ KEY: raw listen bypasses Gemini
        self.gui        = gui_fn
        self._wa_driver = None            # Selenium WhatsApp driver (lazy init)

    def _log(self, text, role="info"):
        if self.gui: self.gui(text, role)

    # ══════════════════════════════════════════════════════
    #  MAIN ROUTER — WhatsApp/Gmail caught BEFORE Gemini
    # ══════════════════════════════════════════════════════
    def handle(self, command: str) -> bool:
        c = command.lower().strip()

        # ── Greetings & small talk ────────────────────────
        if any(w in c for w in ["hello bob", "hi bob", "good morning", "good evening", "good night"]):
            return self._greet(c)
        if "how are you" in c:
            self.speak(random.choice([
                "Running clean, no bugs today — unlike your last project.",
                "All systems optimal. What do you need?",
                "Better than ever. What's the plan?",
            ])); return True
        if "your name" in c or "who are you" in c:
            self.speak("I'm BOB — Built by Ganesh, sharper than your average assistant."); return True
        if "joke" in c or "make me laugh" in c or "tell me something funny" in c:
            self.speak(random.choice(JOKES)); return True
        if "roast" in c or "roast me" in c:
            self.speak(random.choice(ROASTS)); return True

        # ── Time / Date ───────────────────────────────────
        if ("what" in c and "time" in c) or c == "time":
            return self._tell_time()
        if "date" in c or ("today" in c and "date" in c):
            return self._tell_date()
        if "what" in c and "day" in c:
            return self._tell_day()

        # ── YouTube ───────────────────────────────────────
        if any(w in c for w in ["play ", "play on youtube", "youtube", "search youtube"]):
            return self._youtube(c)

        # ── WhatsApp ── caught BEFORE Gemini ──────────────
        if any(w in c for w in ["whatsapp", "send message", "send whatsapp",
                                 "message to", "text to", "send text"]):
            return self._whatsapp_text(c)

        if any(w in c for w in ["whatsapp call", "call on whatsapp", "video call"]):
            return self._whatsapp_call(c)

        if any(w in c for w in ["read whatsapp", "check whatsapp", "read messages",
                                 "any messages", "whatsapp messages"]):
            return self._whatsapp_read(c)

        # ── Gmail ── caught BEFORE Gemini ─────────────────
        if any(w in c for w in ["send email", "send mail", "email to",
                                 "mail to", "compose email", "write email"]):
            return self._send_email(c)

        # ── Open apps ─────────────────────────────────────
        if c.startswith("open "):
            return self._open_app(c.replace("open ", "").strip())

        # ── Web search ────────────────────────────────────
        if any(w in c for w in ["search for", "search ", "google ", "look up"]):
            return self._web_search(c)

        # ── Screenshot ────────────────────────────────────
        if any(w in c for w in ["screenshot", "capture screen", "take screenshot"]):
            return self._screenshot()

        # ── Volume ────────────────────────────────────────
        if any(w in c for w in ["volume up", "increase volume", "louder"]):
            return self._volume("up")
        if any(w in c for w in ["volume down", "decrease volume", "quieter"]):
            return self._volume("down")
        if "mute" in c:
            return self._volume("mute")

        # ── Type ──────────────────────────────────────────
        if c.startswith("type "):
            return self._type_text(c.replace("type ", "", 1))

        # ── System ────────────────────────────────────────
        if "lock" in c and ("screen" in c or "pc" in c or "computer" in c):
            return self._lock()
        if "shutdown" in c and ("computer" in c or "pc" in c):
            return self._shutdown()
        if "restart" in c and ("computer" in c or "pc" in c):
            return self._restart()
        if "minimize" in c:
            pyautogui.hotkey("win", "down"); self.speak("Done."); return True
        if "maximize" in c:
            pyautogui.hotkey("win", "up"); self.speak("Done."); return True
        if any(w in c for w in ["close this", "close window", "close app", "close it"]):
            pyautogui.hotkey("alt", "f4"); self.speak("Closed."); return True
        if "switch window" in c or "alt tab" in c:
            pyautogui.hotkey("alt", "tab"); self.speak("Switched."); return True
        if "copy" in c:
            pyautogui.hotkey("ctrl", "c"); self.speak("Copied."); return True
        if "paste" in c:
            pyautogui.hotkey("ctrl", "v"); self.speak("Pasted."); return True

        # ── Battery ───────────────────────────────────────
        if "battery" in c:
            return self._battery()

        return False  # → falls through to Gemini

    # ══════════════════════════════════════════════════════
    #  HELPERS
    # ══════════════════════════════════════════════════════
    def _ask(self, question: str) -> str:
        """Ask a follow-up question and get raw speech (bypasses Gemini)."""
        self.speak(question)
        if self.listen_raw:
            return self.listen_raw()
        return ""

    # ══════════════════════════════════════════════════════
    #  GREETINGS
    # ══════════════════════════════════════════════════════
    def _greet(self, c):
        h = datetime.datetime.now().hour
        if h < 12:
            self.speak(random.choice([
                "Morning! Ready to get things done?",
                "Good morning, let's make today count.",
            ]))
        elif h < 17:
            self.speak(random.choice([
                "Afternoon! What are we working on?",
                "Hey! What do you need?",
            ]))
        else:
            self.speak(random.choice([
                "Evening! Still grinding I see.",
                "Good evening. What's up?",
            ]))
        return True

    def _tell_time(self):
        self.speak(f"It's {datetime.datetime.now().strftime('%I:%M %p')}.")
        return True

    def _tell_date(self):
        self.speak(f"Today's {datetime.datetime.now().strftime('%A, %B %d, %Y')}.")
        return True

    def _tell_day(self):
        self.speak(f"It's {datetime.datetime.now().strftime('%A')}.")
        return True

    # ══════════════════════════════════════════════════════
    #  WHATSAPP — Selenium, direct contacts + groups
    # ══════════════════════════════════════════════════════
    def _get_wa_driver(self):
        """Lazy-init WhatsApp Selenium driver. Keeps session across commands."""
        if self._wa_driver:
            try:
                _ = self._wa_driver.title  # check if still alive
                return self._wa_driver
            except:
                self._wa_driver = None

        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            import os

            profile_dir = os.path.join(os.getcwd(), "bob_wa_session")
            opts = Options()
            opts.add_argument(f"--user-data-dir={profile_dir}")
            opts.add_argument("--no-sandbox")
            opts.add_argument("--disable-dev-shm-usage")
            opts.add_experimental_option("detach", True)
            opts.add_experimental_option("excludeSwitches", ["enable-logging"])

            driver = webdriver.Chrome(options=opts)
            driver.get("https://web.whatsapp.com")
            self._log("Waiting for WhatsApp Web to load...", "processing")

            WebDriverWait(driver, 90).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, 'div[aria-label="Chat list"]')
                )
            )
            self._wa_driver = driver
            self._log("WhatsApp Web ready!", "system")
            return driver
        except Exception as e:
            self._log(f"WhatsApp init failed: {e}", "error")
            return None

    def _wa_search_and_send(self, name: str, message: str) -> bool:
        """Search for a contact/group by name and send a message."""
        try:
            from selenium.webdriver.common.by import By
            from selenium.webdriver.common.keys import Keys
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC

            driver = self._get_wa_driver()
            if not driver:
                return False

            # Click search
            search_btn = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, 'button[aria-label="Search or start new chat"]')
                )
            )
            search_btn.click()
            time.sleep(0.5)

            # Type name
            search_box = driver.find_element(
                By.CSS_SELECTOR, 'div[aria-label="Search input textbox"]'
            )
            search_box.clear()
            search_box.send_keys(name)
            time.sleep(2)

            # Click first result
            results = driver.find_elements(
                By.CSS_SELECTOR, 'div[aria-label="Search results."] div[role="listitem"]'
            )
            if not results:
                self._log(f"No WhatsApp results for '{name}'", "error")
                return False

            results[0].click()
            time.sleep(1)

            # Only send if message is non-empty
            if message and message.strip():
                msg_box = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, 'div[aria-label="Type a message"]')
                    )
                )
                msg_box.click()
                msg_box.send_keys(message)
                msg_box.send_keys(Keys.ENTER)
                self._log(f"✅ Sent to '{name}'", "system")

            return True
        except Exception as e:
            self._log(f"WhatsApp send error: {e}", "error")
            return False

    def _whatsapp_text(self, command):
        c = command.lower()

        # Try to extract name from command (e.g. "send message to chaitanya")
        recipient = ""
        message   = ""

        if " to " in c:
            after = c.split(" to ", 1)[1]
            words = after.split()
            name_words, msg_start = [], len(words)
            for i, w in enumerate(words):
                if w in ["saying", "that", "message", "say", "tell", "with"]:
                    msg_start = i + 1; break
                name_words.append(w)
            recipient = " ".join(name_words).strip()
            message   = " ".join(words[msg_start:]).strip()

        # ✅ Use listen_raw for missing parts — bypasses Gemini
        if not recipient:
            recipient = self._ask("Who should I message?")
        if not recipient:
            self.speak("Didn't catch the name, try again.")
            return True

        if not message:
            message = self._ask(f"What should I tell {recipient}?")
        if not message:
            self.speak("Didn't catch the message, try again.")
            return True

        self.speak(f"Sending to {recipient} on WhatsApp.")
        self._log(f"WhatsApp → {recipient}: {message}", "processing")

        success = self._wa_search_and_send(recipient, message)
        if success:
            self.speak(f"Done, message sent to {recipient}!")
        else:
            self.speak(f"Couldn't find {recipient} on WhatsApp.")
        return True

    def _whatsapp_call(self, command):
        c = command.lower()
        recipient = ""
        for prefix in ["whatsapp call", "video call", "call on whatsapp", "call "]:
            if prefix in c:
                recipient = c.split(prefix, 1)[1].strip(); break

        if not recipient:
            recipient = self._ask("Who should I call on WhatsApp?")
        if not recipient:
            self.speak("Didn't get the name."); return True

        self.speak(f"Opening {recipient}'s chat for a call.")
        self._wa_search_and_send(recipient, "")  # open chat
        self.speak("Opened the chat — tap call when ready.")
        return True

    def _whatsapp_read(self, command):
        c = command.lower()
        recipient = ""
        for prefix in ["read messages from", "check whatsapp from",
                        "read whatsapp from", "messages from"]:
            if prefix in c:
                recipient = c.split(prefix, 1)[1].strip(); break

        if not recipient:
            recipient = self._ask("Whose chat should I open?")
        if not recipient:
            self.speak("Didn't get the name."); return True

        self.speak(f"Opening {recipient}'s chat.")
        opened = self._wa_search_and_send(recipient, "")

        if opened:
            try:
                from selenium.webdriver.common.by import By
                driver = self._wa_driver
                msgs = driver.find_elements(
                    By.CSS_SELECTOR,
                    'div.message-in span.selectable-text, '
                    'div.message-out span.selectable-text'
                )
                last = [m.text for m in msgs[-5:] if m.text.strip()]
                if last:
                    self.speak(f"Last {len(last)} messages from {recipient}:")
                    for m in last:
                        self.speak(m)
                else:
                    self.speak("No readable messages found.")
            except Exception as e:
                self.speak("Opened the chat — couldn't read messages automatically.")
        else:
            self.speak(f"Couldn't find {recipient}.")
        return True

    # ══════════════════════════════════════════════════════
    #  GMAIL — SMTP with listen_raw follow-ups
    # ══════════════════════════════════════════════════════
    def _send_email(self, command):
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        c = command.lower()

        # Try parsing from command first
        to_email = ""
        subject  = ""
        body     = ""

        if " to " in c:
            after     = c.split(" to ", 1)[1].split()[0].strip()
            # Check contacts book first
            to_email  = EMAIL_CONTACTS.get(after.lower(), after)

        # ✅ Use listen_raw for missing parts — bypasses Gemini
        if not to_email:
            raw = self._ask("Who should I email? Say a name or email address.")
            if raw:
                to_email = EMAIL_CONTACTS.get(raw.strip().lower(), raw.strip())

        if not to_email:
            self.speak("Didn't get the recipient."); return True

        subject = self._ask("What's the subject?")
        if not subject:
            subject = "Message from BOB-AI"

        body = self._ask("What should the email say?")
        if not body:
            self.speak("Didn't get the message body."); return True

        self.speak(f"Sending your email to {to_email}, give me a sec.")
        self._log(f"Gmail → {to_email} | Subject: {subject}", "processing")

        try:
            msg             = MIMEMultipart()
            msg["From"]     = GMAIL_ADDRESS
            msg["To"]       = to_email
            msg["Subject"]  = subject.capitalize()
            msg.attach(MIMEText(body, "plain"))

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
                s.login(GMAIL_ADDRESS, GMAIL_PASSWORD)
                s.sendmail(GMAIL_ADDRESS, to_email, msg.as_string())

            self.speak(f"Email sent to {to_email}. Done!")
        except smtplib.SMTPAuthenticationError:
            self.speak("Gmail auth failed. Set your App Password in commands.py.")
        except Exception as e:
            self._log(f"Gmail error: {e}", "error")
            self.speak("Couldn't send the email. Check your Gmail settings.")
        return True

    # ══════════════════════════════════════════════════════
    #  YOUTUBE
    # ══════════════════════════════════════════════════════
    def _youtube(self, command):
        query = command
        for p in ["search youtube for", "play on youtube", "play on yt",
                  "on youtube", "youtube search", "youtube", "play "]:
            query = query.replace(p, "").strip()
        query = query.strip()

        if not query:
            self.speak("Opening YouTube.")
            webbrowser.open("https://www.youtube.com"); return True

        self.speak(f"Playing {query} on YouTube.")
        self._log(f"YouTube → '{query}'", "processing")
        threading.Thread(target=self._yt_selenium, args=(query,), daemon=True).start()
        return True

    def _yt_selenium(self, query):
        try:
            from selenium import webdriver
            from selenium.webdriver.common.by import By
            from selenium.webdriver.common.keys import Keys
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC

            opts = Options()
            opts.add_argument("--start-maximized")
            opts.add_argument("--autoplay-policy=no-user-gesture-required")
            opts.add_experimental_option("detach", True)
            opts.add_experimental_option("excludeSwitches", ["enable-logging"])

            driver = webdriver.Chrome(options=opts)
            driver.get(f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}")
            wait = WebDriverWait(driver, 10)

            video = wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "ytd-video-renderer a#video-title")
                )
            )
            url = video.get_attribute("href")
            driver.get(url + ("&autoplay=1" if "?" in url else "?autoplay=1"))
            time.sleep(3)

            driver.execute_script("""
                try {
                    var p = document.getElementById('movie_player');
                    if (p) { p.unMute(); p.setVolume(100); p.playVideo(); }
                } catch(e) {}
            """)
        except Exception as e:
            webbrowser.open(
                f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
            )

    # ══════════════════════════════════════════════════════
    #  OPEN APPS
    # ══════════════════════════════════════════════════════
    def _open_app(self, app_name):
        key = app_name.lower().strip()
        self.speak(f"Opening {app_name}.")

        builtins = {
            "notepad":"notepad", "calculator":"calc", "paint":"mspaint",
            "task manager":"taskmgr", "cmd":"cmd", "command prompt":"cmd",
            "file explorer":"explorer", "explorer":"explorer",
            "control panel":"control",
        }
        if key in builtins:
            os.system(f"start {builtins[key]}"); return True

        if key in ["chrome", "google chrome"]:
            for p in [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
            ]:
                if os.path.exists(p):
                    subprocess.Popen([p]); return True
            os.system("start chrome"); return True

        web = {
            "youtube":"https://www.youtube.com", "gmail":"https://mail.google.com",
            "google":"https://www.google.com",   "whatsapp":"https://web.whatsapp.com",
            "instagram":"https://www.instagram.com", "github":"https://www.github.com",
            "spotify":"https://open.spotify.com", "netflix":"https://www.netflix.com",
        }
        if key in web:
            webbrowser.open(web[key]); return True

        apps = {
            "vs code":    [os.path.expandvars(r"%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe")],
            "vscode":     [os.path.expandvars(r"%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe")],
            "spotify":    [os.path.expandvars(r"%APPDATA%\Spotify\Spotify.exe")],
            "discord":    [os.path.expandvars(r"%LOCALAPPDATA%\Discord\Update.exe")],
            "whatsapp":   [os.path.expandvars(r"%LOCALAPPDATA%\WhatsApp\WhatsApp.exe")],
            "telegram":   [os.path.expandvars(r"%APPDATA%\Telegram Desktop\Telegram.exe")],
            "vlc":        [r"C:\Program Files\VideoLAN\VLC\vlc.exe"],
            "zoom":       [os.path.expandvars(r"%APPDATA%\Zoom\bin\Zoom.exe")],
            "word":       [r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE"],
            "excel":      [r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE"],
            "powerpoint": [r"C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE"],
        }
        if key in apps:
            for p in apps[key]:
                if os.path.exists(p):
                    subprocess.Popen([p]); return True

        os.system(f"start {key}"); return True

    # ══════════════════════════════════════════════════════
    #  WEB SEARCH
    # ══════════════════════════════════════════════════════
    def _web_search(self, command):
        q = command
        for p in ["search for", "search", "google", "look up", "find"]:
            q = q.replace(p, "").strip()
        if q:
            self.speak(f"Searching for {q}.")
            webbrowser.open(f"https://www.google.com/search?q={q.replace(' ', '+')}")
        return True

    # ══════════════════════════════════════════════════════
    #  SCREENSHOT
    # ══════════════════════════════════════════════════════
    def _screenshot(self):
        try:
            ts      = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            os.makedirs(desktop, exist_ok=True)
            path    = os.path.join(desktop, f"BOB_{ts}.png")
            self.speak("Taking the screenshot now.")
            time.sleep(0.8)
            import pyautogui as pg
            img = pg.screenshot()
            img.save(path)
            self.speak("Screenshot saved to your Desktop!")
        except Exception:
            self.speak("Using snipping tool instead.")
            os.system("snippingtool")
        return True

    # ══════════════════════════════════════════════════════
    #  VOLUME
    # ══════════════════════════════════════════════════════
    def _volume(self, action):
        if action == "up":
            for _ in range(5): pyautogui.press("volumeup")
            self.speak("Turned it up.")
        elif action == "down":
            for _ in range(5): pyautogui.press("volumedown")
            self.speak("Turned it down.")
        elif action == "mute":
            pyautogui.press("volumemute")
            self.speak("Muted.")
        return True

    # ══════════════════════════════════════════════════════
    #  TYPE TEXT
    # ══════════════════════════════════════════════════════
    def _type_text(self, text):
        if text:
            self.speak("On it.")
            time.sleep(0.5)
            pyautogui.write(text, interval=0.04)
        return True

    # ══════════════════════════════════════════════════════
    #  BATTERY
    # ══════════════════════════════════════════════════════
    def _battery(self):
        try:
            import psutil
            b = psutil.sensors_battery()
            if b:
                status = "charging" if b.power_plugged else "not plugged in"
                self.speak(f"Battery's at {int(b.percent)}%, {status}.")
            else:
                self.speak("Can't read battery on this device.")
        except:
            self.speak("Install psutil to check battery — python -m pip install psutil.")
        return True

    # ══════════════════════════════════════════════════════
    #  SYSTEM
    # ══════════════════════════════════════════════════════
    def _lock(self):
        self.speak("Locking your screen.")
        os.system("rundll32.exe user32.dll,LockWorkStation"); return True

    def _shutdown(self):
        self.speak("Shutting down in 10 seconds.")
        os.system("shutdown /s /t 10"); return True

    def _restart(self):
        self.speak("Restarting in 10 seconds.")
        os.system("shutdown /r /t 10"); return True
