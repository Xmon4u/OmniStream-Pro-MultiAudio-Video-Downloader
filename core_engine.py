"""
NetMi.Video Downloader - Core Download Engine
High-performance multi-audio stream downloader using N_m3u8DL-RE and FFmpeg.
"""

import os
import re
import sys
import time
import shutil
import subprocess
from typing import Dict, Any, Optional, Callable

from setup_dependencies import ensure_dependencies

DEFAULT_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)
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
            # Unescape Windows cmd-style ^ quoting
            cleaned = (
                text
                .replace('^"', '"')
                .replace('^&', '&')
                .replace('^^', '^')
                .replace('^ ', ' ')
            )
            cleaned = re.sub(r'\^(?=[^\n])', '', cleaned)

            url_match = re.search(
                r'(?:--url|-u)?\s*["\']?(https?://[^\s"\'\\]+)["\']?',
                cleaned, re.IGNORECASE
            )
            if url_match:
                url = url_match.group(1).rstrip('"\'')

            header_matches = re.findall(r'-H\s+["\']([^"\']+)["\']', cleaned, re.IGNORECASE)
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
            "curl.exe", "-s", "-L", url,
            "-H", f"Referer: {info['referer']}",
            "-H", f"Origin: {info['origin']}",
            "-H", f"User-Agent: {info['user_agent']}",
            "--max-time", "25",
            "-o", local_path,
        ]

        res = subprocess.run(curl_cmd, capture_output=True, text=True, timeout=30)
        if res.returncode != 0 or not os.path.exists(local_path) or os.path.getsize(local_path) == 0:
            raise RuntimeError(f"Could not fetch playlist: {url}")

        with open(local_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read(600)

        if any(x in content for x in ["Only Valid Users", "403 Forbidden", "Access Denied"]) or \
           "<html" in content.lower():
            raise RuntimeError(
                "Session expired or access denied. Please paste a fresh cURL command."
            )

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

        sep = "-" * 60
        log(sep)
        log("  NetMi.Video Downloader - Multi-Audio Engine")
        log(sep)

        # Step 1: Dependency check
        log("[1/4] Verifying required binaries...")
        n_m3u8_path, ffmpeg_path = ensure_dependencies(
            status_callback=log,
            progress_callback=progress_callback,
        )

        # Step 2: Parse input
        log("[2/4] Parsing stream source...")
        info = self.parse_input(input_text)
        if not info["url"]:
            raise ValueError(
                "No valid stream URL detected. Paste a cURL command or direct M3U8 URL."
            )

        url_display = info['url'][:80] + ('...' if len(info['url']) > 80 else '')
        log(f"  Source : {url_display}")
        log(f"  Referer: {info['referer']}")

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

        log(f"  Output : {save_name}.mkv  ->  {save_dir}")

        # Step 3: Fetch playlist
        log("[3/4] Fetching stream playlist...")
        temp_dir = os.path.join(save_dir, f".netmi_tmp_{os.getpid()}_{int(time.time())}")
        try:
            target_source = self.fetch_master_playlist(info, temp_dir)
            log(f"  Playlist cached ({os.path.getsize(target_source):,} bytes).")
        except Exception as exc:
            log(f"  Warning: Playlist cache failed ({exc}). Using direct URL.")
            target_source = info["url"]

        # Video stream selector — N_m3u8DL-RE syntax: res=HEIGHTp or best
        res_map = {
            "1080p": "res=1080p",
            "720p":  "res=720p",
            "480p":  "res=480p",
            "best":  "best",
        }
        video_sel = res_map.get(resolution, "best")

        # Audio stream selector — 'all' downloads every language track available
        audio_sel_map = {
            "all":   "all",
            "en_hi": "lang=eng,hin",
            "eng":   "lang=eng",
            "hin":   "lang=hin",
        }
        audio_sel = audio_sel_map.get(audio_choice, "all")

        # Build N_m3u8DL-RE command
        cmd = [
            n_m3u8_path,
            target_source,
            "--auto-select",        # non-interactive: auto-pick if filter yields nothing
            "-sv", video_sel,
            "-sa", audio_sel,
            "-mt",                  # concurrent multi-track downloads
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
            "--no-ansi-color",
        ]

        log("[4/4] Starting download (16 parallel workers)...")
        log(sep)

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
        _keywords = (
            "Vid ", "Aud ", "INFO", "WARN", "ERROR", "Exception",
            "Mux", "Merging", "Done", "Fail", "success", "stream",
        )

        for line in iter(self.current_process.stdout.readline, ""):
            if self._is_aborted:
                log("[Aborted] Download cancelled by user.")
                break

            line = line.strip()
            if not line:
                continue

            # Update progress bar
            pct_match = re.search(r"(\d+(?:\.\d+)?)%", line)
            now = time.time()
            if pct_match and progress_callback and (now - last_progress_update > 0.2):
                try:
                    pct = float(pct_match.group(1))
                    progress_callback(pct, line[:100])
                    last_progress_update = now
                except Exception:
                    pass

            # Log only meaningful lines
            if any(k in line for k in _keywords):
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

        rc = self.current_process.returncode

        # Success: file exists and has content (some N_m3u8DL-RE builds exit non-zero on warnings)
        if os.path.exists(final_mkv) and os.path.getsize(final_mkv) > 0:
            size_mb = os.path.getsize(final_mkv) / (1024 * 1024)
            log(sep)
            log("  [SUCCESS] Download and mux complete!")
            log(f"  Output : {final_mkv}")
            log(f"  Size   : {size_mb:.2f} MB")
            log(sep)
            if progress_callback:
                progress_callback(100.0, "Download complete!")
            return final_mkv
        else:
            raise RuntimeError(
                f"Download failed (exit code {rc}). "
                "Check the terminal log above for details. "
                "If the session expired, paste a fresh cURL command."
            )
