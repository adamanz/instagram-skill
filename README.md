# Instagram Skill for OpenClaw

Download, analyze, and share Instagram Reels/videos via yt-dlp.

## Features
- Download public reels/posts without login
- Auto-transcode VP9→H.264 for Telegram compatibility
- Extract metadata (uploader, views, likes, description)
- Frame extraction for vision analysis

## Usage

```bash
# Get metadata
python3 scripts/ig.py info "https://www.instagram.com/reel/XXXXX/"

# Download (auto-transcodes for Telegram)
python3 scripts/ig.py download "https://www.instagram.com/reel/XXXXX/"

# Download + prep for vision analysis
python3 scripts/ig.py watch "https://www.instagram.com/reel/XXXXX/"
```

## Requirements
- yt-dlp (`brew install yt-dlp`)
- ffmpeg (`brew install ffmpeg`)

## License
MIT
