"""
Ultra Downloader - Multi-Audio Edition
Core High-Performance Engine with Non-Blocking Streaming & Conflict Resolution
"""

import os
import re
import sys
import time
import shutil
import subprocess
from typing import Dict, Any, Optional, Callable

from setup_dependencies import ensure_dependencies

DEFAULT_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36"
DEFAULT_SAVE_DIR = os.path.join(os.environ.get("USERPROFILE", "C:\\"), "Desktop")

class DownloadEngine:
    def __init__(self):
        self.current_process: Optional[subprocess.Popen] = None
        self._is_aborted = False

    def abort(self):
        """Safely terminate any running download process."""
        self._is_aborted = True
        if self.current_process and self.current_process.poll() is None:
            try:
                self.current_process.terminate()
                time.sleep(0.5)
                if self.current_process.poll() is None:
                    self.current_process.kill()
            except Exception:
                pass

    @staticmethod
    def parse_input(raw_text: str) -> Dict[str, Any]:
        """Extract stream URL, custom headers, referer, and origin from cURL or URL string."""
        text = raw_text.strip()
        url = ""
        headers = {}

        if "curl" in text.lower():
            cleaned = text.replace('^"', '"').replace('^&', '&').replace('^^', '^').replace('^', '')
            url_match = re.search(r'(?:--url|-u)?\s*["\']?(https?://[^\s"\']+)["\']?', cleaned, re.IGNORECASE)
            if url_match:
                url = url_match.group(1).rstrip('"\'')
                
            header_matches = re.findall(r'-H\s*["\']([^"\']+)["\']', cleaned, re.IGNORECASE)
            for h in header_matches:
                if ":" in h:
                    k, v = h.split(":", 1)
                    headers[k.strip().lower()] = v.strip()
        else:
            url_match = re.search(r'https?://[^\s"\']+', text)
            if url_match:
                url = url_match.group(0).rstrip('"\'')

        referer = headers.get("referer", "https://net52.cc/")
        user_agent = headers.get("user-agent", DEFAULT_UA)
        origin = headers.get("origin", "https://net52.cc")

        return {
            "url": url,
            "referer": referer,
            "user_agent": user_agent,
            "origin": origin,
            "headers": headers
        }

    def fetch_master_playlist(self, info: Dict[str, Any], temp_dir: str) -> str:
        """Download master playlist to local cache to ensure non-expired parsing."""
        url = info["url"]
        if not url:
            raise ValueError("No valid URL found in input.")

        os.makedirs(temp_dir, exist_ok=True)
        local_path = os.path.join(temp_dir, f"master_{int(time.time())}.m3u8")

        curl_cmd = [
            "curl.exe", "-s", url,
            "-H", f"Referer: {info['referer']}",
            "-H", f"Origin: {info['origin']}",
            "-H", f"User-Agent: {info['user_agent']}",
            "-o", local_path
        ]

        res = subprocess.run(curl_cmd, capture_output=True, text=True, timeout=20)
        if res.returncode != 0 or not os.path.exists(local_path) or os.path.getsize(local_path) == 0:
            raise RuntimeError(f"Failed to fetch master playlist from source: {url}")

        with open(local_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read(500)
            if "Only Valid Users Allowed" in content or "403 Forbidden" in content or "<html" in content.lower():
                raise RuntimeError("Access denied or session token expired. Please copy a fresh cURL request from DevTools.")

        return local_path

    def run_download(
        self,
        input_text: str,
        save_name: str = "",
        save_dir: str = DEFAULT_SAVE_DIR,
        resolution: str = "1080p",
        audio_choice: str = "all",
        log_callback: Optional[Callable[[str], None]] = None,
        progress_callback: Optional[Callable[[float, str], None]] = None
    ) -> str:
        """Execute resilient multi-audio download pipeline with auto-conflict resolution."""
        self._is_aborted = False

        def log(msg: str):
            if log_callback:
                log_callback(msg)
            else:
                print(msg, flush=True)

        log("=" * 65)
        log("🚀 ULTRA DOWNLOADER - MULTI-AUDIO ENGINE")
        log("=" * 65)

        # 1. Dependency Verification
        log("[1/4] Verifying required binaries (N_m3u8DL-RE & FFmpeg)...")
        n_m3u8_path, ffmpeg_path = ensure_dependencies(
            status_callback=log,
            progress_callback=progress_callback
        )

        # 2. Input Parsing
        log("[2/4] Parsing stream URL and security headers...")
        info = self.parse_input(input_text)
        if not info["url"]:
            raise ValueError("Invalid stream input. Please paste a cURL command or direct M3U8 link.")

        log(f"  • Source URL: {info['url'][:75]}...")
        log(f"  • Referer:    {info['referer']}")

        # Auto-detect clean title or generate unique filename
        if not save_name:
            id_match = re.search(r'(\d{6,10})', info["url"])
            if id_match:
                save_name = f"Video_{id_match.group(1)}"
            else:
                save_name = f"Video_{int(time.time())}"

        # Sanitize save name
        save_name = re.sub(r'[\\/*?:"<>|]', "", save_name).strip().replace(" ", "_")
        if not save_name:
            save_name = f"Video_{int(time.time())}"

        # Resolve duplicate filenames in the same destination folder
        base_name = save_name
        counter = 1
        while os.path.exists(os.path.join(save_dir, f"{save_name}.mkv")):
            save_name = f"{base_name}_{counter}"
            counter += 1

        log(f"  • Output Name: {save_name}.mkv")
        log(f"  • Destination: {save_dir}")

        # 3. Master Playlist Fetching
        log("[3/4] Fetching playlist metadata...")
        temp_dir = os.path.join(save_dir, f".ultra_tmp_{os.getpid()}_{int(time.time())}")
        try:
            target_source = self.fetch_master_playlist(info, temp_dir)
            log(f"  • Cached master playlist successfully ({os.path.getsize(target_source)} bytes).")
        except Exception as e:
            log(f"  • Direct network streaming fallback ({e})")
            target_source = info["url"]

        # Video Filter
        if resolution == "1080p":
            video_sel = "res=1920*:for=best"
        elif resolution == "720p":
            video_sel = "res=1280*:for=best"
        elif resolution == "480p":
            video_sel = "res=854*:for=best"
        else:
            video_sel = "best"

        # Audio Filter
        if audio_choice == "all":
            audio_sel = "all"
        elif audio_choice == "en_hi":
            audio_sel = "lang=en|hin:for=all"
        elif audio_choice == "eng":
            audio_sel = "lang=en:for=best"
        elif audio_choice == "hin":
            audio_sel = "lang=hin:for=best"
        else:
            audio_sel = "all"

        # Construct N_m3u8DL-RE Command with --auto-select (Mandatory for non-interactive execution)
        cmd = [
            n_m3u8_path,
            target_source,
            "--auto-select",
            "-sv", video_sel,
            "-sa", audio_sel,
            "--save-dir", save_dir,
            "--save-name", save_name,
            "-M", "format=mkv:muxer=ffmpeg",
            "--ffmpeg-binary-path", ffmpeg_path,
            "--thread-count", "16",
            "--download-retry-count", "10",
            "--check-segments-count", "false",
            "-H", f"Referer: {info['referer']}",
            "-H", f"Origin: {info['origin']}",
            "-H", f"User-Agent: {info['user_agent']}",
            "--no-ansi-color"
        ]

        log("[4/4] Starting multi-threaded download engine (16 parallel workers)...")
        log("-" * 65)

        self.current_process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            encoding="utf-8",
            errors="replace"
        )

        final_mkv = os.path.join(save_dir, f"{save_name}.mkv")

        last_progress_update = 0.0
        for line in iter(self.current_process.stdout.readline, ''):
            if self._is_aborted:
                log("\n[ABORTED] Download cancelled by user.")
                break

            line = line.strip()
            if not line:
                continue

            # Parse progress percentage
            pct_match = re.search(r'(\d+(?:\.\d+)?)%', line)
            now = time.time()
            if pct_match and progress_callback and (now - last_progress_update > 0.15):
                try:
                    pct = float(pct_match.group(1))
                    progress_callback(pct, line[:90])
                    last_progress_update = now
                except Exception:
                    pass

            # Log meaningful events and errors without flooding the UI queue
            is_important = any(k in line for k in ["Vid", "Aud", "INFO", "WARN", "ERROR", "Exception", "Mux", "Merging", "Done"])
            if is_important:
                log(f"  {line}")

        self.current_process.stdout.close()
        self.current_process.wait()

        # Clean cache
        if os.path.exists(temp_dir):
            try:
                shutil.rmtree(temp_dir, ignore_errors=True)
            except Exception:
                pass

        if self._is_aborted:
            raise RuntimeError("Operation aborted by user.")

        if self.current_process.returncode == 0 and os.path.exists(final_mkv):
            log("=" * 65)
            log(f"🎉 [SUCCESS] Download & Muxing Complete!")
            log(f"📁 Output File: {final_mkv}")
            log(f"📦 File Size:   {os.path.getsize(final_mkv) / (1024*1024):.2f} MB")
            log("=" * 65)
            if progress_callback:
                progress_callback(100.0, "Download Finished Successfully!")
            return final_mkv
        else:
            raise RuntimeError(f"Engine failed with return code {self.current_process.returncode}. Check output logs above for details.")
