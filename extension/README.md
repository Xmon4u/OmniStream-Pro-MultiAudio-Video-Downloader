# OmniStream Pro — Browser Extension

A Chromium browser extension designed to capture HLS playlists and transfer them to the OmniStream Pro desktop downloader.

## Features

- **Desktop Bridge**: Forwards detected streams and authentication headers directly to the desktop queue at `127.0.0.1:28795`.
- **Stream Detection**: Sniffs web requests to isolate `.m3u8` master and variant playlists from background network traffic.
- **DOM Scanner**: Inspects active media elements and scripts on pages where video sources are loaded asynchronously.
- **cURL Export**: Copies complete terminal-ready cURL commands with current session cookies and headers.

## Installation

1. Open `chrome://extensions` (or `edge://extensions`) in your browser.
2. Enable **Developer mode**.
3. Click **Load unpacked** and select this `extension/` directory.

## License

MIT License.
