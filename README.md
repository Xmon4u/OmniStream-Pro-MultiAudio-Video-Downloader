# OmniStream Pro — Multi-Audio HLS/M3U8 Video Downloader

<div align="center">

[![Release](https://img.shields.io/badge/Release-v1.0.0-6366f1?style=for-the-badge&logo=github)](https://github.com/Xmon4u/OmniStream-Pro-MultiAudio-Video-Downloader/releases)
[![Platform](https://img.shields.io/badge/Platform-Windows%2010%20%7C%2011-06b6d4?style=for-the-badge&logo=windows)](https://github.com/Xmon4u/OmniStream-Pro-MultiAudio-Video-Downloader)
[![License](https://img.shields.io/badge/License-MIT-f59e0b?style=for-the-badge)](LICENSE)

</div>

---

## Overview

**OmniStream Pro** is a Windows desktop application for downloading HLS/M3U8 video streams with full multi-language audio track preservation.

It integrates with the [OmniStream Pro Chrome Extension](https://github.com/Xmon4u/OmniStream-Pro-Chrome-Extension) to receive stream URLs and headers directly from your browser, then downloads all video segments and audio tracks concurrently, muxing them into a single lossless `.mkv` file.

---

## Key Features

- **Batch Queue (IDM-style)**: Links sent from the extension or pasted manually are queued automatically. Click **Download All** to process the entire queue sequentially.
- **Lossless Multi-Audio MKV Muxing**: Downloads and muxes every audio track (English, Hindi, and others) into a single container with proper language track metadata.
- **16x Parallel Segment Downloads**: Uses concurrent segment downloading via N_m3u8DL-RE for maximum bandwidth utilization.
- **Dual-Mode Engine**: Supports adaptive playlists (`.m3u8`, `.mpd`) and direct streaming files (`.mp4`, `.mkv`, `.webm`, `.mp3`).
- **cURL Importer**: Paste any `cURL (bash)` or `cURL (cmd)` command from browser DevTools; headers, cookies, referers, and tokens are parsed automatically.
- **Auto-Dependency Management**: Automatically downloads verified releases of `N_m3u8DL-RE` and `ffmpeg` if they are not found.
- **Live Activity Terminal**: Real-time logging console with progress bar, completion status, and log export.
- **Safe Abort**: Stop any ongoing download immediately without leaving corrupt files.

---

## Getting Started

### Option A: Standalone Executable
1. Download `OmniStream_Pro.exe` from [GitHub Releases](https://github.com/Xmon4u/OmniStream-Pro-MultiAudio-Video-Downloader/releases).
2. Double-click to launch.

### Option B: Run from Source
```bash
git clone https://github.com/Xmon4u/OmniStream-Pro-MultiAudio-Video-Downloader.git
cd OmniStream-Pro-MultiAudio-Video-Downloader

pip install customtkinter
python main_gui.py
```

---

## How to Download Streams

1. Launch **OmniStream Pro** desktop application.
2. In your browser, open any website with video content and play the video.
3. Click the **OmniStream Pro** extension icon.
4. Click **Send All to App** to transfer all detected streams to the desktop app at once.
5. In OmniStream Pro, streams appear in the download queue.
6. Click **Download All (Start Queue)**.

OmniStream Pro downloads all video segments and audio tracks concurrently, muxing each into a lossless `.mkv` file in your chosen output folder.

---

## Building from Source (.exe)

```bash
python build_exe.py
```

The compiled binary will be placed at `dist/OmniStream_Pro.exe`.

---

## Project Structure

```
OmniStream-Pro-MultiAudio-Video-Downloader/
├── main_gui.py              # CustomTkinter desktop application
├── core_engine.py           # Multi-audio download manager & FFmpeg muxer
├── bridge_server.py         # Localhost browser bridge server (127.0.0.1:28795)
├── setup_dependencies.py    # Auto-downloader for N_m3u8DL-RE and FFmpeg
├── build_exe.py             # PyInstaller one-file executable builder
├── app_icon.ico             # Windows application icon
├── app_icon.png             # Application logo
└── README.md                # Documentation
```

---

## Author

**XMON4U** — [GitHub: @Xmon4u](https://github.com/Xmon4u)

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
