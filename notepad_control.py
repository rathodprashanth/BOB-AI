"""
notepad_control.py
==================
BOB AI (Jarvis) - Notepad Control Module
Controls Notepad / WordPad via pyautogui + pyperclip.

Requirements:
    python -m pip install pyautogui pyperclip

Usage in BOB AI:
    from notepad_control import handle_notepad_command
    handle_notepad_command("bold")
    handle_notepad_command("type Hello World")
    handle_notepad_command("backspace 3")
"""

import time
import pyautogui
import pyperclip

# ──────────────────────────────────────────────
#  HELPER
# ──────────────────────────────────────────────

def _pause(sec=0.15):
    time.sleep(sec)


def _get_clipboard_text():
    """Copy all text and return it."""
    pyautogui.hotkey('ctrl', 'a')
    _pause()
    pyautogui.hotkey('ctrl', 'c')
    _pause()
    return pyperclip.paste()


def _replace_all_text(new_text):
    """Replace entire document content."""
    pyautogui.hotkey('ctrl', 'a')
    _pause()
    pyperclip.copy(new_text)
    pyautogui.hotkey('ctrl', 'v')
    _pause()


# ──────────────────────────────────────────────
#  TYPING
# ──────────────────────────────────────────────

def type_text(text: str, interval: float = 0.04):
    """Type text as-is."""
    pyautogui.write(text, interval=interval)

def type_upper(text: str):
    """Type text in UPPERCASE."""
    pyautogui.write(text.upper(), interval=0.04)

def type_lower(text: str):
    """Type text in lowercase."""
    pyautogui.write(text.lower(), interval=0.04)

def type_title(text: str):
    """Type text in Title Case."""
    pyautogui.write(text.title(), interval=0.04)

def type_sentence(text: str):
    """Type text in Sentence case."""
    pyautogui.write(text.capitalize(), interval=0.04)


# ──────────────────────────────────────────────
#  BASIC KEYS
# ──────────────────────────────────────────────

def backspace(n: int = 1):
    pyautogui.press('backspace', presses=n, interval=0.05)

def delete_key(n: int = 1):
    pyautogui.press('delete', presses=n, interval=0.05)

def space(n: int = 1):
    pyautogui.press('space', presses=n, interval=0.05)

def enter(n: int = 1):
    pyautogui.press('enter', presses=n, interval=0.05)

def tab(n: int = 1):
    pyautogui.press('tab', presses=n, interval=0.05)

def escape():
    pyautogui.press('escape')


# ──────────────────────────────────────────────
#  NAVIGATION
# ──────────────────────────────────────────────

def go_home():
    pyautogui.press('home')

def go_end():
    pyautogui.press('end')

def go_top():
    pyautogui.hotkey('ctrl', 'home')

def go_bottom():
    pyautogui.hotkey('ctrl', 'end')

def move_left(n: int = 1):
    pyautogui.press('left', presses=n, interval=0.05)

def move_right(n: int = 1):
    pyautogui.press('right', presses=n, interval=0.05)

def move_up(n: int = 1):
    pyautogui.press('up', presses=n, interval=0.05)

def move_down(n: int = 1):
    pyautogui.press('down', presses=n, interval=0.05)

def next_word():
    pyautogui.hotkey('ctrl', 'right')

def prev_word():
    pyautogui.hotkey('ctrl', 'left')


# ──────────────────────────────────────────────
#  SELECTION
# ──────────────────────────────────────────────

def select_all():
    pyautogui.hotkey('ctrl', 'a')

def select_word():
    """Double-click trick to select current word via keyboard."""
    pyautogui.hotkey('ctrl', 'shift', 'right')

def select_line():
    go_home()
    _pause(0.1)
    pyautogui.hotkey('shift', 'end')

def select_to_end():
    pyautogui.hotkey('shift', 'ctrl', 'end')

def select_to_top():
    pyautogui.hotkey('shift', 'ctrl', 'home')


# ──────────────────────────────────────────────
#  CLIPBOARD
# ──────────────────────────────────────────────

def copy():
    pyautogui.hotkey('ctrl', 'c')

def paste():
    pyautogui.hotkey('ctrl', 'v')

def cut():
    pyautogui.hotkey('ctrl', 'x')

def paste_text(text: str):
    """Set clipboard to text and paste it."""
    pyperclip.copy(text)
    _pause(0.1)
    pyautogui.hotkey('ctrl', 'v')


# ──────────────────────────────────────────────
#  FORMATTING  (WordPad / Notepad++ only)
#  Plain Notepad does NOT support these.
# ──────────────────────────────────────────────

def bold():
    pyautogui.hotkey('ctrl', 'b')

def italic():
    pyautogui.hotkey('ctrl', 'i')

def underline():
    pyautogui.hotkey('ctrl', 'u')

def strikethrough():
    """Notepad++ shortcut."""
    pyautogui.hotkey('ctrl', 'shift', 'k')

