"""
NetMirror Ultra Multi-Audio Video Downloader
Modern Dark-Mode Desktop GUI (CustomTkinter)
100% English Interface & Logs.
"""

import os
import sys
import queue
import threading
import tkinter as tk
from tkinter import filedialog, messagebox

import customtkinter as ctk

# Ensure local imports work in both source and PyInstaller bundle
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from core_engine import DownloadEngine, DEFAULT_SAVE_DIR
from setup_dependencies import ensure_dependencies

# Setup CustomTkinter Theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class NetMirrorUltraApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Settings
        self.title("NetMirror Ultra Downloader | Multi-Audio Edition")
        self.geometry("940x740")
        self.minsize(820, 640)

        # Engine & Queues
        self.engine = DownloadEngine()
        self.log_queue = queue.Queue()
        self.is_downloading = False

        self._build_ui()
        self._start_dependency_check()
        self._poll_log_queue()

    def _build_ui(self):
        # Configure Main Grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)

        # ---------------- 1. HEADER BANNER ----------------
        header_frame = ctk.CTkFrame(self, fg_color="#0f172a", corner_radius=0)
        header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=(0, 10))
        header_frame.grid_columnconfigure(0, weight=1)

        header_content = ctk.CTkFrame(header_frame, fg_color="transparent")
        header_content.pack(fill="x", padx=25, pady=16)

        title_box = ctk.CTkFrame(header_content, fg_color="transparent")
        title_box.pack(side="left")

        title_lbl = ctk.CTkLabel(
            title_box,
            text="🎬 NETMIRROR ULTRA",
            font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"),
            text_color="#38bdf8"
        )
        title_lbl.pack(anchor="w")

        sub_lbl = ctk.CTkLabel(
            title_box,
            text="Universal 1080p Video & Multi-Audio Track Downloader (Supports net52.cc, net77.cc, freecdn1.top)",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color="#94a3b8"
        )
        sub_lbl.pack(anchor="w")

        # Status Badge
        self.status_badge = ctk.CTkLabel(
            header_content,
            text="● SYSTEM READY",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color="#4ade80",
            fg_color="#1e293b",
            corner_radius=12,
            padx=14,
            pady=6
        )
        self.status_badge.pack(side="right")

        # ---------------- 2. INPUT CARD ----------------
        input_card = ctk.CTkFrame(self, fg_color="#1e293b", corner_radius=12)
        input_card.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 12))
        input_card.grid_columnconfigure(0, weight=1)

        input_header = ctk.CTkFrame(input_card, fg_color="transparent")
        input_header.pack(fill="x", padx=16, pady=(12, 6))

        ctk.CTkLabel(
            input_header,
            text="INPUT SOURCE (cURL COMMAND OR M3U8 STREAM URL)",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color="#f8fafc"
        ).pack(side="left")

        # Paste & Clear Buttons
        btn_box = ctk.CTkFrame(input_header, fg_color="transparent")
        btn_box.pack(side="right")

        clear_btn = ctk.CTkButton(
            btn_box,
            text="Clear",
            width=65,
            height=28,
            fg_color="#334155",
            hover_color="#475569",
            text_color="#f1f5f9",
            font=ctk.CTkFont(size=11),
            command=self._clear_input
        )
        clear_btn.pack(side="right", padx=(6, 0))

        paste_btn = ctk.CTkButton(
            btn_box,
            text="📋 Paste Clipboard",
            width=135,
            height=28,
            fg_color="#0284c7",
            hover_color="#0369a1",
            text_color="#ffffff",
            font=ctk.CTkFont(size=11, weight="bold"),
            command=self._paste_clipboard
        )
        paste_btn.pack(side="right")

        self.input_box = ctk.CTkTextbox(
            input_card,
            height=85,
            font=ctk.CTkFont(family="Consolas", size=12),
            fg_color="#0f172a",
            text_color="#f8fafc",
            border_width=1,
            border_color="#334155",
            corner_radius=8
        )
        self.input_box.pack(fill="x", padx=16, pady=(0, 14))

        # ---------------- 3. SETTINGS CARD ----------------
        settings_card = ctk.CTkFrame(self, fg_color="#1e293b", corner_radius=12)
        settings_card.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 12))
        settings_card.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Row 1: Filename & Resolution
        ctk.CTkLabel(
            settings_card, text="File Name (Optional):", font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#cbd5e1"
        ).grid(row=0, column=0, sticky="w", padx=16, pady=(12, 4))

        self.filename_entry = ctk.CTkEntry(
            settings_card,
            placeholder_text="e.g., Avatar_The_Last_Airbender_S01E01",
            fg_color="#0f172a",
            border_color="#334155",
            height=34
        )
        self.filename_entry.grid(row=0, column=1, sticky="ew", padx=(0, 16), pady=(12, 4))

        ctk.CTkLabel(
            settings_card, text="Resolution:", font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#cbd5e1"
        ).grid(row=0, column=2, sticky="w", padx=16, pady=(12, 4))

        self.res_menu = ctk.CTkOptionMenu(
            settings_card,
            values=["1080p (Full HD)", "720p (HD)", "480p (SD)", "Best Available"],
            fg_color="#0f172a",
            button_color="#334155",
            button_hover_color="#475569",
            height=34
        )
        self.res_menu.set("1080p (Full HD)")
        self.res_menu.grid(row=0, column=3, sticky="ew", padx=(0, 16), pady=(12, 4))

        # Row 2: Save Folder & Audio Selection
        ctk.CTkLabel(
            settings_card, text="Save Folder:", font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#cbd5e1"
        ).grid(row=1, column=0, sticky="w", padx=16, pady=(6, 14))

        folder_frame = ctk.CTkFrame(settings_card, fg_color="transparent")
        folder_frame.grid(row=1, column=1, sticky="ew", padx=(0, 16), pady=(6, 14))
        folder_frame.grid_columnconfigure(0, weight=1)

        self.folder_entry = ctk.CTkEntry(
            folder_frame,
            fg_color="#0f172a",
            border_color="#334155",
            height=34
        )
        self.folder_entry.grid(row=0, column=0, sticky="ew")
        self.folder_entry.insert(0, DEFAULT_SAVE_DIR)

        browse_btn = ctk.CTkButton(
            folder_frame,
            text="Browse",
            width=70,
            height=34,
            fg_color="#334155",
            hover_color="#475569",
            command=self._browse_folder
        )
        browse_btn.grid(row=0, column=1, padx=(6, 0))

        ctk.CTkLabel(
            settings_card, text="Audio Tracks:", font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#cbd5e1"
        ).grid(row=1, column=2, sticky="w", padx=16, pady=(6, 14))

        self.audio_menu = ctk.CTkOptionMenu(
            settings_card,
            values=[
                "All Audio Tracks (Recommended)",
                "English & Hindi Only",
                "English Only",
                "Hindi Only"
            ],
            fg_color="#0f172a",
            button_color="#334155",
            button_hover_color="#475569",
            height=34
        )
        self.audio_menu.set("All Audio Tracks (Recommended)")
        self.audio_menu.grid(row=1, column=3, sticky="ew", padx=(0, 16), pady=(6, 14))

        # ---------------- 4. CONTROLS & PROGRESS ----------------
        control_frame = ctk.CTkFrame(self, fg_color="transparent")
        control_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 10))
        control_frame.grid_columnconfigure(0, weight=3)
        control_frame.grid_columnconfigure(1, weight=1)
        control_frame.grid_columnconfigure(2, weight=1)

        self.start_btn = ctk.CTkButton(
            control_frame,
            text="🚀 START MULTI-AUDIO DOWNLOAD",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=44,
            fg_color="#0284c7",
            hover_color="#0369a1",
            corner_radius=10,
            command=self._start_download
        )
        self.start_btn.grid(row=0, column=0, sticky="ew", padx=(0, 10))

        self.abort_btn = ctk.CTkButton(
            control_frame,
            text="⏹ Abort",
            font=ctk.CTkFont(size=13, weight="bold"),
            height=44,
            fg_color="#ef4444",
            hover_color="#dc2626",
            state="disabled",
            corner_radius=10,
            command=self._abort_download
        )
        self.abort_btn.grid(row=0, column=1, sticky="ew", padx=(0, 10))

        self.open_folder_btn = ctk.CTkButton(
            control_frame,
            text="📁 Open Folder",
            font=ctk.CTkFont(size=13),
            height=44,
            fg_color="#334155",
            hover_color="#475569",
            corner_radius=10,
            command=self._open_output_folder
        )
        self.open_folder_btn.grid(row=0, column=2, sticky="ew")

        # Progress Bar & Info
        progress_box = ctk.CTkFrame(self, fg_color="#1e293b", corner_radius=10)
        progress_box.grid(row=4, column=0, sticky="ew", padx=20, pady=(0, 10))
        progress_box.grid_columnconfigure(0, weight=1)

        self.progress_bar = ctk.CTkProgressBar(progress_box, height=12, corner_radius=6)
        self.progress_bar.pack(fill="x", padx=16, pady=(12, 6))
        self.progress_bar.set(0)

        self.progress_lbl = ctk.CTkLabel(
            progress_box,
            text="Ready. Paste your stream link above and click 'START MULTI-AUDIO DOWNLOAD'.",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color="#94a3b8"
        )
        self.progress_lbl.pack(anchor="w", padx=16, pady=(0, 10))

        # ---------------- 5. LOG TERMINAL ----------------
        log_frame = ctk.CTkFrame(self, fg_color="#1e293b", corner_radius=12)
        log_frame.grid(row=5, column=0, sticky="nsew", padx=20, pady=(0, 16))
        log_frame.grid_rowconfigure(1, weight=1)
        log_frame.grid_columnconfigure(0, weight=1)

        log_head = ctk.CTkFrame(log_frame, fg_color="transparent")
        log_head.grid(row=0, column=0, sticky="ew", padx=16, pady=(10, 4))

        ctk.CTkLabel(
            log_head,
            text="TERMINAL OUTPUT",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#94a3b8"
        ).pack(side="left")

        copy_log_btn = ctk.CTkButton(
            log_head,
            text="Copy Logs",
            width=75,
            height=24,
            font=ctk.CTkFont(size=10),
            fg_color="#334155",
            hover_color="#475569",
            command=self._copy_logs
        )
        copy_log_btn.pack(side="right")

        self.log_textbox = ctk.CTkTextbox(
            log_frame,
            font=ctk.CTkFont(family="Consolas", size=11),
            fg_color="#020617",
            text_color="#4ade80",
            corner_radius=8,
            border_width=1,
            border_color="#1e293b"
        )
        self.log_textbox.grid(row=1, column=0, sticky="nsew", padx=14, pady=(0, 12))

    # ---------------- HELPER METHODS ----------------
    def _log(self, text: str):
        self.log_queue.put(("log", text))

    def _set_progress(self, pct: float, msg: str):
        self.log_queue.put(("progress", (pct, msg)))

    def _poll_log_queue(self):
        while not self.log_queue.empty():
            msg_type, data = self.log_queue.get_nowait()
            if msg_type == "log":
                self.log_textbox.insert("end", data + "\n")
                self.log_textbox.see("end")
            elif msg_type == "progress":
                pct, status_text = data
                self.progress_bar.set(max(0.0, min(1.0, pct / 100.0)))
                self.progress_lbl.configure(text=status_text)
        self.after(100, self._poll_log_queue)

    def _start_dependency_check(self):
        """Run initial dependency check in background."""
        def check():
            self._log("[System] Checking required binaries (N_m3u8DL-RE & FFmpeg)...")
            try:
                n, f = ensure_dependencies(
                    status_callback=lambda s: self._log(f"  {s}"),
                    progress_callback=lambda pct, txt: self._set_progress(pct, txt)
                )
                self._log(f"[System] Binaries verified:\n  • Downloader: {n}\n  • Muxer: {f}\n")
                self.status_badge.configure(text="● SYSTEM READY", text_color="#4ade80")
                self._set_progress(0, "Ready. All dependencies are configured.")
            except Exception as e:
                self._log(f"[System Error] Dependency initialization failed: {e}")
                self.status_badge.configure(text="● SETUP ERROR", text_color="#ef4444")

        threading.Thread(target=check, daemon=True).start()

    def _paste_clipboard(self):
        try:
            content = self.clipboard_get().strip()
            self.input_box.delete("1.0", "end")
            self.input_box.insert("end", content)
            self._log("[Action] Pasted content from clipboard.")
        except Exception:
            messagebox.showwarning("Clipboard", "Could not read content from system clipboard.")

    def _clear_input(self):
        self.input_box.delete("1.0", "end")

    def _browse_folder(self):
        folder = filedialog.askdirectory(initialdir=self.folder_entry.get())
        if folder:
            self.folder_entry.delete(0, "end")
            self.folder_entry.insert(0, folder)

    def _open_output_folder(self):
        p = self.folder_entry.get().strip()
        if os.path.exists(p):
            os.startfile(p)
        else:
            messagebox.showerror("Error", f"Folder does not exist:\n{p}")

    def _copy_logs(self):
        logs = self.log_textbox.get("1.0", "end")
        self.clipboard_clear()
        self.clipboard_append(logs)
        messagebox.showinfo("Copied", "Logs copied to clipboard!")

    def _abort_download(self):
        if self.is_downloading:
            self._log("\n[Action] Sending abort request to engine...")
            self.engine.abort()

    def _start_download(self):
        if self.is_downloading:
            return

        raw_input = self.input_box.get("1.0", "end").strip()
        if not raw_input:
            messagebox.showwarning("Missing Input", "Please paste a cURL command or M3U8 stream URL first!")
            return

        filename = self.filename_entry.get().strip()
        save_dir = self.folder_entry.get().strip()
        
        # Resolution map
        res_text = self.res_menu.get()
        if "1080p" in res_text:
            resolution = "1080p"
        elif "720p" in res_text:
            resolution = "720p"
        elif "480p" in res_text:
            resolution = "480p"
        else:
            resolution = "best"

        # Audio map
        aud_text = self.audio_menu.get()
        if "English & Hindi" in aud_text:
            audio_choice = "en_hi"
        elif "English Only" in aud_text:
            audio_choice = "eng"
        elif "Hindi Only" in aud_text:
            audio_choice = "hin"
        else:
            audio_choice = "all"

        self.is_downloading = True
        self.start_btn.configure(state="disabled", fg_color="#475569", text="⏳ DOWNLOADING...")
        self.abort_btn.configure(state="normal")
        self.status_badge.configure(text="● DOWNLOADING", text_color="#38bdf8")
        self.progress_bar.set(0)

        def worker():
            try:
                out = self.engine.run_download(
                    input_text=raw_input,
                    save_name=filename,
                    save_dir=save_dir,
                    resolution=resolution,
                    audio_choice=audio_choice,
                    log_callback=self._log,
                    progress_callback=self._set_progress
                )
                self.status_badge.configure(text="● COMPLETED", text_color="#4ade80")
                self._set_progress(100.0, f"Completed: {os.path.basename(out)}")
                messagebox.showinfo(
                    "Download Complete",
                    f"Successfully downloaded with multi-audio support!\n\nFile:\n{out}"
                )
            except Exception as e:
                self.status_badge.configure(text="● FAILED", text_color="#ef4444")
                self._log(f"\n[Error] {e}")
                self._set_progress(0, f"Error: {e}")
                messagebox.showerror("Download Error", str(e))
            finally:
                self.is_downloading = False
                self.start_btn.configure(state="normal", fg_color="#0284c7", text="🚀 START MULTI-AUDIO DOWNLOAD")
                self.abort_btn.configure(state="disabled")

        threading.Thread(target=worker, daemon=True).start()

if __name__ == "__main__":
    app = NetMirrorUltraApp()
    app.mainloop()
