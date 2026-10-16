"""
NetMirror Ultra Multi-Audio Video Downloader - Core Engine
Handles parsing, master playlist retrieval, multi-threading, and ffmpeg muxing.
100% English code, comments, and logging.
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
        """Abort currently active download process."""
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
        """Extract URL, headers, and metadata from cURL command or raw URL string."""
        text = raw_text.strip()
        url = ""
        headers = {}

        if "curl" in text.lower():
            # Clean Windows command prompt escape sequences
            cleaned = text.replace('^"', '"').replace('^&', '&').replace('^^', '^').replace('^', '')
            
            # Extract URL
            url_match = re.search(r'(?:--url|-u)?\s*["\']?(https?://[^\s"\']+)["\']?', cleaned, re.IGNORECASE)
            if url_match:
                url = url_match.group(1).rstrip('"\'')
                
            # Extract Headers
            header_matches = re.findall(r'-H\s*["\']([^"\']+)["\']', cleaned, re.IGNORECASE)
            for h in header_matches:
                if ":" in h:
                    k, v = h.split(":", 1)
                    headers[k.strip().lower()] = v.strip()
        else:
            url_match = re.search(r'https?://[^\s"\']+', text)
            if url_match:
                url = url_match.group(0).rstrip('"\'')

        # Fallback values
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
        """Download master playlist to a local file to bypass escaping/token issues."""
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
            raise RuntimeError(f"Failed to fetch master playlist from: {url}")

        with open(local_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read(500)
            if "Only Valid Users Allowed" in content or "403 Forbidden" in content or "<html" in content.lower():
                raise RuntimeError(f"Server rejected token or access: {content.strip()[:120]}")

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
        """Execute full multi-audio download pipeline."""
        self._is_aborted = False

        def log(msg: str):
            if log_callback:
                log_callback(msg)
            else:
                print(msg, flush=True)

        log("=" * 65)
        log("🎬 NETMIRROR MULTI-AUDIO DOWNLOADER - HIGH-SPEED ENGINE")
        log("=" * 65)

        # 1. Ensure Dependencies
        log("[1/4] Checking and verifying dependencies...")
        n_m3u8_path, ffmpeg_path = ensure_dependencies(
            status_callback=log,
            progress_callback=progress_callback
        )

        # 2. Parse Input
        log("[2/4] Parsing input stream specifications...")
        info = self.parse_input(input_text)
        if not info["url"]:
            raise ValueError("Invalid input. Please provide a valid M3U8 URL or cURL command.")

        log(f"  • Source URL: {info['url'][:75]}...")
        log(f"  • Referer:    {info['referer']}")

        # Determine Save Name
        if not save_name:
            id_match = re.search(r'(\d{6,10})', info["url"])
            if id_match:
                save_name = f"Movie_NetMirror_{id_match.group(1)}"
            else:
                save_name = f"Movie_NetMirror_{int(time.time())}"

        save_name = re.sub(r'[\\/*?:"<>|]', "", save_name).strip().replace(" ", "_")
        log(f"  • Output Filename: {save_name}.mkv")
        log(f"  • Target Directory: {save_dir}")

        # 3. Retrieve Playlist
        log("[3/4] Resolving master playlist streams...")
        temp_dir = os.path.join(save_dir, ".netmirror_cache")
        try:
            target_source = self.fetch_master_playlist(info, temp_dir)
            log(f"  • Master playlist cached locally ({os.path.getsize(target_source)} bytes).")
        except Exception as e:
            log(f"  • Note: Direct streaming mode fallback ({e})")
            target_source = info["url"]

        # Build Video Selection Filter
        if resolution == "1080p":
            video_sel = "res=1920*:for=best"
        elif resolution == "720p":
            video_sel = "res=1280*:for=best"
        elif resolution == "480p":
            video_sel = "res=854*:for=best"
        else:
            video_sel = "best"

        # Build Audio Selection Filter
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

        # 4. Construct Command
        cmd = [
            n_m3u8_path,
            target_source,
            "-sv", video_sel,
            "-sa", audio_sel,
            "--save-dir", save_dir,
            "--save-name", save_name,
            "-M", "format=mkv:muxer=ffmpeg",
            "--ffmpeg-binary-path", ffmpeg_path,
            "--thread-count", "16",
            "--download-retry-count", "10",
            "-H", f"Referer: {info['referer']}",
            "-H", f"Origin: {info['origin']}",
            "-H", f"User-Agent: {info['user_agent']}",
            "--no-ansi-color"
        ]

        log("[4/4] Launching multi-threaded downloader with 16 connections...")
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

        for line in iter(self.current_process.stdout.readline, ''):
            if self._is_aborted:
                log("\n[ABORTED] Download cancelled by user.")
                break

            line = line.strip()
            if not line:
                continue

            # Update progress if percentage found
            pct_match = re.search(r'(\d+\.\d+)%', line)
            if pct_match and progress_callback:
                try:
                    pct = float(pct_match.group(1))
                    progress_callback(pct, line)
                except Exception:
                    pass

            if any(k in line for k in ["Vid", "Aud", "INFO", "WARN", "Mux", "Merging", "%"]):
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
                progress_callback(100.0, "Completed!")
            return final_mkv
        else:
            raise RuntimeError(f"Process terminated with exit code {self.current_process.returncode}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        engine = DownloadEngine()
        engine.run_download(" ".join(sys.argv[1:]))
    else:
        print("Usage: python core_engine.py \"<cURL_or_M3U8_URL>\"")
