"""
╔══════════════════════════════════════════════╗
║         BOB-AI  —  Virtual Assistant         ║
║         Jarvis-Class Desktop Agent           ║
║         Version 1.0  |  By Ganesh            ║
╚══════════════════════════════════════════════╝

HOW TO USE:
  python main.py

Wake word: "Hey Bob" or "Bob"
Then speak your command.
"""

import threading
import sys
from modules.assistant import Assistant
from modules.gui import AssistantGUI
import tkinter as tk
from bob_commands import handle_command


def main():
    root = tk.Tk()
    gui  = AssistantGUI(root)
    bob  = Assistant(gui_callback=gui.update)

    # Run assistant in background thread
    t = threading.Thread(target=bob.run, daemon=True)
    t.start()

    root.mainloop()


if __name__ == "__main__":
    main()
