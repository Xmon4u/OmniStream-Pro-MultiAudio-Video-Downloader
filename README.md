# NetMirror Multi-Audio Downloader

[![Release](https://img.shields.io/github/v/release/Xmon4u/NetMirror-MultiAudio-Downloader?color=38bdf8&style=flat-square)](https://github.com/Xmon4u/NetMirror-MultiAudio-Downloader/releases)
[![Platform](https://img.shields.io/badge/Platform-Windows-0284c7?style=flat-square&logo=windows)](https://github.com/Xmon4u/NetMirror-MultiAudio-Downloader)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

A lightweight, portable Windows desktop utility built to rip and download full 1080p videos alongside **all multi-language audio tracks** (English, Hindi, Spanish, German, Japanese, etc.) from NetMirror mirrors (`net52.cc`, `net77.cc`, `freecdn1.top`).

The app automatically combines all extracted audio channels with the high-resolution video into a clean `.mkv` container using FFmpeg, ready for VLC or MPC-HC with switchable audio tracks.

---

## ✨ Features

- **Multi-Track Audio Muxing**: Grabs every audio language available on the master playlist (up to 15+ tracks) and muxes them into a single MKV file.
- **Zero Configuration Required**: On first launch, the app automatically checks for `N_m3u8DL-RE` and `FFmpeg`. If not present on your system, it automatically downloads and configures them in the background.
- **Modern Dark UI**: Clean, responsive desktop interface built with CustomTkinter. Includes real-time progress bars, speed monitors, and live terminal logging.
- **Multi-Threaded Ripping**: Spawns up to 16 concurrent segment download workers for maximum network throughput.
- **cURL & M3U8 Auto-Detection**: Accepts raw cURL commands copied straight from browser DevTools, parsing all necessary headers, referers, and temporary session tokens automatically.

---

## 📥 Download & Quick Start

1. Go to the [**Releases**](https://github.com/Xmon4u/NetMirror-MultiAudio-Downloader/releases) page.
2. Download **`NetMirror_MultiAudio_Downloader.exe`**.
3. Double-click to run (no installation needed).

---

## 📖 How to Use

### Step 1: Copy Stream Link from Browser
1. In your browser (Chrome / Edge / Brave), navigate to **net52.cc** or **net77.cc** and play the movie/episode.
2. Press `F12` to open **Developer Tools** and switch to the **Network** tab.
3. In the filter box, type `m3u8`.
4. Right-click the master playlist request (e.g., `70307658.m3u8` or `1080p.m3u8`):
   - Choose **Copy** ➔ **Copy as cURL (cmd)** *(or "Copy link address")*.

### Step 2: Download
1. Open **NetMirror Multi-Audio Downloader**.
2. Click **📋 Paste Clipboard**.
3. Select your desired resolution (`1080p`, `720p`, `480p`) and audio preference (`All Audio Tracks` or specific languages).
4. Click **🚀 START MULTI-AUDIO DOWNLOAD**.

Once finished, click **📁 Open Folder** to find your `.mkv` file ready to play!

---

## 🛠️ Running from Source

If you prefer running the Python script directly instead of using the pre-compiled `.exe`:

### Prerequisites
- Python 3.10 or higher
- Git

### Installation
```bash
# Clone the repository
git clone https://github.com/Xmon4u/NetMirror-MultiAudio-Downloader.git
cd NetMirror-MultiAudio-Downloader

# Install Python requirements
pip install customtkinter pillow pyinstaller
```

### Run the App
```bash
python main_gui.py
```

### Build Executable
```bash
python build_exe.py
```
The compiled single-file binary will be placed in the `dist/` directory.

---

## ⚖️ License

Distributed under the [MIT License](LICENSE).

---

## ⚠️ Disclaimer

This tool is created for educational and personal archival purposes only. Users are solely responsible for ensuring compliance with all local laws and terms of service of any third-party websites accessed.
