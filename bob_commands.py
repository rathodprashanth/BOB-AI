import time
import sys
import os
import webbrowser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.parse

# ─────────────────────────────────────────────
# 1. YOUTUBE - Auto Play Fix
# ─────────────────────────────────────────────
def play_youtube(query="pushpass songs"):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--autoplay-policy=no-user-gesture-required")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 15)

    try:
        print(f"🔍 Searching YouTube: {query}")

        # Go directly to search results
        driver.get(f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}")

        # Get first video URL
        first_video = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ytd-video-renderer a#video-title"))
        )
        video_url = first_video.get_attribute("href")
        title = first_video.get_attribute("title")
        print(f"🎯 Found: {title}")

        # Add autoplay=1 param to URL — forces YouTube to autoplay!
        if "?" in video_url:
            video_url += "&autoplay=1"
        else:
            video_url += "?autoplay=1"

        driver.get(video_url)
        print("📺 Loading video...")

        # Wait for player to be ready
        wait.until(EC.presence_of_element_located((By.ID, "movie_player")))
        time.sleep(3)

        # Force play using YouTube's internal player API
        for _ in range(5):
            result = driver.execute_script("""
                try {
                    var p = document.getElementById('movie_player');
                    if (p && typeof p.playVideo === 'function') {
                        p.unMute();
                        p.setVolume(100);
                        p.playVideo();
                        return p.getPlayerState();
                    }
                } catch(e) { return -99; }
            """)
            print(f"⚡ Player state: {result} (1=playing, 2=paused)")
            if result == 1:
                print("🎶 Playing! Enjoy bro!")
                break
            time.sleep(1)

        # Keep browser open
        input("\nPress Enter to close YouTube...\n")

    except Exception as e:
        print(f"❌ YouTube Error: {e}")
    finally:
        driver.quit()


# ─────────────────────────────────────────────
# 2. WHATSAPP - Send Message Fix
# ─────────────────────────────────────────────
def send_whatsapp(phone_number, message):
    """
    phone_number: include country code, no + or spaces
    Example: "919876543210" for India
    """
    try:
        print(f"📱 Opening WhatsApp for {phone_number}...")

        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        options.add_argument(r"--user-data-dir=C:\Users\\" + os.getenv("USERNAME", "User") + r"\AppData\Local\Google\Chrome\User Data")
        options.add_argument("--profile-directory=Default")

        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, 60)

        # Encode message for URL
        encoded_msg = urllib.parse.quote(message)
        url = f"https://web.whatsapp.com/send?phone={phone_number}&text={encoded_msg}"
        driver.get(url)

        print("⏳ Waiting for WhatsApp to load (scan QR if first time)...")

        # Wait for send button to appear
        send_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'span[data-icon="send"]'))
        )
        time.sleep(2)
        send_btn.click()
        print(f"✅ Message sent to {phone_number}!")

        time.sleep(3)
        driver.quit()

    except Exception as e:
        print(f"❌ WhatsApp Error: {e}")
        try:
            driver.quit()
        except:
            pass


# ─────────────────────────────────────────────
# 3. CLOSE / EXIT BOB - Fixed
# ─────────────────────────────────────────────
def close_bob():
    print("👋 Closing BOB AI... Goodbye bro!")
    time.sleep(1)
    sys.exit(0)


# ─────────────────────────────────────────────
# BOB Command Handler - Paste into your main BOB script
# ─────────────────────────────────────────────
def handle_command(command):
    command = command.lower().strip()

    # YouTube
    if "play" in command and ("youtube" in command or "song" in command or "video" in command):
        query = command.replace("play", "").replace("on youtube", "").replace("youtube", "").replace("song", "").replace("video", "").strip()
        if not query:
            query = "trending songs"
        play_youtube(query)

    # WhatsApp
    elif "whatsapp" in command or "send message" in command:
        # Example: "send whatsapp message to 919876543210 hello bro"
        parts = command.split()
        # Customize this parsing based on how you speak to BOB
        number = "919999999999"  # ← Replace with dynamic parsing
        message = "Hello from BOB AI!"
        send_whatsapp(number, message)

    # Close / Exit
    elif any(word in command for word in ["exit", "close", "quit", "bye", "goodbye", "shutdown", "stop"]):
        close_bob()

    else:
        print(f"🤖 Unknown command: {command}")


# ─────────────────────────────────────────────
# TEST IT
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("=== BOB AI Command Test ===")
    print("1. play pushpass songs on youtube")
    print("2. send whatsapp message")
    print("3. exit")
    choice = input("Enter command: ").strip()
    handle_command(choice)
