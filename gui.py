"""
BOB-AI v1 Upgraded — Sci-Fi GUI with Unique Boot Animation
"""

import tkinter as tk
import threading, time, math

C = {
    "bg":"#050a12","panel":"#0b1220","border":"#1a3a5c",
    "accent":"#00d4ff","accent2":"#00ffaa","danger":"#ff4466",
    "warn":"#ffaa00","text":"#c8e0f4","muted":"#4a6a8a",
    "bob":"#00ffaa","user":"#0088cc","error":"#ff4466",
    "system":"#888899","listening":"#00d4ff","idle":"#1a3a5c",
    "processing":"#ffaa00",
}

ROLE_PREFIX = {
    "bob":"BOB","user":"YOU","system":"SYS","error":"ERR",
    "listening":"MIC","idle":"---","info":"INF","processing":"...",
}

BOOT_MSGS = [
    "INITIALIZING BOB-AI...",
    "LOADING VOICE ENGINE...",
    "CONNECTING GEMINI AI...",
    "LOADING AUTOMATION...",
    "CALIBRATING MIC...",
    "ALL SYSTEMS ONLINE ✓",
]


class AssistantGUI:
    def __init__(self, root: tk.Tk):
        self.root    = root
        self.booting = True
        self._setup_window()
        self._boot_angle    = 0
        self._boot_progress = 0.0
        self._boot_msg_idx  = 0
        self._show_boot()

    # ── WINDOW ────────────────────────────────────────────
    def _setup_window(self):
        self.root.title("BOB-AI v1 Upgraded")
        self.root.configure(bg=C["bg"])
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha",   0.96)
        self.root.resizable(False, False)
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry(f"480x580+{sw-500}+{sh-620}")

    # ── BOOT ANIMATION ────────────────────────────────────
    def _show_boot(self):
        self.boot_frame = tk.Frame(self.root, bg=C["bg"])
        self.boot_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.boot_canvas = tk.Canvas(
            self.boot_frame, width=480, height=580,
            bg=C["bg"], highlightthickness=0
        )
        self.boot_canvas.pack()
        self._animate_boot()

    def _animate_boot(self):
        cv = self.boot_canvas
        cv.delete("all")
        cx, cy = 240, 265

        # Outer rotating rings
        for i in range(4):
            r  = 70 + i * 28
            a0 = math.radians(self._boot_angle * (1 + i * 0.25))
            a1 = a0 + math.pi * 1.4
            x0, y0 = cx + math.cos(a0) * r, cy + math.sin(a0) * r
            # arc approximation with line
            pts = []
            steps = 40
            for s in range(steps + 1):
                ang = a0 + (a1 - a0) * s / steps
                pts += [cx + math.cos(ang) * r, cy + math.sin(ang) * r]
            opacity = [22, 44, 66, 88][i]
            col = f"#{opacity:02x}d4ff" if i < 3 else "#00ffaa"
            try:
                cv.create_line(*pts, fill=C["accent"] if i < 3 else C["accent2"],
                               width=1 + i * 0.4, smooth=True)
            except:
                pass
            # dot at tip
            cv.create_oval(x0-4, y0-4, x0+4, y0+4, fill=C["accent"], outline="")

        # Pulsing inner orb
        pulse = abs(math.sin(math.radians(self._boot_angle * 2))) * 10
        r = 52 + pulse
        cv.create_oval(cx-r, cy-r, cx+r, cy+r,
                       fill="#001833", outline=C["accent"], width=2)
        cv.create_oval(cx-r+8, cy-r+8, cx+r-8, cy+r-8,
                       fill="#002a44", outline=C["accent2"], width=1)

        # Inner scan line
        scan_y = cy - 30 + (int(self._boot_angle * 0.8) % 60)
        cv.create_line(cx - r + 12, scan_y, cx + r - 12, scan_y,
                       fill="#003344", width=2)

        # BOB text
        cv.create_text(cx, cy - 8, text="BOB",
                       fill=C["accent"], font=("Courier New", 16, "bold"))
        cv.create_text(cx, cy + 12, text="AI",
                       fill=C["accent2"], font=("Courier New", 9, "bold"))

        # Title block
        cv.create_text(cx, 62, text="BOB-AI",
                       fill=C["accent"], font=("Courier New", 26, "bold"))
        cv.create_text(cx, 90, text="JARVIS-CLASS VIRTUAL ASSISTANT",
                       fill=C["muted"], font=("Courier New", 8))
        cv.create_text(cx, 106, text="v1.0  |  by Venkat Sai Ganesh",
                       fill="#2a4a6a", font=("Courier New", 7))

        # Boot message
        idx = min(self._boot_msg_idx, len(BOOT_MSGS) - 1)
        cv.create_text(cx, 390, text=BOOT_MSGS[idx],
                       fill=C["accent"], font=("Courier New", 9, "bold"))

        # Progress bar
        bx, by, bw = cx - 160, 415, 320
        cv.create_rectangle(bx, by, bx + bw, by + 7,
                            fill="#0a1a2a", outline=C["border"])
        filled = int(bw * self._boot_progress / 100)
        if filled > 0:
            cv.create_rectangle(bx, by, bx + filled, by + 7,
                                fill=C["accent"], outline="")
        cv.create_text(cx, by + 18,
                       text=f"{int(self._boot_progress)}%",
                       fill=C["muted"], font=("Courier New", 8))

        # Corner brackets
        for x1,y1,x2,y2 in [
            (8,8,40,8),(8,8,8,40),(440,8,472,8),(472,8,472,40),
            (8,540,40,540),(8,540,8,572),(440,540,472,540),(472,540,472,572)
        ]:
            cv.create_line(x1,y1,x2,y2, fill=C["border"], width=1)

        # ── Advance state ──
        self._boot_angle    += 2.8
        self._boot_progress  = min(100.0, self._boot_progress + 1.1)

        step = int(self._boot_progress / (100 / max(len(BOOT_MSGS), 1)))
        if step < len(BOOT_MSGS):
            self._boot_msg_idx = step

        if self._boot_progress < 100:
            self.root.after(28, self._animate_boot)
        else:
            self.root.after(700, self._finish_boot)

    def _finish_boot(self):
        self.boot_frame.destroy()
        self.booting = False
        self._build_ui()

    # ── MAIN UI ───────────────────────────────────────────
    def _build_ui(self):
        # Header
        hdr = tk.Frame(self.root, bg=C["panel"], pady=9)
        hdr.pack(fill="x")

        self.orb = tk.Canvas(hdr, width=40, height=40,
                              bg=C["panel"], highlightthickness=0)
        self.orb.pack(side="left", padx=(13, 8))
        self._draw_orb(C["accent"])

        info = tk.Frame(hdr, bg=C["panel"])
        info.pack(side="left")
        tk.Label(info, text="BOB-AI", bg=C["panel"], fg=C["accent"],
                 font=("Courier New", 14, "bold")).pack(anchor="w")
        tk.Label(info, text="JARVIS-CLASS ASSISTANT  v1.0 UPGRADED",
                 bg=C["panel"], fg=C["muted"],
                 font=("Courier New", 6)).pack(anchor="w")

        right = tk.Frame(hdr, bg=C["panel"])
        right.pack(side="right", padx=13)
        self.status_var = tk.StringVar(value="● IDLE")
        self.status_lbl = tk.Label(right, textvariable=self.status_var,
                                    bg=C["panel"], fg=C["muted"],
                                    font=("Courier New", 8, "bold"))
        self.status_lbl.pack(anchor="e")
        self.clock_var = tk.StringVar(value="--:-- --")
        tk.Label(right, textvariable=self.clock_var,
                 bg=C["panel"], fg=C["muted"],
                 font=("Courier New", 7)).pack(anchor="e")

        tk.Frame(self.root, bg=C["border"], height=1).pack(fill="x")

        # Current action
        act = tk.Frame(self.root, bg=C["panel"], pady=7)
        act.pack(fill="x")
        self.action_var = tk.StringVar(value="Say 'Hey Bob' to activate...")
        tk.Label(act, textvariable=self.action_var,
                 bg=C["panel"], fg=C["accent"],
                 font=("Courier New", 8), wraplength=450).pack(padx=12)

        tk.Frame(self.root, bg=C["border"], height=1).pack(fill="x")

        # Log
        wrap = tk.Frame(self.root, bg=C["bg"])
        wrap.pack(fill="both", expand=True)
        self.log = tk.Text(
            wrap, bg=C["bg"], fg=C["text"], font=("Courier New", 9),
            relief="flat", bd=0, wrap="word", state="disabled",
            padx=11, pady=8, cursor="arrow",
            selectbackground=C["border"],
        )
        sb = tk.Scrollbar(wrap, command=self.log.yview,
                          bg=C["panel"], troughcolor=C["bg"],
                          relief="flat", width=5)
        self.log.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.log.pack(fill="both", expand=True)

        for role, color in C.items():
            self.log.tag_configure(role, foreground=color)
        self.log.tag_configure("timestamp", foreground=C["muted"])

        # Footer
        tk.Frame(self.root, bg=C["border"], height=1).pack(fill="x")
        ft = tk.Frame(self.root, bg=C["panel"], pady=6)
        ft.pack(fill="x")
        tk.Label(ft, text="Wake: 'Hey Bob'  |  Sleep: 'Bye'  |  BOB-AI v1 Upgraded © 2026 Ganesh",
                 bg=C["panel"], fg=C["muted"],
                 font=("Courier New", 6)).pack()

        self._update_clock()
        self._pulse()

    # ── ORB ───────────────────────────────────────────────
    def _draw_orb(self, color):
        self.orb.delete("all")
        self.orb.create_oval(2, 2, 38, 38, fill=color,
                              outline=C["accent"], width=1)
        self.orb.create_oval(8, 8, 17, 17, fill="white",
                              outline="", stipple="gray25")

    def _pulse(self):
        if self.booting: return
        cols = [C["accent"], "#005577", C["accent"], "#003344"]
        if not hasattr(self, "_pi"): self._pi = 0
        try:
            self._draw_orb(cols[self._pi % len(cols)])
            self._pi += 1
        except: pass
        self.root.after(650, self._pulse)

    def _update_clock(self):
        if self.booting:
            self.root.after(1000, self._update_clock); return
        import datetime
        self.clock_var.set(datetime.datetime.now().strftime("%I:%M %p"))
        self.root.after(1000, self._update_clock)

    # ── PUBLIC UPDATE ─────────────────────────────────────
    def update(self, text: str, role: str = "info"):
        self.root.after(0, lambda: self._update_ui(text, role))

    def _update_ui(self, text: str, role: str):
        if self.booting: return

        sm = {
            "listening":  ("● LISTENING", C["accent"]),
            "bob":        ("● SPEAKING",  C["accent2"]),
            "user":       ("● HEARD",     C["user"]),
            "idle":       ("● IDLE",      C["muted"]),
            "processing": ("● THINKING",  C["warn"]),
            "error":      ("● ERROR",     C["danger"]),
            "system":     ("● SYSTEM",    C["muted"]),
        }
        if role in sm:
            lbl, col = sm[role]
            self.status_var.set(lbl)
            self.status_lbl.config(fg=col)

        self.action_var.set(text[:72] + ("..." if len(text) > 72 else ""))

        import datetime
        ts     = datetime.datetime.now().strftime("%H:%M:%S")
        prefix = ROLE_PREFIX.get(role, "   ")

        self.log.configure(state="normal")
        self.log.insert("end", f"[{ts}] ", "timestamp")
        self.log.insert("end", f"{prefix}  ", role if role in C else "text")
        self.log.insert("end", f"{text}\n", role if role in C else "text")
        self.log.configure(state="disabled")
        self.log.see("end")

        if role == "listening":
            self._draw_orb(C["accent"])
        elif role == "bob":
            self._draw_orb(C["accent2"])
        elif role == "error":
            self._draw_orb(C["danger"])
        elif role == "processing":
            self._draw_orb(C["warn"])