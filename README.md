# OmniStream Pro

<div align="center">

![OmniStream Pro Icon](app_icon.png)

### Universal Multi-Audio HLS/M3U8 Stream Downloader & Multiplexer
**Enterprise-grade stream capture tool for Windows with concurrent multi-track audio preservation.**

[![Release](https://img.shields.io/badge/Release-v1.0.0-6366f1?style=for-the-badge&logo=github)](https://github.com/Xmon4u/OmniStream-Pro/releases)
[![Platform](https://img.shields.io/badge/Platform-Windows%2010%20%7C%2011-06b6d4?style=for-the-badge&logo=windows)](https://github.com/Xmon4u/OmniStream-Pro)
[![Python](https://img.shields.io/badge/Python-3.10%2B-10b981?style=for-the-badge&logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-f59e0b?style=for-the-badge)](LICENSE)

</div>

---

## ⚡ Overview

**OmniStream Pro** is a high-performance Windows desktop application built to capture complex adaptive HLS/M3U8 video streams and automatically mux **all available multi-language audio tracks** into a single, clean `.mkv` file. 

Powered by [N_m3u8DL-RE](https://github.com/nilaoda/N_m3u8DL-RE) and [FFmpeg](https://ffmpeg.org/), both binaries are automatically configured and downloaded on first launch—no manual setup required.

---

## ✨ Key Features

- **🎧 Lossless Multi-Audio MKV Muxing**: Downloads and muxes every audio track (English, Hindi, Bengali, etc.) directly into a single container with proper track metadata.
- **🚀 16x Parallel Segment Acceleration**: Leverages concurrent segment downloads (`-mt`) for maximum throughput.
- **📋 Intelligent cURL Importer**: Paste any raw `cURL (bash)` or `cURL (cmd)` copied directly from browser DevTools; headers, cookies, referers, and tokens are parsed automatically.
- **🖥️ Dynamic Video Quality**: Choose between Best Available, 1080p (Full HD), 720p (HD), 480p (SD), or Audio-Only.
- **🛡️ Auto-Dependency Management**: Automatically checks and downloads verified releases of `N_m3u8DL-RE` and `ffmpeg` if missing.
- **📊 Real-Time Activity Terminal**: Live logging console with progress bar, completion status, and log export.
- **🛑 Safe Abort Handling**: Stop and clean up any ongoing download instantly at any moment.
- **📦 100% Portable**: Single standalone executable, no installation or admin rights required.

---

## 🌐 Supported Sites

| Site | Status |
|------|--------|
| `net52.cc` | ✅ Tested |
| `net77.cc` | ✅ Tested |
| `freecdn1.top` | ✅ Tested |
| Any HLS/M3U8 stream | ✅ Should work |

---

## 🚀 Getting Started

### Option A: Standalone Executable (Recommended)

1. Head over to [**GitHub Releases**](https://github.com/Xmon4u/OmniStream-Pro/releases).
2. Download `OmniStream_Pro.exe` from the latest **v1.0.0** release.
3. Double-click to launch—ready out of the box!

### Option B: Run from Source

```bash
# Clone the repository
git clone https://github.com/Xmon4u/OmniStream-Pro.git
cd OmniStream-Pro

# Install Python requirements
pip install customtkinter pillow

# Launch the modern GUI
python main_gui.py
```

---

## 📖 How to Download Streams

1. Open your target stream or video in Google Chrome, Edge, or Brave.
2. Press `F12` to open **Developer Tools** and navigate to the **Network** tab.
3. Filter by `m3u8`.
4. Right-click the master playlist request ➔ **Copy** ➔ **Copy as cURL**.
5. Open **OmniStream Pro** and click **📋 Paste**.
6. (Optional) Customize the video title, quality preset, or audio tracks.
7. Click **▶ Start Download & Mux**.
8. Your output file will be saved directly to your chosen folder (Desktop by default) as a clean `.mkv` file.

---

## 🛠️ Build Standalone Executable

To compile your own single-file `.exe`:

```bash
pip install pyinstaller customtkinter pillow
python build_exe.py
```

The resulting executable will be placed in `dist/OmniStream_Pro.exe` and copied to your Desktop.

---

## 📂 Project Architecture

```
OmniStream Pro/
├── app_icon.ico             # Windows multi-resolution icon (16x16 to 256x256)
├── app_icon.png             # High-resolution application artwork
├── bridge_server.py         # Localhost browser extension bridge server
├── build_exe.py             # PyInstaller one-file compilation pipeline
├── core_engine.py           # Stream parsing, download manager & FFmpeg muxer
├── generate_icon.py         # High-definition icon rendering script
├── main_gui.py              # CustomTkinter dark-mode desktop interface
├── setup_dependencies.py    # Automated portable binary downloader
├── Start_OmniStream_Pro.bat # Quick launcher batch script
├── LICENSE                  # MIT Open Source License
└── README.md                # Documentation
```

---

## 👤 Author

**XMON4U**
- GitHub: [@Xmon4u](https://github.com/Xmon4u)

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
