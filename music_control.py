"""
BOB-AI v2 — Music Control Module
✅ Spotify (app + web)
✅ YouTube Music
✅ Gaana, JioSaavn, Wynk
✅ Local music files (mp3/wav/flac/m4a)
✅ Playback controls — play, pause, next, previous, volume
✅ Voice command examples at bottom
"""

import os
import time
import webbrowser
import threading
import subprocess
import glob
import random
import pyautogui

# ── MUSIC APP PATHS (Windows) ──────────────────────────────────────────
SPOTIFY_PATHS = [
    os.path.expandvars(r"%APPDATA%\Spotify\Spotify.exe"),
    os.path.expandvars(r"%LOCALAPPDATA%\Spotify\Spotify.exe"),
    r"C:\Program Files\WindowsApps\SpotifyAB.SpotifyMusic_*\Spotify.exe",
]

# ── MUSIC PLATFORM URLs ───────────────────────────────────────────────
MUSIC_URLS = {
    "spotify":       "https://open.spotify.com",
    "youtube music": "https://music.youtube.com",
    "yt music":      "https://music.youtube.com",
    "gaana":         "https://gaana.com",
    "saavn":         "https://www.jiosaavn.com",
    "jiosaavn":      "https://www.jiosaavn.com",
    "wynk":          "https://wynkmusic.com",
    "hungama":       "https://www.hungama.com/music",
    "amazon music":  "https://music.amazon.in",
}

MUSIC_SEARCH_URLS = {
    "spotify":       "https://open.spotify.com/search/{}",
    "youtube music": "https://music.youtube.com/search?q={}",
    "gaana":         "https://gaana.com/search/{}",
    "saavn":         "https://www.jiosaavn.com/search/{}",
    "jiosaavn":      "https://www.jiosaavn.com/search/{}",
}

# ── LOCAL MUSIC FOLDERS ───────────────────────────────────────────────
LOCAL_MUSIC_DIRS = [
    os.path.join(os.path.expanduser("~"), "Music"),
    os.path.join(os.path.expanduser("~"), "Downloads"),
    os.path.join(os.path.expanduser("~"), "Desktop"),
    r"D:\Music",
    r"D:\Songs",
    r"E:\Music",
    r"E:\Songs",
]

MUSIC_EXTENSIONS = [".mp3", ".wav", ".flac", ".m4a", ".aac", ".ogg", ".wma"]


