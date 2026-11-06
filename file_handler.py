"""
BOB-AI v2 — File System Module
✅ Open files and folders by voice
✅ Search for files by name across entire system
✅ Create, delete, rename files/folders
✅ List folder contents
✅ Open recent files
✅ Open in specific apps (VS Code, Notepad, etc.)
✅ Voice command examples at bottom
"""

import os
import glob
import time
import shutil
import subprocess
import datetime
import threading
import pyautogui
import pyperclip
from pathlib import Path


# ── COMMON FOLDER SHORTCUTS ───────────────────────────────────────────
FOLDER_SHORTCUTS = {
    "desktop":    os.path.join(os.path.expanduser("~"), "Desktop"),
    "downloads":  os.path.join(os.path.expanduser("~"), "Downloads"),
    "documents":  os.path.join(os.path.expanduser("~"), "Documents"),
    "pictures":   os.path.join(os.path.expanduser("~"), "Pictures"),
    "music":      os.path.join(os.path.expanduser("~"), "Music"),
    "videos":     os.path.join(os.path.expanduser("~"), "Videos"),
    "d drive":    "D:\\",
    "e drive":    "E:\\",
    "c drive":    "C:\\",
    "projects":   os.path.join(os.path.expanduser("~"), "Documents", "Projects"),
    "bob ai":     os.path.join(os.path.expanduser("~"), "Desktop", "BOB-AI"),
    "quizdom":    os.path.join(os.path.expanduser("~"), "Desktop", "Quizdom"),
}

