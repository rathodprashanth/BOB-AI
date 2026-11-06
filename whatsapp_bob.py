from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

# ─── Keep session so you only scan QR once ───────────────────────────
PROFILE_DIR = os.path.join(os.getcwd(), "bob_whatsapp_session")

def launch_whatsapp():
    options = webdriver.ChromeOptions()
    options.add_argument(f"--user-data-dir={PROFILE_DIR}")  # saves login session
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    driver.get("https://web.whatsapp.com")
    print("[BOB] Waiting for WhatsApp Web to load...")

    # Wait until chats are visible (means logged in)
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-label="Chat list"]'))
    )
    print("[BOB] WhatsApp Web loaded!")
    return driver


# ─── Fetch all contacts and groups from chat list ────────────────────
def get_all_chats(driver):
    chats = {}
    chat_list = driver.find_elements(
        By.CSS_SELECTOR, 'div[aria-label="Chat list"] div[role="listitem"]'
    )

    for chat in chat_list:
        try:
            name = chat.find_element(By.CSS_SELECTOR, 'span[title]').get_attribute("title")
            if name:
                chats[name.lower()] = chat  # store by lowercase name
        except:
            continue

    print(f"[BOB] Found {len(chats)} chats (contacts + groups)")
    return chats


# ─── Send message to a contact or group by name (from chat list) ─────
def send_message(driver, name, message):
    chats = get_all_chats(driver)
    name_lower = name.lower()

    # Find best match
    match = None
    for chat_name in chats:
        if name_lower in chat_name:
            match = chat_name
            break

    if not match:
        print(f"[BOB] Contact/Group '{name}' not found in recent chats!")
        return False

    # Click the chat
    chats[match].click()
    time.sleep(1)

    # Type and send message
    msg_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-label="Type a message"]'))
    )
    msg_box.click()
    msg_box.send_keys(message)
    msg_box.send_keys(Keys.ENTER)
    print(f"[BOB] ✅ Message sent to '{match}'!")
    return True


# ─── Search for any contact or group (even not in recent chats) ──────
def search_and_send(driver, name, message):
    try:
        # Click the search button
        search_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'button[aria-label="Search or start new chat"]')
            )
        )
        search_btn.click()
        time.sleep(0.5)

        # Type the contact/group name
        search_box = driver.find_element(
            By.CSS_SELECTOR, 'div[aria-label="Search input textbox"]'
        )
        search_box.send_keys(name)
        time.sleep(2)  # wait for results to load

        # Click first result
        results = driver.find_elements(
            By.CSS_SELECTOR, 'div[aria-label="Search results."] div[role="listitem"]'
        )
        if not results:
            print(f"[BOB] No results found for '{name}'")
            return False

        results[0].click()
        time.sleep(1)

        # Type and send message
        msg_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'div[aria-label="Type a message"]')
            )
        )
        msg_box.send_keys(message)
        msg_box.send_keys(Keys.ENTER)
        print(f"[BOB] ✅ Message sent to '{name}'!")
        return True

    except Exception as e:
        print(f"[BOB] ❌ Error sending message: {e}")
        return False


# ─── Read last N messages from current open chat ─────────────────────
def read_last_messages(driver, count=5):
    try:
        messages = driver.find_elements(
            By.CSS_SELECTOR, 'div.message-in span.selectable-text, div.message-out span.selectable-text'
        )
        last = messages[-count:] if len(messages) >= count else messages
        print(f"[BOB] Last {len(last)} messages:")
        for msg in last:
            print(" →", msg.text)
        return [m.text for m in last]
    except Exception as e:
        print(f"[BOB] ❌ Could not read messages: {e}")
        return []
