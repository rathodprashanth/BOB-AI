"""
BOB-AI v2 — OTT Module
✅ Netflix, YouTube, Spotify, Amazon Prime, Hotstar, JioCinema, ZEE5, SonyLIV
✅ Opens, plays, searches — all by voice
✅ Selenium auto-play for YouTube
✅ Voice command examples at bottom
"""

import webbrowser
import time
import subprocess
import os
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


# ── OTT PLATFORM URLs ─────────────────────────────────────────────────
OTT_URLS = {
    "netflix":       "https://www.netflix.com",
    "youtube":       "https://www.youtube.com",
    "prime":         "https://www.primevideo.com",
    "amazon prime":  "https://www.primevideo.com",
    "hotstar":       "https://www.hotstar.com",
    "disney":        "https://www.hotstar.com",
    "disney hotstar":"https://www.hotstar.com",
    "jiocinema":     "https://www.jiocinema.com",
    "jio cinema":    "https://www.jiocinema.com",
    "zee5":          "https://www.zee5.com",
    "sony liv":      "https://www.sonyliv.com",
    "sonyliv":       "https://www.sonyliv.com",
    "mxplayer":      "https://www.mxplayer.in",
    "mx player":     "https://www.mxplayer.in",
    "voot":          "https://www.voot.com",
    "aha":           "https://www.aha.video",
    "sun nxt":       "https://www.sunnxt.com",
    "sunnxt":        "https://www.sunnxt.com",
}

# ── SEARCH URL TEMPLATES ──────────────────────────────────────────────
SEARCH_URLS = {
    "youtube":       "https://www.youtube.com/results?search_query={}",
    "netflix":       "https://www.netflix.com/search?q={}",
    "prime":         "https://www.primevideo.com/search/ref=atv_nb_sr?phrase={}",
    "amazon prime":  "https://www.primevideo.com/search/ref=atv_nb_sr?phrase={}",
    "hotstar":       "https://www.hotstar.com/in/search?q={}",
    "jiocinema":     "https://www.jiocinema.com/search?q={}",
    "zee5":          "https://www.zee5.com/search?q={}",
    "sonyliv":       "https://www.sonyliv.com/search?q={}",
    "aha":           "https://www.aha.video/search?q={}",
}


