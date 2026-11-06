"""
BOB-AI v2 — WhatsApp Module
✅ Selenium-based — accesses actual contacts + groups directly
✅ No phone number required — searches by name
✅ Session saved — scan QR only once ever
✅ Works for both personal chats and group chats
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os


PROFILE_DIR = os.path.join(os.getcwd(), "bob_wa_session")


class WhatsAppHandler:
    def __init__(self, speak_fn):
        self.speak  = speak_fn
        self.driver = None

    # ── LAUNCH ────────────────────────────────────────────
    def launch(self):
        """Launch WhatsApp Web. Scans QR only on first run."""
        if self.driver:
            try:
                _ = self.driver.title
                return True
            except:
                self.driver = None

        try:
            opts = Options()
            opts.add_argument(f"--user-data-dir={PROFILE_DIR}")
            opts.add_argument("--no-sandbox")
            opts.add_argument("--disable-dev-shm-usage")
            opts.add_experimental_option("detach", True)
            opts.add_experimental_option("excludeSwitches", ["enable-logging"])

            self.driver = webdriver.Chrome(options=opts)
            self.driver.get("https://web.whatsapp.com")

            self.speak("WhatsApp Web is loading. If it's your first time, scan the QR code.")
            WebDriverWait(self.driver, 90).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, 'div[aria-label="Chat list"]')
                )
            )
            print("[BOB] ✅ WhatsApp Web ready!")
            return True

        except Exception as e:
            print(f"[BOB] ❌ WhatsApp launch failed: {e}")
            self.speak("WhatsApp Web couldn't load. Make sure Chrome is installed.")
            return False

    # ── SEARCH & OPEN CHAT ────────────────────────────────
    def open_chat(self, name: str) -> bool:
        """Search for a contact or group by name and open the chat."""
        if not self.driver:
            if not self.launch():
                return False

        try:
            # Click search bar
            search_btn = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, 'button[aria-label="Search or start new chat"]')
                )
            )
            search_btn.click()
            time.sleep(0.5)

            # Type name
            search_box = self.driver.find_element(
                By.CSS_SELECTOR, 'div[aria-label="Search input textbox"]'
            )
            search_box.clear()
            search_box.send_keys(name)
            time.sleep(2)

            # Click first result
            results = self.driver.find_elements(
                By.CSS_SELECTOR, 'div[aria-label="Search results."] div[role="listitem"]'
            )
            if not results:
                print(f"[BOB] No results for '{name}'")
                return False

            results[0].click()
            time.sleep(1)
            return True

        except Exception as e:
            print(f"[BOB] ❌ open_chat error: {e}")
            return False

    # ── SEND MESSAGE ──────────────────────────────────────
    def send(self, recipient: str, message: str) -> bool:
        """Send a message to a contact or group by name."""
        if not self.open_chat(recipient):
            self.speak(f"Couldn't find {recipient} on WhatsApp.")
            return False

        if not message or not message.strip():
            return True  # just opened chat

        try:
            msg_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, 'div[aria-label="Type a message"]')
                )
            )
            msg_box.click()
            msg_box.send_keys(message)
            msg_box.send_keys(Keys.ENTER)
            print(f"[BOB] ✅ Sent to '{recipient}': {message}")
            return True

        except Exception as e:
            print(f"[BOB] ❌ send error: {e}")
            self.speak("Opened the chat but couldn't type the message.")
            return False

    # ── READ MESSAGES ─────────────────────────────────────
    def read_last(self, recipient: str, count: int = 5) -> list:
        """Open a chat and return last N messages."""
        if not self.open_chat(recipient):
            return []

        try:
            msgs = self.driver.find_elements(
                By.CSS_SELECTOR,
                'div.message-in span.selectable-text, '
                'div.message-out span.selectable-text'
            )
            last = [m.text for m in msgs[-count:] if m.text.strip()]
            print(f"[BOB] Read {len(last)} messages from '{recipient}'")
            return last
        except Exception as e:
            print(f"[BOB] ❌ read error: {e}")
            return []

    # ── CLOSE ─────────────────────────────────────────────
    def close(self):
        try:
            if self.driver:
                self.driver.quit()
                self.driver = None
        except:
            pass
