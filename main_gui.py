# NetMi.Video Downloader - v2.1.0
# Professional multi-audio stream downloader with fixed UI layout.
# Author: XMON4U (https://github.com/Xmon4u)

import os
import sys
import queue
import threading
import webbrowser
from tkinter import filedialog, messagebox

import customtkinter as ctk

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from core_engine import DownloadEngine, DEFAULT_SAVE_DIR
from setup_dependencies import ensure_dependencies

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# ── Color Palette ─────────────────────────────────────────────────────────────
BG_ROOT      = "#0a0f1e"
BG_HEADER    = "#0d1326"
BG_CARD      = "#111827"
BG_CARD2     = "#0f1929"
BG_INPUT     = "#080d1a"
BG_TERMINAL  = "#060b18"
ACCENT_BLUE  = "#2563eb"
ACCENT_CYAN  = "#06b6d4"
ACCENT_GLOW  = "#38bdf8"
BORDER       = "#1e2d4a"
BORDER2      = "#16253d"
TEXT_PRIMARY = "#f0f6ff"
TEXT_SECOND  = "#8ba3c4"
TEXT_MUTED   = "#4a6080"
TEXT_GREEN   = "#22d3a5"
TEXT_RED     = "#f87171"
TEXT_YELLOW  = "#fbbf24"
TEXT_LOG     = "#7ee8a2"
FONT_MAIN    = "Segoe UI"
FONT_MONO    = "Cascadia Code"

# Grid row constants — each section gets its own row, NO overlapping
ROW_HEADER   = 0
ROW_INPUT    = 1
ROW_OPTIONS  = 2
ROW_ACTIONS  = 3   # buttons: Start / Stop / Open Folder
ROW_PROGRESS = 4   # thin progress bar + status text
ROW_TERMINAL = 5   # expandable log panel
ROW_FOOTER   = 6