class OTTHandler:
    def __init__(self, speak_fn, listen_raw_fn=None, gui_fn=None):
        self.speak      = speak_fn
        self.listen_raw = listen_raw_fn
        self.gui        = gui_fn

    def _log(self, text, role="info"):
        print(f"[OTT] {text}")
        if self.gui: self.gui(text, role)

    def _ask(self, question: str) -> str:
        self.speak(question)
        return self.listen_raw() if self.listen_raw else ""

    # ── MAIN HANDLER ─────────────────────────────────────
    def handle(self, command: str) -> bool:
        c = command.lower().strip()

        # "open netflix / hotstar / prime etc"
        for platform, url in OTT_URLS.items():
            if platform in c and ("open" in c or "launch" in c or "start" in c):
                self.speak(f"Opening {platform.title()}.")
                webbrowser.open(url)
                return True

        # "play <title> on <platform>"
        if "play" in c:
            return self._play(c)

        # "search <query> on <platform>"
        if "search" in c:
            return self._search(c)

        # "watch <title>" — tries to detect platform from command
        if "watch" in c:
            return self._watch(c)

        return False

    # ── PLAY ─────────────────────────────────────────────
    def _play(self, command: str) -> bool:
        c = command.lower()

        # Detect platform
        platform = self._detect_platform(c)

        # Extract title
        title = c
        for word in ["play", "on", "in", platform or "", "youtube", "netflix",
                     "hotstar", "prime", "jiocinema", "zee5", "sonyliv", "aha"]:
            title = title.replace(word, "").strip()
        title = title.strip()

        if not title:
            title = self._ask("What should I play?")
        if not title:
            self.speak("Didn't get the title."); return True

        if not platform:
            platform = "youtube"  # default to YouTube

        self.speak(f"Playing {title} on {platform.title()}.")
        self._log(f"Play '{title}' on {platform}", "processing")

        if platform == "youtube":
            threading.Thread(
                target=self._youtube_autoplay,
                args=(title,), daemon=True
            ).start()
        elif platform in SEARCH_URLS:
            url = SEARCH_URLS[platform].format(title.replace(" ", "+"))
            webbrowser.open(url)
        else:
            url = OTT_URLS.get(platform, "https://www.youtube.com")
            webbrowser.open(url)

        return True

    # ── SEARCH ───────────────────────────────────────────
    def _search(self, command: str) -> bool:
        c = command.lower()
        platform = self._detect_platform(c)

        query = c
        for word in ["search", "for", "on", "in", platform or "", "youtube",
                     "netflix", "hotstar", "prime", "jiocinema"]:
            query = query.replace(word, "").strip()
        query = query.strip()

        if not query:
            query = self._ask("What should I search for?")
        if not query:
            self.speak("Didn't get the search query."); return True

        if not platform:
            platform = "youtube"

        self.speak(f"Searching for {query} on {platform.title()}.")
        url = SEARCH_URLS.get(platform, SEARCH_URLS["youtube"]).format(
            query.replace(" ", "+")
        )
        webbrowser.open(url)
        return True

    # ── WATCH ────────────────────────────────────────────
    def _watch(self, command: str) -> bool:
        c = command.lower()
        platform = self._detect_platform(c)

        title = c.replace("watch", "").strip()
        for word in ["on", "in", platform or "", "youtube", "netflix",
                     "hotstar", "prime", "jiocinema", "zee5"]:
            title = title.replace(word, "").strip()
        title = title.strip()

        if not title:
            title = self._ask("What do you want to watch?")
        if not title:
            self.speak("Didn't catch the title."); return True

        if not platform:
            platform = self._ask(
                "Which app? Netflix, Hotstar, Prime, JioCinema, YouTube?"
            ).lower()

        self.speak(f"Searching for {title} on {platform.title()}.")
        url = SEARCH_URLS.get(platform, SEARCH_URLS["youtube"]).format(
            title.replace(" ", "+")
        )
        webbrowser.open(url)
        return True

    # ── DETECT PLATFORM ──────────────────────────────────
    def _detect_platform(self, command: str) -> str:
        for platform in SEARCH_URLS.keys():
            if platform in command:
                return platform
        # aliases
        if "prime" in command or "amazon" in command:
            return "prime"
        if "disney" in command or "star" in command:
            return "hotstar"
        if "jio" in command:
            return "jiocinema"
        if "zee" in command:
            return "zee5"
        if "sony" in command:
            return "sonyliv"
        return ""

    # ── YOUTUBE SELENIUM AUTOPLAY ─────────────────────────
    def _youtube_autoplay(self, query: str):
        try:
            opts = Options()
            opts.add_argument("--start-maximized")
            opts.add_argument("--autoplay-policy=no-user-gesture-required")
            opts.add_argument("--disable-blink-features=AutomationControlled")
            opts.add_experimental_option("detach", True)
            opts.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
            opts.add_experimental_option("useAutomationExtension", False)

            driver = webdriver.Chrome(options=opts)
            wait   = WebDriverWait(driver, 15)

            driver.get(
                f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
            )

            # Click first video
            first = wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "ytd-video-renderer a#video-title")
                )
            )
            url   = first.get_attribute("href")
            title = first.get_attribute("title")
            self._log(f"YouTube → {title}", "system")

            driver.get(url + ("&autoplay=1" if "?" in url else "?autoplay=1"))
            time.sleep(3)

            # Force play via YouTube's internal API
            for _ in range(5):
                state = driver.execute_script("""
                    try {
                        var p = document.getElementById('movie_player');
                        if (p && typeof p.playVideo === 'function') {
                            p.unMute(); p.setVolume(100); p.playVideo();
                            return p.getPlayerState();
                        }
                    } catch(e) {}
                    return -1;
                """)
                if state == 1:
                    self._log("YouTube playing!", "system")
                    break
                time.sleep(1)

        except Exception as e:
            self._log(f"YouTube error: {e}", "error")
            webbrowser.open(
                f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
            )


# ── VOICE COMMAND EXAMPLES ────────────────────────────────────────────
"""
✅ OTT COMMANDS:

"Open Netflix"
"Open Hotstar"
"Open Prime"
"Open JioCinema"
"Open ZEE5"
"Open AHA"

"Play Pushpa on YouTube"
"Play RRR on Netflix"
"Play Kalki on Prime"
"Play KGF on Hotstar"
"Play Family Star on AHA"

"Search for Prabhas movies on Hotstar"
"Search Marvel on Netflix"
"Search Telugu movies on Prime"

"Watch Saaho on Hotstar"
"Watch Money Heist on Netflix"
"""