# ── APP OPENERS ───────────────────────────────────────────────────────
OPEN_WITH = {
    "vscode":    [os.path.expandvars(r"%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe")],
    "vs code":   [os.path.expandvars(r"%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe")],
    "notepad":   ["notepad.exe"],
    "vlc":       [r"C:\Program Files\VideoLAN\VLC\vlc.exe"],
    "word":      [r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE"],
    "excel":     [r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE"],
    "photoshop": [r"C:\Program Files\Adobe\Adobe Photoshop 2024\Photoshop.exe"],
}

# ── SEARCH ROOTS ─────────────────────────────────────────────────────
SEARCH_ROOTS = [
    os.path.expanduser("~"),  # entire user home
    "D:\\",
    "E:\\",
]


class FileHandler:
    def __init__(self, speak_fn, listen_raw_fn=None, gui_fn=None):
        self.speak      = speak_fn
        self.listen_raw = listen_raw_fn
        self.gui        = gui_fn

    def _log(self, text, role="info"):
        print(f"[FILE] {text}")
        if self.gui: self.gui(text, role)

    def _ask(self, question: str) -> str:
        self.speak(question)
        return self.listen_raw() if self.listen_raw else ""

    # ── MAIN HANDLER ─────────────────────────────────────
    def handle(self, command: str) -> bool:
        c = command.lower().strip()

        # Open folder shortcuts
        if any(x in c for x in ["open folder", "go to folder", "show folder",
                                  "open my", "open downloads", "open desktop",
                                  "open documents", "open pictures", "open music",
                                  "open videos", "open d drive", "open e drive",
                                  "open c drive"]):
            return self._open_folder(c)

        # Open specific file
        if any(x in c for x in ["open file", "open the file", "launch file"]):
            return self._open_file_by_name(c)

        # Search for file
        if any(x in c for x in ["find file", "search file", "where is", "locate file",
                                  "find my file", "search for file"]):
            return self._search_file(c)

        # List contents of folder
        if any(x in c for x in ["list files", "show files", "what's in", "whats in",
                                  "list folder", "show folder contents"]):
            return self._list_folder(c)

        # Create new folder
        if any(x in c for x in ["create folder", "make folder", "new folder"]):
            return self._create_folder(c)

        # Create new file
        if any(x in c for x in ["create file", "make file", "new file", "create a file"]):
            return self._create_file(c)

        # Delete file/folder
        if any(x in c for x in ["delete file", "delete folder", "remove file"]):
            return self._delete_item(c)

        # Rename file/folder
        if "rename" in c and ("file" in c or "folder" in c):
            return self._rename_item(c)

        # Open with specific app
        if "open with" in c:
            return self._open_with_app(c)

        # Recent files
        if any(x in c for x in ["recent files", "recently opened", "last opened",
                                  "recently used files"]):
            return self._recent_files()

        # Copy file path
        if "copy path" in c or "copy file path" in c:
            return self._copy_path(c)

        return False

    # ── OPEN FOLDER ──────────────────────────────────────
    def _open_folder(self, command: str) -> bool:
        c = command.lower()

        # Check shortcuts
        for name, path in FOLDER_SHORTCUTS.items():
            if name in c:
                if os.path.exists(path):
                    self.speak(f"Opening {name} folder.")
                    self._log(f"Open folder: {path}", "system")
                    os.startfile(path)
                else:
                    self.speak(f"Couldn't find the {name} folder on this device.")
                return True

        # Ask if not found
        folder = self._ask("Which folder should I open?")
        if folder:
            for name, path in FOLDER_SHORTCUTS.items():
                if name in folder.lower():
                    if os.path.exists(path):
                        os.startfile(path)
                        self.speak(f"Opening {name}.")
                    return True

        self.speak("Couldn't find that folder.")
        return True

    # ── OPEN FILE BY NAME ────────────────────────────────
    def _open_file_by_name(self, command: str) -> bool:
        c = command.lower()

        # Extract filename
        name = c
        for word in ["open", "file", "the", "launch", "my"]:
            name = name.replace(word, "").strip()
        name = name.strip()

        if not name:
            name = self._ask("What's the file name?")
        if not name:
            self.speak("Didn't get the file name."); return True

        self.speak(f"Searching for {name}, give me a moment.")
        self._log(f"Searching file: {name}", "processing")

        found = self._find_file(name)

        if found:
            self.speak(f"Found it — opening {os.path.basename(found)}.")
            self._log(f"Opening: {found}", "system")
            os.startfile(found)
        else:
            self.speak(f"Couldn't find a file named {name} on your system.")
        return True

    # ── SEARCH FILE ──────────────────────────────────────
    def _search_file(self, command: str) -> bool:
        c = command.lower()

        name = c
        for word in ["find", "search", "file", "where", "is", "locate", "my", "for"]:
            name = name.replace(word, "").strip()
        name = name.strip()

        if not name:
            name = self._ask("What file should I search for?")
        if not name:
            self.speak("Didn't get the file name."); return True

        self.speak(f"Searching for {name} on your system.")
        results = self._find_all_files(name, max_results=5)

        if results:
            self.speak(f"Found {len(results)} file(s) named {name}.")
            for i, r in enumerate(results, 1):
                self._log(f"{i}. {r}", "info")
                self.speak(f"{i}. {os.path.basename(r)} in {os.path.dirname(r)}")
            if len(results) == 1:
                self.speak("Should I open it?")
                if self.listen_raw:
                    ans = self.listen_raw()
                    if "yes" in ans or "yeah" in ans or "sure" in ans or "open" in ans:
                        os.startfile(results[0])
                        self.speak("Opened!")
        else:
            self.speak(f"No file named {name} found on your system.")
        return True

    # ── LIST FOLDER CONTENTS ─────────────────────────────
    def _list_folder(self, command: str) -> bool:
        c = command.lower()

        folder_path = None
        for name, path in FOLDER_SHORTCUTS.items():
            if name in c:
                folder_path = path; break

        if not folder_path:
            folder_name = self._ask("Which folder should I list?")
            if folder_name:
                for name, path in FOLDER_SHORTCUTS.items():
                    if name in folder_name.lower():
                        folder_path = path; break

        if not folder_path or not os.path.exists(folder_path):
            self.speak("Couldn't find that folder."); return True

        try:
            items = os.listdir(folder_path)
            files = [i for i in items if os.path.isfile(os.path.join(folder_path, i))]
            dirs  = [i for i in items if os.path.isdir(os.path.join(folder_path, i))]

            self.speak(
                f"Found {len(files)} file(s) and {len(dirs)} folder(s). "
                f"Opening in File Explorer."
            )
            os.startfile(folder_path)
            self._log(f"Folder contents of: {folder_path}", "info")
            for item in items[:10]:
                self._log(f"  → {item}", "info")
        except Exception as e:
            self.speak(f"Couldn't list that folder.")
        return True

    # ── CREATE FOLDER ────────────────────────────────────
    def _create_folder(self, command: str) -> bool:
        c = command.lower()

        name = c
        for word in ["create", "make", "new", "folder", "a", "called", "named"]:
            name = name.replace(word, "").strip()
        name = name.strip()

        if not name:
            name = self._ask("What should I name the new folder?")
        if not name:
            self.speak("Didn't get a name."); return True

        # Default location: Desktop
        location = os.path.join(os.path.expanduser("~"), "Desktop", name)

        try:
            os.makedirs(location, exist_ok=True)
            self.speak(f"Created folder {name} on your Desktop.")
            self._log(f"Created folder: {location}", "system")
            os.startfile(os.path.dirname(location))
        except Exception as e:
            self.speak(f"Couldn't create the folder. {e}")
        return True

    # ── CREATE FILE ──────────────────────────────────────
    def _create_file(self, command: str) -> bool:
        c = command.lower()

        name = c
        for word in ["create", "make", "new", "file", "a", "called", "named", "the"]:
            name = name.replace(word, "").strip()
        name = name.strip()

        if not name:
            name = self._ask("What should I name the new file?")
        if not name:
            self.speak("Didn't get a name."); return True

        # Add .txt extension if no extension given
        if "." not in name:
            name += ".txt"

        location = os.path.join(os.path.expanduser("~"), "Desktop", name)

        try:
            with open(location, "w") as f:
                f.write(f"# Created by BOB AI on {datetime.datetime.now()}\n")
            self.speak(f"Created {name} on your Desktop and opening it.")
            self._log(f"Created file: {location}", "system")
            os.startfile(location)
        except Exception as e:
            self.speak(f"Couldn't create the file. {e}")
        return True

    # ── DELETE ITEM ──────────────────────────────────────
    def _delete_item(self, command: str) -> bool:
        c = command.lower()

        name = c
        for word in ["delete", "remove", "file", "folder", "the", "my"]:
            name = name.replace(word, "").strip()
        name = name.strip()

        if not name:
            name = self._ask("What file or folder should I delete?")
        if not name:
            self.speak("Didn't get the name."); return True

        found = self._find_file(name) or self._find_folder(name)

        if not found:
            self.speak(f"Couldn't find {name} to delete."); return True

        self.speak(f"Found {os.path.basename(found)}. Are you sure you want to delete it?")
        if self.listen_raw:
            confirm = self.listen_raw()
            if "yes" in confirm or "delete" in confirm or "sure" in confirm:
                try:
                    if os.path.isfile(found):
                        os.remove(found)
                    else:
                        shutil.rmtree(found)
                    self.speak(f"Deleted {os.path.basename(found)}.")
                    self._log(f"Deleted: {found}", "system")
                except Exception as e:
                    self.speak(f"Couldn't delete it. {e}")
            else:
                self.speak("Okay, cancelled the deletion.")
        return True

    # ── RENAME ITEM ──────────────────────────────────────
    def _rename_item(self, command: str) -> bool:
        # Extract old and new name
        c = command.lower()

        old_name = self._ask("What's the current file or folder name?")
        if not old_name:
            self.speak("Didn't get the name."); return True

        new_name = self._ask(f"What should I rename {old_name} to?")
        if not new_name:
            self.speak("Didn't get the new name."); return True

        found = self._find_file(old_name) or self._find_folder(old_name)

        if not found:
            self.speak(f"Couldn't find {old_name}."); return True

        try:
            parent   = os.path.dirname(found)
            ext      = os.path.splitext(found)[1]
            new_path = os.path.join(parent, new_name + (ext if "." not in new_name else ""))
            os.rename(found, new_path)
            self.speak(f"Renamed to {new_name}.")
            self._log(f"Renamed: {found} → {new_path}", "system")
        except Exception as e:
            self.speak(f"Couldn't rename it. {e}")
        return True

    # ── OPEN WITH APP ────────────────────────────────────
    def _open_with_app(self, command: str) -> bool:
        c = command.lower()

        app_name = None
        for app in OPEN_WITH:
            if app in c:
                app_name = app; break

        if not app_name:
            app_name = self._ask("Which app — VS Code, Notepad, VLC, Word, Excel?")
            if not app_name:
                self.speak("Didn't get the app name."); return True
            app_name = app_name.lower().strip()

        file_part = c.replace("open with", "").replace(app_name, "").strip()
        file_part = file_part.replace("using", "").replace("in", "").strip()

        if not file_part:
            file_part = self._ask("Which file should I open?")
        if not file_part:
            self.speak("Didn't get the file name."); return True

        found = self._find_file(file_part)
        if not found:
            self.speak(f"Couldn't find {file_part}."); return True

        app_paths = OPEN_WITH.get(app_name, [])
        for app_path in app_paths:
            if os.path.exists(app_path):
                subprocess.Popen([app_path, found])
                self.speak(f"Opening {os.path.basename(found)} in {app_name.title()}.")
                return True

        # Fallback
        os.startfile(found)
        self.speak(f"Opened {os.path.basename(found)}.")
        return True

    # ── RECENT FILES ─────────────────────────────────────
    def _recent_files(self) -> bool:
        recent_path = os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Recent")
        try:
            files = sorted(
                [os.path.join(recent_path, f) for f in os.listdir(recent_path)],
                key=os.path.getmtime, reverse=True
            )[:5]

            self.speak(f"Here are your 5 most recent files:")
            for i, f in enumerate(files, 1):
                name = os.path.basename(f).replace(".lnk", "")
                self._log(f"{i}. {name}", "info")
                self.speak(f"{i}. {name}")

            os.startfile(recent_path)
        except Exception as e:
            self.speak("Couldn't access recent files.")
        return True

    # ── COPY FILE PATH ───────────────────────────────────
    def _copy_path(self, command: str) -> bool:
        c = command.lower()

        name = c.replace("copy", "").replace("path", "").replace("file", "").strip()
        if not name:
            name = self._ask("Which file's path should I copy?")
        if not name:
            self.speak("Didn't get the file name."); return True

        found = self._find_file(name)
        if found:
            pyperclip.copy(found)
            self.speak(f"Copied path of {os.path.basename(found)} to clipboard.")
        else:
            self.speak(f"Couldn't find {name}.")
        return True

    # ── FILE SEARCH HELPERS ──────────────────────────────
    def _find_file(self, query: str) -> str:
        """Find first matching file."""
        results = self._find_all_files(query, max_results=1)
        return results[0] if results else ""

    def _find_folder(self, query: str) -> str:
        """Find first matching folder."""
        query_lower = query.lower()
        for root in SEARCH_ROOTS:
            if not os.path.exists(root):
                continue
            try:
                for item in os.scandir(root):
                    if item.is_dir() and query_lower in item.name.lower():
                        return item.path
                # Deeper search in user home
                if root == os.path.expanduser("~"):
                    for dirpath, dirnames, _ in os.walk(root):
                        for d in dirnames:
                            if query_lower in d.lower():
                                return os.path.join(dirpath, d)
            except PermissionError:
                continue
        return ""

    def _find_all_files(self, query: str, max_results: int = 5) -> list:
        """Search system for files matching query."""
        query_lower = query.lower()
        results     = []

        # Common folders first (faster)
        priority_dirs = [
            os.path.join(os.path.expanduser("~"), "Desktop"),
            os.path.join(os.path.expanduser("~"), "Downloads"),
            os.path.join(os.path.expanduser("~"), "Documents"),
            os.path.join(os.path.expanduser("~"), "Music"),
            os.path.join(os.path.expanduser("~"), "Pictures"),
            os.path.join(os.path.expanduser("~"), "Videos"),
        ]

        for folder in priority_dirs:
            if not os.path.exists(folder):
                continue
            for f in glob.glob(os.path.join(folder, "**", f"*{query_lower}*"), recursive=True):
                if os.path.isfile(f):
                    results.append(f)
                    if len(results) >= max_results:
                        return results

        # Deeper search if not found
        if not results:
            for root in SEARCH_ROOTS:
                if not os.path.exists(root):
                    continue
                try:
                    for dirpath, _, filenames in os.walk(root):
                        for filename in filenames:
                            if query_lower in filename.lower():
                                results.append(os.path.join(dirpath, filename))
                                if len(results) >= max_results:
                                    return results
                except PermissionError:
                    continue

        return results


# ── VOICE COMMAND EXAMPLES ────────────────────────────────────────────────
"""
✅ FILE COMMANDS:

OPEN FOLDERS:
"Open Desktop"
"Open Downloads"
"Open Documents"
"Open D drive"
"Open my Music folder"

OPEN FILES:
"Open file resume"
"Open file assignment"
"Launch file bob ai"

FIND FILES:
"Find file Quizdom"
"Search for resume.docx"
"Where is my project file"
"Locate assignment"

LIST CONTENTS:
"List files in Downloads"
"What's in my Desktop"
"Show folder contents of Documents"

CREATE:
"Create folder College Projects"
"Create file notes"
"Make new folder Assignments"
"New file todo.txt"

DELETE:
"Delete file old notes"
"Delete folder temp"

RENAME:
"Rename file assignment"  → BOB asks old and new name

OPEN WITH:
"Open with VS Code project"
"Open with Notepad readme"
"Open with VLC movie"

RECENT:
"Show recent files"
"Recently opened files"
"""
