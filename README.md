# 📸 Instagram Skill for OpenClaw

> Download, transcode & analyze Instagram Reels and videos. No login required.

[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://clawhub.com)

## Install

```bash
# Add to your OpenClaw skills directory
git clone https://github.com/adamanz/instagram-skill.git ~/.openclaw/skills/instagram
```

Or add to your OpenClaw config:
```yaml
skills:
  - path: ~/.openclaw/skills/instagram
```

## Usage

```bash
# Get metadata (uploader, views, likes, description)
python3 scripts/ig.py info "https://www.instagram.com/reel/XXXXX/"

# Download video (auto-transcodes VP9→H.264 for Telegram)
python3 scripts/ig.py download "https://www.instagram.com/reel/XXXXX/"

# Download + prep for vision analysis
python3 scripts/ig.py watch "https://www.instagram.com/reel/XXXXX/"
```

## Features

- **No login required** for public content
- **Auto-transcode** VP9→H.264 for Telegram/messaging compatibility
- **Metadata extraction** — uploader, views, likes, description, duration
- **Vision-ready** — download + frame extraction for AI analysis
- **Private content** — supports cookie auth for private accounts

## Requirements

- `yt-dlp` — `brew install yt-dlp`
- `ffmpeg` — `brew install ffmpeg`

## How It Works

1. User shares an Instagram URL
2. Skill downloads via yt-dlp (no API key needed)
3. Auto-detects VP9 codec and transcodes to H.264
4. Returns Telegram-compatible video + metadata

## Keywords

`openclaw` `openclaw-skill` `instagram` `reels` `video` `download` `yt-dlp` `telegram`

## License

MIT
