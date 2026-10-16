# Ultra Downloader - Multi-Audio Edition

[![Release](https://img.shields.io/github/v/release/Xmon4u/NetMirror-MultiAudio-Downloader?color=38bdf8&style=flat-square)](https://github.com/Xmon4u/NetMirror-MultiAudio-Downloader/releases)
[![Platform](https://img.shields.io/badge/Platform-Windows-0284c7?style=flat-square&logo=windows)](https://github.com/Xmon4u/NetMirror-MultiAudio-Downloader)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python)](https://python.org)
[![Developer](https://img.shields.io/badge/Developer-XMON4U-f43f5e?style=flat-square)](https://github.com/Xmon4u)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

**Ultra Downloader** is a high-speed, portable Windows utility built to download full **1080p Full HD video** streams along with **all multi-language audio tracks** (English, Hindi, Spanish, German, Japanese, French, Korean, etc.) from modern media streaming servers.

It automatically extracts, downloads, and multiplexes all audio channels into a clean `.mkv` container using FFmpeg, ready for instant playback in VLC or MPC-HC with switchable audio tracks.

---

## ✨ Features

- **Multi-Track Audio Multiplexing**: Captures every audio track available in the master stream (up to 30+ language streams) and packages them together.
- **Zero Configuration / Auto-Bootstrapper**: Automatically checks for `N_m3u8DL-RE` and `FFmpeg`. If missing on any target machine, it automatically fetches and installs them in the background.
- **Modern Dark UI**: Windows 11 style dark interface powered by CustomTkinter, featuring real-time speed monitoring, progress tracking, and non-blocking terminal logs.
- **Auto-Conflict & Duplicate Resolution**: Automatically handles file name collisions so subsequent downloads in the same folder never freeze or fail.
- **cURL Command & M3U8 Auto-Detection**: Paste direct cURL commands copied from browser Developer Tools (F12) to bypass session tokens and referer checks.
- **16 Multi-Threaded Workers**: Parallel chunk retrieval for maximum download speeds.

---

## 📥 Download & Quick Start

1. Go to the [**Releases**](https://github.com/Xmon4u/NetMirror-MultiAudio-Downloader/releases) page.
2. Download **`Ultra_Downloader_MultiAudio.exe`**.
3. Double-click to launch (standalone, no installation required).

---

## 📖 How to Use

### Step 1: Copy Stream Link from Browser
1. In your browser (Chrome / Edge / Brave), navigate to your streaming page and hit play.
2. Press **`F12`** to open **Developer Tools** and switch to the **Network** tab.
3. In the filter box, type **`m3u8`**.
4. Right-click the master playlist request (e.g. `*.m3u8` or `1080p.m3u8`):
   - Select **Copy** ➔ **Copy as cURL (cmd)** *(or "Copy link address")*.

### Step 2: Download
1. Launch **Ultra Downloader**.
2. Click **📋 Paste Clipboard**.
3. (Optional) Provide a custom movie title, target resolution, and audio preference.
4. Click **🚀 START MULTI-AUDIO DOWNLOAD**.

When completed, click **📁 Open Folder** to play your multi-audio `.mkv` file!

---

## 🛠️ Building from Source

```bash
# Clone the repository
git clone https://github.com/Xmon4u/NetMirror-MultiAudio-Downloader.git
cd NetMirror-MultiAudio-Downloader

# Install dependencies
pip install customtkinter pillow pyinstaller

# Run GUI
python main_gui.py

# Build single-file EXE with icon
python build_exe.py
```

---

## 👨‍💻 Developer & Credits

- **Developer:** [XMON4U](https://github.com/Xmon4u)
- **GitHub:** [github.com/Xmon4u](https://github.com/Xmon4u)

---

## ⚖️ License

Distributed under the [MIT License](LICENSE).