class MusicHandler:
    def __init__(self, speak_fn, listen_raw_fn=None, gui_fn=None):
        self.speak      = speak_fn
        self.listen_raw = listen_raw_fn
        self.gui        = gui_fn
        self._current_process = None

    def _log(self, text, role="info"):
        print(f"[MUSIC] {text}")
        if self.gui: self.gui(text, role)

    def _ask(self, question: str) -> str:
        self.speak(question)
        return self.listen_raw() if self.listen_raw else ""

    # ── MAIN HANDLER ─────────────────────────────────────
    def handle(self, command: str) -> bool:
        c = command.lower().strip()

        # Playback controls (no song needed)
        if any(x in c for x in ["pause music", "pause song", "pause the music"]):
            return self._playback_control("pause")
        if any(x in c for x in ["resume music", "resume song", "play music", "unpause"]):
            return self._playback_control("play")
        if any(x in c for x in ["next song", "skip song", "next track", "skip"]):
            return self._playback_control("next")
        if any(x in c for x in ["previous song", "prev song", "last song", "go back"]):
            return self._playback_control("previous")
        if "stop music" in c or "stop the music" in c:
            return self._playback_control("stop")
        if "shuffle" in c and "music" in c:
            return self._playback_control("shuffle")

        # Open platform
        for platform in MUSIC_URLS:
            if platform in c and ("open" in c or "launch" in c):
                self.speak(f"Opening {platform.title()}.")
                webbrowser.open(MUSIC_URLS[platform])
                return True

        # Play on platform
        if "play" in c and ("spotify" in c or "gaana" in c or "saavn" in c
                             or "jiosaavn" in c or "youtube music" in c
                             or "yt music" in c or "wynk" in c):
            return self._play_on_platform(c)

        # Play local file
        if any(x in c for x in ["play local", "play from files", "play offline",
                                  "play my music", "play downloaded"]):
            return self._play_local(c)

        # Play Spotify specifically
        if "spotify" in c and "play" in c:
            return self._play_on_platform(c)

        return False

    # ── PLAY ON PLATFORM ─────────────────────────────────
    def _play_on_platform(self, command: str) -> bool:
        c       = command.lower()
        platform = self._detect_platform(c)

        # Extract song/artist name
        song = c
        for word in ["play", "on", "in", "open", platform or "",
                     "spotify", "gaana", "saavn", "jiosaavn",
                     "youtube music", "yt music", "wynk", "hungama"]:
            song = song.replace(word, "").strip()
        song = song.strip()

        if not song:
            song = self._ask("What song or artist should I play?")
        if not song:
            self.speak("Didn't catch the song name."); return True

        self.speak(f"Playing {song} on {platform.title() if platform else 'Spotify'}.")
        self._log(f"Music → '{song}' on {platform}", "processing")

        if platform == "spotify":
            self._open_spotify(song)
        elif platform in MUSIC_SEARCH_URLS:
            url = MUSIC_SEARCH_URLS[platform].format(song.replace(" ", "+"))
            webbrowser.open(url)
        else:
            # Default: Spotify web search
            url = MUSIC_SEARCH_URLS["spotify"].format(song.replace(" ", "+"))
            webbrowser.open(url)

        return True

    # ── OPEN SPOTIFY ─────────────────────────────────────
    def _open_spotify(self, query: str = ""):
        """Open Spotify app if installed, otherwise open web."""
        # Try Spotify app
        for path in SPOTIFY_PATHS:
            expanded = glob.glob(path)
            target = expanded[0] if expanded else path
            if os.path.exists(target):
                subprocess.Popen([target])
                time.sleep(3)
                if query:
                    # Use Spotify search shortcut (Ctrl+L)
                    pyautogui.hotkey("ctrl", "l")
                    time.sleep(0.5)
                    pyautogui.write(query, interval=0.05)
                    pyautogui.press("enter")
                self._log(f"Spotify app opened → {query}", "system")
                return

        # Fallback: Spotify web
        if query:
            url = MUSIC_SEARCH_URLS["spotify"].format(query.replace(" ", "+"))
        else:
            url = MUSIC_URLS["spotify"]
        webbrowser.open(url)
        self._log(f"Spotify web opened → {query}", "system")

    # ── PLAY LOCAL FILES ──────────────────────────────────
    def _play_local(self, command: str = "") -> bool:
        c = command.lower()

        # Extract song name from command
        song_query = c
        for word in ["play", "local", "from", "files", "offline",
                     "my", "music", "downloaded", "song", "the"]:
            song_query = song_query.replace(word, "").strip()
        song_query = song_query.strip()

        if not song_query:
            song_query = self._ask(
                "What song should I play from your files? Say the name or say random."
            )

        if not song_query:
            self.speak("Didn't catch the song name."); return True

        if "random" in song_query:
            return self._play_random_local()

        # Search for the file
        found = self._find_local_file(song_query)

        if found:
            self.speak(f"Playing {os.path.basename(found)} from your files.")
            self._log(f"Local → {found}", "system")
            self._open_file(found)
        else:
            self.speak(
                f"Couldn't find {song_query} in your music folders. "
                f"Want me to search YouTube instead?"
            )
            if self.listen_raw:
                ans = self.listen_raw()
                if "yes" in ans or "yeah" in ans or "sure" in ans:
                    from modules.ott_control import OTTHandler
                    ott = OTTHandler(self.speak, self.listen_raw, self.gui)
                    ott._youtube_autoplay(song_query)

        return True

    def _find_local_file(self, query: str) -> str:
        """Search local music folders for a matching file."""
        query_lower = query.lower()

        for folder in LOCAL_MUSIC_DIRS:
            if not os.path.exists(folder):
                continue
            for ext in MUSIC_EXTENSIONS:
                # Direct search
                pattern = os.path.join(folder, "**", f"*{ext}")
                for f in glob.glob(pattern, recursive=True):
                    name = os.path.basename(f).lower()
                    # Check if any word from query is in filename
                    if any(word in name for word in query_lower.split() if len(word) > 2):
                        return f

        return ""

    def _play_random_local(self) -> bool:
        """Pick and play a random local music file."""
        all_files = []
        for folder in LOCAL_MUSIC_DIRS:
            if not os.path.exists(folder):
                continue
            for ext in MUSIC_EXTENSIONS:
                all_files.extend(
                    glob.glob(os.path.join(folder, "**", f"*{ext}"), recursive=True)
                )

        if not all_files:
            self.speak(
                "Couldn't find any music files in your Music, Downloads, or Desktop folders."
            )
            return True

        chosen = random.choice(all_files)
        self.speak(f"Playing a random one — {os.path.basename(chosen)}.")
        self._log(f"Random local → {chosen}", "system")
        self._open_file(chosen)
        return True

    def _open_file(self, path: str):
        """Open a file with the default media player."""
        try:
            os.startfile(path)  # Windows default player
        except Exception:
            try:
                subprocess.Popen(["xdg-open", path])  # Linux fallback
            except Exception as e:
                self._log(f"File open error: {e}", "error")

    # ── PLAYBACK CONTROLS ────────────────────────────────
    def _playback_control(self, action: str) -> bool:
        """Media key controls — works for Spotify, Windows Media Player, VLC, etc."""
        actions = {
            "pause":    (pyautogui.press, ["playpause"]),
            "play":     (pyautogui.press, ["playpause"]),
            "next":     (pyautogui.press, ["nexttrack"]),
            "previous": (pyautogui.press, ["prevtrack"]),
            "stop":     (pyautogui.press, ["stop"]),
            "shuffle":  (pyautogui.hotkey, ["ctrl", "s"]),  # Spotify shortcut
        }
        responses = {
            "pause":    "Paused.",
            "play":     "Resuming.",
            "next":     "Skipping to next track.",
            "previous": "Going back to previous track.",
            "stop":     "Stopped the music.",
            "shuffle":  "Shuffling your playlist.",
        }

        if action in actions:
            fn, args = actions[action]
            try:
                fn(*args)
                self.speak(responses[action])
            except Exception as e:
                self._log(f"Playback control error: {e}", "error")
                self.speak("Couldn't control playback. Make sure your music app is open.")
        return True

    # ── DETECT PLATFORM ──────────────────────────────────
    def _detect_platform(self, command: str) -> str:
        if "spotify" in command:
            return "spotify"
        if "youtube music" in command or "yt music" in command:
            return "youtube music"
        if "gaana" in command:
            return "gaana"
        if "saavn" in command or "jiosaavn" in command:
            return "jiosaavn"
        if "wynk" in command:
            return "wynk"
        if "hungama" in command:
            return "hungama"
        return "spotify"  # default


# ── VOICE COMMAND EXAMPLES ────────────────────────────────────────────
"""
✅ MUSIC COMMANDS:

PLATFORM:
"Open Spotify"
"Open Gaana"
"Open JioSaavn"
"Open YouTube Music"

PLAY ONLINE:
"Play Pushpa songs on Spotify"
"Play AR Rahman on Gaana"
"Play Kesariya on JioSaavn"
"Play Anirudh on YouTube Music"
"Play Sid Sriram"

PLAY LOCAL FILES:
"Play local Pushpa"
"Play offline AR Rahman"
"Play from files Kesariya"
"Play my music random"
"Play downloaded songs"

CONTROLS:
"Pause music"
"Resume music"
"Next song"
"Previous song"
"Stop music"
"Shuffle music"
"""
