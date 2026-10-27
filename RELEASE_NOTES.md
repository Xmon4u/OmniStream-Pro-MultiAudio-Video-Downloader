# OmniStream Pro Release Notes

## Version 2.0.0

### Highlights
- **Browser-to-Desktop Link Forwarding**: Added local HTTP bridge (`localhost:28795`) allowing instant link dispatch from Chromium browsers into the desktop queue.
- **Batch Download Queue**: Added queue management system to process multiple streams sequentially with individual item controls.
- **Multi-Track Audio Muxing**: Preserves all audio stream languages and multiplexes them cleanly into a single `.mkv` file with language tags.
- **cURL Header Parsing**: Automatic extraction of cookies, User-Agent, and Referer headers from raw cURL commands copied from DevTools.
- **Automatic Tool Setup**: Added automatic downloading and verification of `N_m3u8DL-RE` and `ffmpeg` binaries.

---

## Version 1.0.0

- Initial release featuring single-stream HLS/M3U8 downloading and MKV container output.