class NetMiApp(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("NetMi.Video Downloader")
        self.geometry("980x820")
        self.minsize(880, 720)
        self.configure(fg_color=BG_ROOT)

        icon_path = os.path.join(BASE_DIR, "app_icon.ico")
        if os.path.exists(icon_path):
            try:
                self.iconbitmap(icon_path)
            except Exception:
                pass

        self.engine         = DownloadEngine()
        self.log_queue      = queue.Queue()
        self.is_downloading = False

        self._build_ui()
        self._poll_log_queue()
        self._start_dependency_check()

    # ── Layout grid ──────────────────────────────────────────────────────────
    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        # Only the terminal row expands to fill remaining vertical space
        self.grid_rowconfigure(ROW_TERMINAL, weight=1)

        self._build_header()
        self._build_input_card()
        self._build_options_card()
        self._build_action_buttons()   # row 3
        self._build_progress_row()     # row 4
        self._build_terminal()         # row 5
        self._build_footer()           # row 6

    # ── Header (row 0) ───────────────────────────────────────────────────────
    def _build_header(self):
        hdr = ctk.CTkFrame(self, fg_color=BG_HEADER, corner_radius=0, height=72)
        hdr.grid(row=ROW_HEADER, column=0, sticky="ew")
        hdr.grid_propagate(False)
        hdr.grid_columnconfigure(1, weight=1)

        # Icon box
        icon_box = ctk.CTkFrame(hdr, fg_color=ACCENT_BLUE, width=40, height=40,
                                corner_radius=10)
        icon_box.grid(row=0, column=0, rowspan=2, padx=(18, 12), pady=16)
        icon_box.grid_propagate(False)
        ctk.CTkLabel(icon_box, text="N",
                     font=ctk.CTkFont(size=18, weight="bold"),
                     text_color="white").place(relx=0.5, rely=0.5, anchor="center")

        # Title
        ctk.CTkLabel(
            hdr, text="NetMi.Video Downloader",
            font=ctk.CTkFont(family=FONT_MAIN, size=18, weight="bold"),
            text_color=TEXT_PRIMARY, anchor="w"
        ).grid(row=0, column=1, sticky="sw", pady=(16, 0))

        # Subtitle
        ctk.CTkLabel(
            hdr,
            text="1080p  ·  All Audio Tracks  ·  MKV Output  |  net52.cc  ·  net77.cc  ·  freecdn1.top",
            font=ctk.CTkFont(family=FONT_MAIN, size=10),
            text_color=TEXT_SECOND, anchor="w"
        ).grid(row=1, column=1, sticky="nw", pady=(0, 12))

        # Status badge
        self.status_badge = ctk.CTkLabel(
            hdr, text="  ●  Initializing",
            font=ctk.CTkFont(family=FONT_MAIN, size=11, weight="bold"),
            text_color=TEXT_YELLOW,
            fg_color=BG_CARD, corner_radius=20, padx=14, pady=6
        )
        self.status_badge.grid(row=0, column=2, rowspan=2, padx=18, pady=16)

    # ── Input Card (row 1) ───────────────────────────────────────────────────
    def _build_input_card(self):
        card = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=10)
        card.grid(row=ROW_INPUT, column=0, sticky="ew", padx=16, pady=(10, 5))
        card.grid_columnconfigure(0, weight=1)

        # Top row: label + buttons
        top = ctk.CTkFrame(card, fg_color="transparent")
        top.pack(fill="x", padx=14, pady=(10, 5))

        ctk.CTkLabel(
            top, text="Stream Source",
            font=ctk.CTkFont(family=FONT_MAIN, size=12, weight="bold"),
            text_color=ACCENT_GLOW
        ).pack(side="left")

        ctk.CTkLabel(
            top, text="  Paste a cURL command or direct M3U8 URL",
            font=ctk.CTkFont(family=FONT_MAIN, size=10),
            text_color=TEXT_MUTED
        ).pack(side="left")

        # Button group (right-aligned)
        btn_row = ctk.CTkFrame(top, fg_color="transparent")
        btn_row.pack(side="right")

        ctk.CTkButton(
            btn_row, text="Clear", width=60, height=30,
            fg_color=BG_CARD2, hover_color=BORDER,
            border_width=1, border_color=BORDER2,
            text_color=TEXT_SECOND,
            font=ctk.CTkFont(family=FONT_MAIN, size=11), corner_radius=6,
            command=self._clear_input
        ).pack(side="right", padx=(6, 0))

        ctk.CTkButton(
            btn_row, text="📋  Paste", width=100, height=30,
            fg_color=ACCENT_BLUE, hover_color="#1d4ed8",
            text_color="white",
            font=ctk.CTkFont(family=FONT_MAIN, size=11, weight="bold"), corner_radius=6,
            command=self._paste_clipboard
        ).pack(side="right")

        # Text input box
        self.input_box = ctk.CTkTextbox(
            card, height=75,
            font=ctk.CTkFont(family=FONT_MONO, size=10),
            fg_color=BG_INPUT, text_color="#c8deff",
            border_width=1, border_color=BORDER2, corner_radius=8
        )
        self.input_box.pack(fill="x", padx=14, pady=(0, 12))

    # ── Options Card (row 2) ─────────────────────────────────────────────────
    def _build_options_card(self):
        card = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=10)
        card.grid(row=ROW_OPTIONS, column=0, sticky="ew", padx=16, pady=(0, 5))
        card.grid_columnconfigure(1, weight=1)
        card.grid_columnconfigure(3, weight=1)

        def lbl(row, col, text):
            ctk.CTkLabel(
                card, text=text,
                font=ctk.CTkFont(family=FONT_MAIN, size=11, weight="bold"),
                text_color=TEXT_SECOND
            ).grid(row=row, column=col, sticky="w", padx=(16, 8), pady=8)

        entry_kw = dict(
            fg_color=BG_INPUT, border_color=BORDER2, border_width=1,
            height=34, text_color=TEXT_PRIMARY,
            font=ctk.CTkFont(family=FONT_MAIN, size=11)
        )
        menu_kw = dict(
            fg_color=BG_INPUT, button_color=BORDER,
            button_hover_color=BORDER2,
            dropdown_fg_color=BG_CARD, dropdown_hover_color=BORDER,
            height=34,
            font=ctk.CTkFont(family=FONT_MAIN, size=11),
            text_color=TEXT_PRIMARY
        )

        # Row 0: Title + Resolution
        lbl(0, 0, "Title (optional)")
        self.filename_entry = ctk.CTkEntry(
            card, placeholder_text="Leave blank to auto-detect", **entry_kw
        )
        self.filename_entry.grid(row=0, column=1, sticky="ew", padx=(0, 16), pady=8)

        lbl(0, 2, "Resolution")
        self.res_menu = ctk.CTkOptionMenu(
            card,
            values=["1080p (Full HD)", "720p (HD)", "480p (SD)", "Best Available"],
            **menu_kw
        )
        self.res_menu.set("1080p (Full HD)")
        self.res_menu.grid(row=0, column=3, sticky="ew", padx=(0, 16), pady=8)

        # Row 1: Save Folder + Audio Tracks
        lbl(1, 0, "Save Folder")
        fr = ctk.CTkFrame(card, fg_color="transparent")
        fr.grid(row=1, column=1, sticky="ew", padx=(0, 16), pady=8)
        fr.grid_columnconfigure(0, weight=1)

        self.folder_entry = ctk.CTkEntry(fr, **entry_kw)
        self.folder_entry.grid(row=0, column=0, sticky="ew")
        self.folder_entry.insert(0, DEFAULT_SAVE_DIR)

        ctk.CTkButton(
            fr, text="Browse", width=70, height=34,
            fg_color=BG_CARD2, hover_color=BORDER,
            border_width=1, border_color=BORDER2,
            text_color=TEXT_SECOND,
            font=ctk.CTkFont(family=FONT_MAIN, size=11), corner_radius=6,
            command=self._browse_folder
        ).grid(row=0, column=1, padx=(6, 0))

        lbl(1, 2, "Audio Tracks")
        self.audio_menu = ctk.CTkOptionMenu(
            card,
            values=[
                "All Languages (Recommended)",
                "English + Hindi",
                "English Only",
                "Hindi Only",
            ],
            **menu_kw
        )
        self.audio_menu.set("All Languages (Recommended)")
        self.audio_menu.grid(row=1, column=3, sticky="ew", padx=(0, 16), pady=8)

    # ── Action Buttons (row 3) — OWN dedicated row, NO overlap ──────────────
    def _build_action_buttons(self):
        bar = ctk.CTkFrame(self, fg_color="transparent")
        bar.grid(row=ROW_ACTIONS, column=0, sticky="ew", padx=16, pady=(5, 5))
        bar.grid_columnconfigure(0, weight=3)   # Start button takes most space
        bar.grid_columnconfigure(1, weight=1)
        bar.grid_columnconfigure(2, weight=1)

        # Start Download
        self.start_btn = ctk.CTkButton(
            bar,
            text="▶   Start Download",
            font=ctk.CTkFont(family=FONT_MAIN, size=14, weight="bold"),
            height=46, corner_radius=10,
            fg_color=ACCENT_BLUE, hover_color="#1d4ed8",
            text_color="white",
            command=self._start_download
        )
        self.start_btn.grid(row=0, column=0, sticky="ew", padx=(0, 8))

        # Stop / Abort
        self.abort_btn = ctk.CTkButton(
            bar,
            text="■  Stop",
            font=ctk.CTkFont(family=FONT_MAIN, size=13, weight="bold"),
            height=46, corner_radius=10,
            fg_color="#7f1d1d", hover_color="#991b1b",
            text_color="#fca5a5",
            state="disabled",
            command=self._abort_download
        )
        self.abort_btn.grid(row=0, column=1, sticky="ew", padx=(0, 8))

        # Open Folder
        ctk.CTkButton(
            bar,
            text="📁  Open Folder",
            font=ctk.CTkFont(family=FONT_MAIN, size=13),
            height=46, corner_radius=10,
            fg_color=BG_CARD, hover_color=BORDER,
            border_width=1, border_color=BORDER2,
            text_color=TEXT_SECOND,
            command=self._open_output_folder
        ).grid(row=0, column=2, sticky="ew")

    # ── Progress Row (row 4) — thin bar below buttons ────────────────────────
    def _build_progress_row(self):
        prog = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=8)
        prog.grid(row=ROW_PROGRESS, column=0, sticky="ew", padx=16, pady=(0, 5))
        prog.grid_columnconfigure(0, weight=1)

        self.progress_bar = ctk.CTkProgressBar(
            prog, height=5, corner_radius=3,
            progress_color=ACCENT_CYAN, fg_color=BORDER2
        )
        self.progress_bar.pack(fill="x", padx=14, pady=(9, 3))
        self.progress_bar.set(0)

        self.progress_lbl = ctk.CTkLabel(
            prog,
            text="Ready — paste a stream source above and click Start Download.",
            font=ctk.CTkFont(family=FONT_MAIN, size=10),
            text_color=TEXT_MUTED, anchor="w"
        )
        self.progress_lbl.pack(anchor="w", padx=14, pady=(0, 7))

    # ── Terminal / Output Log (row 5) ────────────────────────────────────────
    def _build_terminal(self):
        term = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=10)
        term.grid(row=ROW_TERMINAL, column=0, sticky="nsew", padx=16, pady=(0, 5))
        term.grid_rowconfigure(1, weight=1)
        term.grid_columnconfigure(0, weight=1)

        # Header bar with traffic-light dots
        thead = ctk.CTkFrame(term, fg_color="transparent")
        thead.grid(row=0, column=0, sticky="ew", padx=12, pady=(9, 3))

        dots = ctk.CTkFrame(thead, fg_color="transparent")
        dots.pack(side="left")
        for dot_color in ("#ef4444", "#f59e0b", "#22c55e"):
            ctk.CTkFrame(
                dots, fg_color=dot_color, width=9, height=9, corner_radius=5
            ).pack(side="left", padx=3)

        ctk.CTkLabel(
            thead, text="Output Log",
            font=ctk.CTkFont(family=FONT_MAIN, size=11, weight="bold"),
            text_color=TEXT_MUTED
        ).pack(side="left", padx=(10, 0))

        btn_r = ctk.CTkFrame(thead, fg_color="transparent")
        btn_r.pack(side="right")

        ctk.CTkButton(
            btn_r, text="Clear", width=52, height=22,
            font=ctk.CTkFont(size=10), fg_color=BG_CARD2,
            hover_color=BORDER, border_width=1, border_color=BORDER2,
            text_color=TEXT_MUTED, corner_radius=5,
            command=lambda: self.log_textbox.delete("1.0", "end")
        ).pack(side="right", padx=(5, 0))

        ctk.CTkButton(
            btn_r, text="Copy", width=52, height=22,
            font=ctk.CTkFont(size=10), fg_color=BG_CARD2,
            hover_color=BORDER, border_width=1, border_color=BORDER2,
            text_color=TEXT_MUTED, corner_radius=5,
            command=self._copy_logs
        ).pack(side="right")

        # Log textbox — fills remaining space
        self.log_textbox = ctk.CTkTextbox(
            term,
            font=ctk.CTkFont(family=FONT_MONO, size=10),
            fg_color=BG_TERMINAL, text_color=TEXT_LOG,
            corner_radius=8, border_width=1, border_color=BORDER2,
            wrap="none"
        )
        self.log_textbox.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

    # ── Footer (row 6) ───────────────────────────────────────────────────────
    def _build_footer(self):
        footer = ctk.CTkFrame(self, fg_color=BG_HEADER, corner_radius=0, height=28)
        footer.grid(row=ROW_FOOTER, column=0, sticky="ew")
        footer.grid_propagate(False)

        ctk.CTkButton(
            footer,
            text="XMON4U  •  github.com/Xmon4u  •  v2.1.0",
            font=ctk.CTkFont(family=FONT_MAIN, size=10),
            text_color=TEXT_MUTED, fg_color="transparent",
            hover_color=BG_CARD, cursor="hand2",
            command=lambda: webbrowser.open_new_tab("https://github.com/Xmon4u")
        ).pack(side="right", padx=14)

    # ── Queue polling ─────────────────────────────────────────────────────────
    def _log(self, text: str):
        self.log_queue.put(("log", text))

    def _set_progress(self, pct: float, msg: str):
        self.log_queue.put(("progress", (pct, msg)))

    def _poll_log_queue(self):
        processed = 0
        while not self.log_queue.empty() and processed < 30:
            msg_type, data = self.log_queue.get_nowait()
            processed += 1
            if msg_type == "log":
                self.log_textbox.insert("end", data + "\n")
                self.log_textbox.see("end")
            elif msg_type == "progress":
                pct, status_text = data
                self.progress_bar.set(max(0.0, min(1.0, pct / 100.0)))
                self.progress_lbl.configure(text=status_text)
        self.after(80, self._poll_log_queue)

    def _set_status(self, state: str):
        states = {
            "ready":       ("  ●  Ready",        TEXT_GREEN),
            "downloading": ("  ●  Downloading",  ACCENT_GLOW),
            "done":        ("  ●  Complete",     TEXT_GREEN),
            "error":       ("  ●  Error",        TEXT_RED),
            "aborted":     ("  ●  Stopped",      TEXT_YELLOW),
        }
        text, color = states.get(state, ("  ●  Ready", TEXT_GREEN))
        self.status_badge.configure(text=text, text_color=color)

    # ── Dependency check ──────────────────────────────────────────────────────
    def _start_dependency_check(self):
        def _check():
            self._log("[System] Checking dependencies (N_m3u8DL-RE + FFmpeg)...")
            try:
                n, f = ensure_dependencies(
                    status_callback=lambda s: self._log(f"  {s}"),
                    progress_callback=lambda pct, txt: self._set_progress(pct, txt),
                )
                self._log(f"[Ready] Downloader : {n}")
                self._log(f"[Ready] Multiplexer: {f}\n")
                self._set_status("ready")
                self._set_progress(0, "Ready — all dependencies configured.")
            except Exception as exc:
                self._log(f"[Error] Dependency setup failed: {exc}")
                self._set_status("error")

        threading.Thread(target=_check, daemon=True).start()

    # ── User actions ──────────────────────────────────────────────────────────
    def _paste_clipboard(self):
        try:
            content = self.clipboard_get().strip()
            self.input_box.delete("1.0", "end")
            self.input_box.insert("end", content)
        except Exception:
            messagebox.showwarning("Clipboard", "Could not read from system clipboard.")

    def _clear_input(self):
        self.input_box.delete("1.0", "end")

    def _browse_folder(self):
        folder = filedialog.askdirectory(initialdir=self.folder_entry.get())
        if folder:
            self.folder_entry.delete(0, "end")
            self.folder_entry.insert(0, folder)

    def _open_output_folder(self):
        path = self.folder_entry.get().strip()
        if os.path.isdir(path):
            os.startfile(path)
        else:
            messagebox.showerror("Folder Not Found",
                                 f"The folder does not exist:\n{path}")

    def _copy_logs(self):
        logs = self.log_textbox.get("1.0", "end")
        self.clipboard_clear()
        self.clipboard_append(logs)

    def _abort_download(self):
        if self.is_downloading:
            self._log("\n[Action] Sending stop signal to download engine...")
            self.engine.abort()

    def _start_download(self):
        if self.is_downloading:
            return

        raw_input = self.input_box.get("1.0", "end").strip()
        if not raw_input:
            messagebox.showwarning(
                "Missing Input",
                "Please paste a cURL command or direct M3U8 link first."
            )
            return

        filename = self.filename_entry.get().strip()
        save_dir = self.folder_entry.get().strip()

        res_text   = self.res_menu.get()
        resolution = (
            "1080p" if "1080p" in res_text else
            "720p"  if "720p"  in res_text else
            "480p"  if "480p"  in res_text else
            "best"
        )

        aud_text     = self.audio_menu.get()
        audio_choice = (
            "en_hi" if "English + Hindi" in aud_text else
            "eng"   if "English Only"    in aud_text else
            "hin"   if "Hindi Only"      in aud_text else
            "all"
        )

        # Switch UI to downloading state
        self.is_downloading = True
        self.start_btn.configure(
            state="disabled",
            fg_color="#1e3a5f",
            text="⏳  Downloading..."
        )
        self.abort_btn.configure(state="normal")
        self._set_status("downloading")
        self.progress_bar.set(0)
        self.log_textbox.delete("1.0", "end")

        def _worker():
            try:
                out = self.engine.run_download(
                    input_text=raw_input,
                    save_name=filename,
                    save_dir=save_dir,
                    resolution=resolution,
                    audio_choice=audio_choice,
                    log_callback=self._log,
                    progress_callback=self._set_progress,
                )
                self._set_status("done")
                self._set_progress(100.0, f"Saved: {os.path.basename(out)}")
                messagebox.showinfo(
                    "Download Complete",
                    f"File saved successfully.\n\n{out}"
                )
            except RuntimeError as exc:
                err = str(exc)
                self._set_status("aborted" if "aborted" in err.lower() else "error")
                self._log(f"\n[Error] {err}")
                self._set_progress(0, f"Failed: {err[:100]}")
                if "aborted" not in err.lower():
                    messagebox.showerror("Download Failed", err)
            except Exception as exc:
                self._set_status("error")
                self._log(f"\n[Unexpected Error] {exc}")
                self._set_progress(0, "An unexpected error occurred.")
                messagebox.showerror("Unexpected Error", str(exc))
            finally:
                self.is_downloading = False
                self.start_btn.configure(
                    state="normal",
                    fg_color=ACCENT_BLUE,
                    text="▶   Start Download"
                )
                self.abort_btn.configure(state="disabled")

        threading.Thread(target=_worker, daemon=True).start()


if __name__ == "__main__":
    app = NetMiApp()
    app.mainloop()
