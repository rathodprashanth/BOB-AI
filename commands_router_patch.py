"""
BOB-AI v2 — Command Handler (UPDATED ROUTER)
Add this block to your existing modules/commands.py __init__ and handle() method.
Replace the existing __init__ and handle() with these.
"""

# ── ADD THESE IMPORTS at top of your commands.py ─────────────────────
# from modules.ott_control import OTTHandler
# from modules.music_control import MusicHandler
# from modules.file_handler import FileHandler


# ── REPLACE __init__ with this ───────────────────────────────────────
"""
def __init__(self, speak_fn, listen_raw_fn=None, gui_fn=None):
    self.speak      = speak_fn
    self.listen_raw = listen_raw_fn
    self.gui        = gui_fn
    self._wa_driver = None

    # New modules
    self.ott   = OTTHandler(speak_fn, listen_raw_fn, gui_fn)
    self.music = MusicHandler(speak_fn, listen_raw_fn, gui_fn)
    self.files = FileHandler(speak_fn, listen_raw_fn, gui_fn)
"""


# ── ADD THIS BLOCK inside handle() BEFORE the existing YouTube block ──
"""
# ── OTT Platforms ── caught BEFORE Gemini ─────────────────
if any(x in c for x in [
    "netflix", "hotstar", "prime video", "jiocinema", "jio cinema",
    "zee5", "sonyliv", "sony liv", "aha video", "aha", "voot",
    "mx player", "mxplayer", "sun nxt",
    "watch", "stream"
]):
    handled = self.ott.handle(c)
    if handled: return True

# ── Music ── caught BEFORE Gemini ─────────────────────────
if any(x in c for x in [
    "play on spotify", "play on gaana", "play on saavn",
    "play on jiosaavn", "play on youtube music", "play on yt music",
    "open spotify", "open gaana", "open saavn", "open jiosaavn",
    "open wynk", "open youtube music",
    "play local", "play offline", "play downloaded", "play from files",
    "play my music",
    "pause music", "pause song",
    "resume music", "next song", "previous song",
    "skip song", "stop music", "shuffle music",
]):
    handled = self.music.handle(c)
    if handled: return True

# ── File System ── caught BEFORE Gemini ───────────────────
if any(x in c for x in [
    "open folder", "open desktop", "open downloads",
    "open documents", "open pictures", "open music folder",
    "open videos", "open d drive", "open e drive", "open c drive",
    "open file", "find file", "search file", "locate file",
    "list files", "show files", "whats in", "what's in",
    "create folder", "make folder", "new folder",
    "create file", "make file", "new file",
    "delete file", "delete folder", "remove file",
    "rename file", "rename folder",
    "open with vs code", "open with notepad", "open with vlc",
    "recent files", "recently opened",
    "copy path", "copy file path",
]):
    handled = self.files.handle(c)
    if handled: return True
"""
