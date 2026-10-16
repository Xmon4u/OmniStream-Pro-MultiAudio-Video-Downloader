# NetMi.Video Downloader

**Professional multi-audio HLS/M3U8 stream downloader for Windows.**

Automatically downloads 1080p video with **all audio language tracks** muxed
into a single `.mkv` file using [N_m3u8DL-RE](https://github.com/nilaoda/N_m3u8DL-RE)
and [FFmpeg](https://ffmpeg.org/) — both auto-downloaded on first run.

---

## Features

- **Multi-audio MKV** — all language tracks downloaded and muxed automatically
- **1080p by default** — also supports 720p, 480p, or best available
- **cURL import** — paste any cURL command copied from DevTools
- **No installation** — single portable `.exe`, no Python required
- **Auto-dependency setup** — N_m3u8DL-RE and FFmpeg fetched automatically
- **Real-time log** — live terminal output while downloading
- **Abort support** — stop the download at any time

---

## Supported Sites

| Site | Status |
|------|--------|
| net52.cc | ✅ Tested |
| net77.cc | ✅ Tested |
| freecdn1.top | ✅ Tested |
| Any HLS/M3U8 stream | ✅ Should work |

---

## How to Use

### Option A — Download the .exe (Recommended)

1. Go to [**Releases**](https://github.com/Xmon4u/NetMirror-MultiAudio-Downloader/releases)
2. Download `NetMi_Video_Downloader.exe`
3. Run it — no installation needed

### Option B — Run from source

```bash
pip install customtkinter pillow
python main_gui.py
```

---

## Usage

1. Open the video in your browser
2. Press `F12` → **Network** tab → find the `.m3u8` request
3. Right-click the request → **Copy as cURL**
4. Paste into NetMi.Video Downloader
5. Set title and save folder (optional)
6. Click **▶ Start Download**

Files are saved as `<Title>.mkv` on your Desktop by default.

---

## Build from Source

```bash
pip install pyinstaller customtkinter pillow
python build_exe.py
```

Output: `dist/NetMi_Video_Downloader.exe`

---

## Project Structure

```
NetMi.Video Downloader/
├── main_gui.py           # CustomTkinter UI (NetMiApp)
├── core_engine.py        # Download engine (N_m3u8DL-RE + FFmpeg)
├── setup_dependencies.py # Auto-downloads N_m3u8DL-RE and FFmpeg
├── build_exe.py          # PyInstaller build script
├── app_icon.ico          # App icon (Windows)
└── app_icon.png          # App icon (PNG)
```

---

## Requirements (source)

- Python 3.10+
- `customtkinter`, `pillow`

## Requirements (exe)

- Windows 10/11 x64
- Internet connection (for first-run dependency setup)

---

## Author

**XMON4U** — [github.com/Xmon4u](https://github.com/Xmon4u)

---

## License

MIT License — see [LICENSE](LICENSE)