def align_left():
    pyautogui.hotkey('ctrl', 'l')

def align_center():
    pyautogui.hotkey('ctrl', 'e')

def align_right():
    pyautogui.hotkey('ctrl', 'r')

def justify():
    pyautogui.hotkey('ctrl', 'j')

def increase_font():
    pyautogui.hotkey('ctrl', ']')

def decrease_font():
    pyautogui.hotkey('ctrl', '[')


# ──────────────────────────────────────────────
#  UNDO / REDO
# ──────────────────────────────────────────────

def undo(n: int = 1):
    for _ in range(n):
        pyautogui.hotkey('ctrl', 'z')
        _pause(0.1)

def redo(n: int = 1):
    for _ in range(n):
        pyautogui.hotkey('ctrl', 'y')
        _pause(0.1)


# ──────────────────────────────────────────────
#  CASE CONVERSION (operates on full document)
# ──────────────────────────────────────────────

def convert_uppercase():
    text = _get_clipboard_text() or _get_all()
    _replace_all_text(text.upper())

def convert_lowercase():
    text = _get_all()
    _replace_all_text(text.lower())

def convert_titlecase():
    text = _get_all()
    _replace_all_text(text.title())

def convert_sentencecase():
    text = _get_all()
    _replace_all_text(text.capitalize())

def convert_togglecase():
    text = _get_all()
    _replace_all_text(text.swapcase())

def _get_all():
    pyautogui.hotkey('ctrl', 'a')
    _pause()
    pyautogui.hotkey('ctrl', 'c')
    _pause()
    return pyperclip.paste()


# ──────────────────────────────────────────────
#  FIND & REPLACE
# ──────────────────────────────────────────────

def open_find():
    pyautogui.hotkey('ctrl', 'f')

def open_replace():
    pyautogui.hotkey('ctrl', 'h')

def find_next():
    pyautogui.press('f3')

def find_prev():
    pyautogui.hotkey('shift', 'f3')


# ──────────────────────────────────────────────
#  FILE OPERATIONS
# ──────────────────────────────────────────────

def save():
    pyautogui.hotkey('ctrl', 's')

def save_as():
    pyautogui.hotkey('ctrl', 'shift', 's')

def open_file():
    pyautogui.hotkey('ctrl', 'o')

def new_file():
    pyautogui.hotkey('ctrl', 'n')

def print_doc():
    pyautogui.hotkey('ctrl', 'p')

def close_file():
    pyautogui.hotkey('ctrl', 'w')


# ──────────────────────────────────────────────
#  ZOOM
# ──────────────────────────────────────────────

def zoom_in():
    pyautogui.hotkey('ctrl', '+')

def zoom_out():
    pyautogui.hotkey('ctrl', '-')

def zoom_reset():
    pyautogui.hotkey('ctrl', '0')


# ──────────────────────────────────────────────
#  INSERT HELPERS
# ──────────────────────────────────────────────

def insert_date_time():
    """Insert current date & time (Notepad built-in shortcut)."""
    pyautogui.press('f5')

def insert_bullet():
    paste_text("• ")

def insert_separator():
    paste_text("\n" + "─" * 40 + "\n")


# ──────────────────────────────────────────────
#  BOB AI VOICE COMMAND HANDLER
# ──────────────────────────────────────────────

