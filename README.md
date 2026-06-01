# YT-DLP Video Downloader

> **One-click video downloader for 1000+ websites** — YouTube, Twitter/X, TikTok, Instagram, Facebook, Reddit, and more.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![yt-dlp](https://img.shields.io/badge/powered%20by-yt--dlp-red.svg)](https://github.com/yt-dlp/yt-dlp)

A browser extension + Python backend that brings the power of [yt-dlp](https://github.com/yt-dlp/yt-dlp) to your browser toolbar. No command line needed. Just click, choose quality, and download.

![Extension Popup](screenshots/extension-popup.png)

## Features

- **One-click downloads** from any website while you browse
- **1000+ supported sites** — anything yt-dlp supports (YouTube, TikTok, Twitter, Instagram, etc.)
- **Multiple formats** — Best Quality, 1080p, 720p, or Audio-only MP3
- **Live progress bar** — See download %, speed, and ETA in real-time
- **Background downloads** — Close the popup, download keeps running
- **Custom save location** — Choose any folder via Advanced Settings
- **Auto-start option** — Server starts automatically with Windows
- **Dark theme UI** — Clean, modern interface

## Screenshots

| Extension Popup | Download Progress | Advanced Settings |
|:---:|:---:|:---:|
| ![Popup](screenshots/extension-popup.png) | ![Progress](screenshots/download-progress.png) | ![Settings](screenshots/extension-settings.png) |

## Quick Start (3 Steps)

### 1. Start the Backend Server

**Option A — Auto-start forever (Recommended):**
```bash
Double-click: Add_to_Startup.bat
```
- Server runs silently in background on every Windows boot
- No black CMD window ever appears

**Option B — Manual start:**
```bash
Double-click: Start_Server.bat
```
- Keep the window open while browsing

### 2. Install the Browser Extension

1. Open Chrome/Edge and go to `chrome://extensions/`
2. Turn ON **"Developer mode"** (toggle top-right)
3. Click **"Load unpacked"**
4. Select the `extension/` folder from this repo
5. Pin the extension to your toolbar (click puzzle icon → Pin)

### 3. Download Any Video

1. Go to any website with a video
2. Click the **YT-DLP** icon in your toolbar
3. Select format: **Best / 1080p / 720p / MP3**
4. Click **Download Video**
5. Watch progress in the popup — file saves automatically

## System Requirements

| Requirement | How to check / install |
|---|---|
| **Windows 10/11** | Required for batch scripts |
| **Python 3.8+** | [python.org](https://www.python.org/downloads/) — Check "Add to PATH" |
| **yt-dlp** | [Download yt-dlp.exe](https://github.com/yt-dlp/yt-dlp/releases) → place in Downloads folder |
| **Flask** | Auto-installed by `Start_Server.bat` |

## File Structure

```
YT-DLP-Video-Downloader/
├── extension/          # Browser extension (Chrome/Edge)
│   ├── manifest.json
│   ├── popup.html      # Download UI with progress bar
│   ├── popup.js        # URL detection + server communication
│   ├── options.html    # Settings page
│   └── background.js   # Service worker
├── backend/            # Python server
│   ├── yt-dlp-bridge.py    # Flask server, runs yt-dlp in background
│   └── requirements.txt    # Flask dependencies
├── Start_Server.bat        # Manual start (visible window)
├── Start_Background.bat    # Silent background start
├── Add_to_Startup.bat      # Auto-start on Windows login
├── Remove_from_Startup.bat # Remove auto-start
├── Stop_Server.bat         # Stop running server
├── Check_Server.bat        # Diagnose connection issues
└── Test_Server.html        # Browser connectivity test
```

## Supported Websites

Any site supported by [yt-dlp](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md), including:

- **YouTube** (videos, Shorts, playlists)
- **Twitter / X** (tweets with video)
- **TikTok** (videos, profiles)
- **Instagram** (posts, Reels, stories)
- **Facebook** (videos, reels)
- **Reddit** (videos, GIFs)
- **Twitch** (clips, VODs)
- **Vimeo**, **Dailymotion**, **Bilibili**, **SoundCloud**
- **1000+ more sites**

## Troubleshooting

| Problem | Solution |
|---|---|
| "Server offline" in extension | Run `Start_Server.bat` or `Add_to_Startup.bat` |
| "yt-dlp not found" | Download [yt-dlp.exe](https://github.com/yt-dlp/yt-dlp/releases) → place in Downloads folder |
| Download fails on a site | Some sites require cookies or have DRM. Check [yt-dlp docs](https://github.com/yt-dlp/yt-dlp/wiki) |
| Extension won't install | Make sure you selected the `extension/` folder, not individual files |
| Server crashes | Run `Check_Server.bat` to diagnose |

## Advanced Settings

Click **⚙ Advanced Settings** in the extension popup to configure:

- **Download directory** — Default is `Downloads`. Change to any folder (e.g., `D:\Videos`)
- **Default format** — Pre-select your preferred quality

Settings are saved to `backend/settings.json`.

## How It Works

```
Browser Extension → detects current URL → sends to local server
                                    ↓
Python Server (Flask) on localhost:8765
                                    ↓
Spawns yt-dlp process in background → parses real-time output
                                    ↓
Extension polls progress every 500ms → updates progress bar
                                    ↓
Video file saved to chosen directory
```

Everything stays **local** — no data leaves your computer.

## Contributing

Pull requests welcome! Areas to improve:
- Firefox support
- macOS/Linux compatibility
- Playlist auto-detection
- Thumbnail previews
- Download history

## License

[MIT](LICENSE) — free for personal and commercial use.

## Credits

- Built on [yt-dlp](https://github.com/yt-dlp/yt-dlp) — the most powerful video downloader
- Browser extension uses [Flask](https://flask.palletsprojects.com/) + [Flask-CORS](https://flask-cors.readthedocs.io/)

---

**Star ⭐ this repo if it helped you!**
