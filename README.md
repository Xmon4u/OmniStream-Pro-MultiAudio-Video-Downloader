# OmniStream Pro — Multi-Audio HLS/M3U8 Downloader

[![Release](https://img.shields.io/github/v/release/Xmon4u/OmniStream-Pro-MultiAudio-Video-Downloader?label=Release)](https://github.com/Xmon4u/OmniStream-Pro-MultiAudio-Video-Downloader/releases)
[![Platform](https://img.shields.io/badge/Platform-Windows%2010%20%7C%2011-blue.svg)](https://github.com/Xmon4u/OmniStream-Pro-MultiAudio-Video-Downloader)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A Windows desktop application for downloading HLS/M3U8 video streams with multi-language audio track preservation and automated MKV multiplexing.

## Overview

OmniStream Pro captures adaptive streaming media (HLS playlists) and direct video streams. It connects with the companion [OmniStream Chrome Extension](https://github.com/Xmon4u/OmniStream-Pro-Chrome-Extension) over a local bridge, allowing one-click stream forwarding directly from your browser. 

The application downloads video and audio segments concurrently using `N_m3u8DL-RE` and multiplexes them into a single container using `FFmpeg`.

## Features

- **Batch Download Queue**: Links sent from the browser extension or pasted manually are queued automatically. Download items individually or run the full queue sequentially.
- **Multi-Track Audio Muxing**: Downloads all available audio tracks (different languages or commentaries) and bundles them into an `.mkv` file with appropriate metadata tags.
- **Parallel Segment Downloads**: Utilizes concurrent chunk requests via `N_m3u8DL-RE` to maximize connection bandwidth.
- **Dual Stream Engine**: Supports adaptive playlists (`.m3u8`, `.mpd`) as well as direct media files (`.mp4`, `.mkv`, `.webm`, `.mp3`).
- **cURL Importer**: Paste raw `curl` commands directly from browser DevTools; authentication cookies, referers, and request headers are parsed automatically.
- **Automatic Dependency Setup**: Automatically downloads and checks for required CLI tools (`N_m3u8DL-RE` and `ffmpeg`) on initial launch if not found locally.
- **Console Activity Log**: Embedded log window showing command output, download speed, and error notifications.
- **Clean Cancellation**: Cancel running downloads safely without leaving corrupted partial files behind.

## Getting Started

### Standalone Executable (Windows)
1. Download `OmniStream_Pro.exe` from [GitHub Releases](https://github.com/Xmon4u/OmniStream-Pro-MultiAudio-Video-Downloader/releases).
2. Run the executable. No manual dependencies setup is needed.

### Running from Source

#### Prerequisites
- Windows 10 or 11
- Python 3.10+
- `pip`

```bash
# Clone the repository
git clone https://github.com/Xmon4u/OmniStream-Pro-MultiAudio-Video-Downloader.git
cd OmniStream-Pro-MultiAudio-Video-Downloader

# Install Python UI framework
pip install customtkinter

# Run the application
python main.py
```

## Browser Extension Integration

To send stream links directly from Chrome or Edge:
1. Install the [OmniStream Pro Extension](https://github.com/Xmon4u/OmniStream-Pro-Chrome-Extension).
2. Start the OmniStream Pro desktop application (the background listener opens on `http://127.0.0.1:28795`).
3. Click **Send to App** in the extension popup when a stream is detected.

## Project Structure

```text
OmniStream-Pro-MultiAudio-Video-Downloader/
├── assets/                 # Icons and theme assets
├── bin/                    # Auto-downloaded helper binaries (N_m3u8DL-RE, ffmpeg)
├── extension/              # Packaged browser extension files
├── main.py                 # Desktop GUI and queue controller
├── bridge.py               # Localhost HTTP listener for extension requests
├── downloader.py           # Process orchestration for N_m3u8DL-RE & ffmpeg
├── RELEASE_NOTES.md        # Version history
└── README.md
```

## License

This project is licensed under the [MIT License](LICENSE).