def handle_notepad_command(command: str) -> str:
    """
    Parse a voice/text command from BOB AI and run
    the matching notepad function.

    Returns a status string for TTS feedback.
    """
    cmd = command.strip().lower()

    # ── Typing ────────────────────────────────
    if cmd.startswith("type "):
        text = command[5:]
        type_text(text)
        return f"Typed: {text}"

    elif cmd.startswith("type upper "):
        type_upper(command[11:])
        return "Typed in uppercase"

    elif cmd.startswith("type lower "):
        type_lower(command[11:])
        return "Typed in lowercase"

    elif cmd.startswith("type title "):
        type_title(command[11:])
        return "Typed in title case"

    elif cmd.startswith("type sentence "):
        type_sentence(command[14:])
        return "Typed in sentence case"

    # ── Basic Keys ────────────────────────────
    elif "backspace" in cmd:
        n = _extract_number(cmd)
        backspace(n)
        return f"Backspaced {n} time(s)"

    elif "delete" in cmd:
        n = _extract_number(cmd)
        delete_key(n)
        return f"Deleted {n} character(s)"

    elif cmd in ("space", "add space"):
        n = _extract_number(cmd)
        space(n)
        return "Space added"

    elif "new line" in cmd or cmd == "enter":
        enter()
        return "New line"

    elif "tab" in cmd:
        tab()
        return "Tab added"

    # ── Navigation ────────────────────────────
    elif "go to top" in cmd or "beginning" in cmd:
        go_top()
        return "Moved to top"

    elif "go to bottom" in cmd or "end of document" in cmd:
        go_bottom()
        return "Moved to bottom"

    elif "go to end" in cmd:
        go_end()
        return "Moved to end of line"

    elif "go to home" in cmd or "start of line" in cmd:
        go_home()
        return "Moved to start of line"

    elif "next word" in cmd:
        next_word()
        return "Moved to next word"

    elif "previous word" in cmd or "prev word" in cmd:
        prev_word()
        return "Moved to previous word"

    # ── Formatting ────────────────────────────
    elif "bold" in cmd:
        bold()
        return "Bold toggled"

    elif "italic" in cmd:
        italic()
        return "Italic toggled"

    elif "underline" in cmd:
        underline()
        return "Underline toggled"

    elif "strikethrough" in cmd or "strike" in cmd:
        strikethrough()
        return "Strikethrough toggled"

    elif "align left" in cmd:
        align_left()
        return "Aligned left"

    elif "align center" in cmd or "centre" in cmd:
        align_center()
        return "Aligned center"

    elif "align right" in cmd:
        align_right()
        return "Aligned right"

    elif "justify" in cmd:
        justify()
        return "Justified"

    elif "increase font" in cmd or "font bigger" in cmd:
        increase_font()
        return "Font increased"

    elif "decrease font" in cmd or "font smaller" in cmd:
        decrease_font()
        return "Font decreased"

    # ── Case Conversion ───────────────────────
    elif "uppercase" in cmd or "all caps" in cmd:
        convert_uppercase()
        return "Converted to uppercase"

    elif "lowercase" in cmd or "all lower" in cmd:
        convert_lowercase()
        return "Converted to lowercase"

    elif "title case" in cmd:
        convert_titlecase()
        return "Converted to title case"

    elif "sentence case" in cmd:
        convert_sentencecase()
        return "Converted to sentence case"

    elif "toggle case" in cmd or "swap case" in cmd:
        convert_togglecase()
        return "Case toggled"

    # ── Clipboard ─────────────────────────────
    elif "select all" in cmd:
        select_all()
        return "All text selected"

    elif "copy" in cmd:
        copy()
        return "Copied to clipboard"

    elif "paste" in cmd:
        paste()
        return "Pasted from clipboard"

    elif "cut" in cmd:
        cut()
        return "Cut to clipboard"

    # ── Undo / Redo ───────────────────────────
    elif "undo" in cmd:
        n = _extract_number(cmd)
        undo(n)
        return f"Undone {n} time(s)"

    elif "redo" in cmd:
        n = _extract_number(cmd)
        redo(n)
        return f"Redone {n} time(s)"

    # ── Find & Replace ────────────────────────
    elif "find" in cmd:
        open_find()
        return "Find dialog opened"

    elif "replace" in cmd:
        open_replace()
        return "Replace dialog opened"

    # ── File Ops ──────────────────────────────
    elif "save as" in cmd:
        save_as()
        return "Save As dialog opened"

    elif "save" in cmd:
        save()
        return "File saved"

    elif "open file" in cmd or "open document" in cmd:
        open_file()
        return "Open dialog launched"

    elif "new file" in cmd or "new document" in cmd:
        new_file()
        return "New file created"

    elif "print" in cmd:
        print_doc()
        return "Print dialog opened"

    # ── Zoom ──────────────────────────────────
    elif "zoom in" in cmd:
        zoom_in()
        return "Zoomed in"

    elif "zoom out" in cmd:
        zoom_out()
        return "Zoomed out"

    elif "zoom reset" in cmd or "reset zoom" in cmd:
        zoom_reset()
        return "Zoom reset"

    # ── Insert Helpers ────────────────────────
    elif "date" in cmd or "time" in cmd:
        insert_date_time()
        return "Date and time inserted"

    elif "bullet" in cmd:
        insert_bullet()
        return "Bullet point inserted"

    elif "separator" in cmd or "divider" in cmd:
        insert_separator()
        return "Separator inserted"

    else:
        return f"Sorry, I didn't understand the notepad command: '{command}'"


# ──────────────────────────────────────────────
#  UTILITY
# ──────────────────────────────────────────────

def _extract_number(text: str, default: int = 1) -> int:
    """Extract the first number found in a string."""
    import re
    nums = re.findall(r'\d+', text)
    return int(nums[0]) if nums else default


# ──────────────────────────────────────────────
#  QUICK TEST (run directly to test)
# ──────────────────────────────────────────────

if __name__ == "__main__":
    print("BOB AI Notepad Control - Test Mode")
    print("Open Notepad, click inside it, then press Enter here.")
    input("Ready? Press Enter...")
    time.sleep(1)

    # Demo sequence
    cmds = [
        "type Hello from BOB AI!",
        "enter",
        "type this is sentence case",
        "sentence case",
        "enter",
        "type bold text here",
        "bold",
        "select all",
        "bold",          # toggle off
        "save",
    ]

    for c in cmds:
        result = handle_notepad_command(c)
        print(f"CMD: {c!r:40s} → {result}")
        time.sleep(0.5)
