from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def play_youtube(query="pushpass songs"):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--autoplay-policy=no-user-gesture-required")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 15)

    try:
        print(f"🔍 Searching: {query}")

        # Step 1: Go to search results
        driver.get(f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}")

        # Step 2: Get first video URL
        first_video = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ytd-video-renderer a#video-title"))
        )
        video_url = first_video.get_attribute("href")
        title = first_video.get_attribute("title")
        print(f"▶️  Found: {title}")

        # Step 3: Open video directly
        driver.get(video_url)
        time.sleep(3)

        # Step 4: Use YouTube's internal JS player API to force play (NO keyboard!)
        driver.execute_script("""
            // Method 1: HTML5 video element
            var video = document.querySelector('video');
            if (video) {
                video.muted = false;
                video.volume = 1.0;
                video.play();
            }
        """)
        time.sleep(1)

        # Step 5: Use YouTube's own player object (most powerful!)
        driver.execute_script("""
            try {
                var player = document.getElementById('movie_player');
                if (player && player.playVideo) {
                    player.setVolume(100);
                    player.unMute();
                    player.playVideo();
                }
            } catch(e) {}
        """)

        time.sleep(2)

        # Step 6: If still paused, click the actual play button via JS (NO mouse/keyboard!)
        driver.execute_script("""
            try {
                var btn = document.querySelector('.ytp-play-button');
                if (btn && btn.getAttribute('aria-label').includes('Play')) {
                    btn.click();
                }
            } catch(e) {}
        """)

        print("🎶 Playing now bro!")
        input("\nPress Enter to close...\n")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        driver.quit()

if __name__ == "__main__":
    play_youtube("pushpass songs")
