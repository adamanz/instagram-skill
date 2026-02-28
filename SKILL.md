---
name: instagram
description: Watch, download, and analyze Instagram Reels and videos. Use when a user shares an Instagram URL (reel, post, story) and wants to see/understand the content, download the video, or get metadata. Also use when asked to check someone's Instagram content.
---

# Instagram

Download and analyze Instagram Reels/videos via `yt-dlp`. No login required for public content.

## Quick Reference

```bash
# Get metadata (title, uploader, views, likes, description)
python3 ~/clawd/skills/instagram/scripts/ig.py info "https://www.instagram.com/reel/XXXXX/"

# Download video
python3 ~/clawd/skills/instagram/scripts/ig.py download "https://www.instagram.com/reel/XXXXX/"

# Download + prepare for vision analysis
python3 ~/clawd/skills/instagram/scripts/ig.py watch "https://www.instagram.com/reel/XXXXX/"
```

## Workflow: "Watch" a Reel

1. Run `ig.py watch <url>` — downloads video to `~/clawd/media/videos/instagram/`
2. Extract frames with video-frames skill: `ffmpeg -i <video> -vf "fps=1" /tmp/ig-frames/frame_%03d.jpg`
3. Analyze frames with the `image` tool to describe what's happening
4. Combine with metadata (description, uploader) for full context

## Workflow: Just Get Info

Run `ig.py info <url>` for quick metadata without downloading.

## Sending Videos via Telegram

Instagram videos are VP9 codec — **Telegram can't play VP9 inline**. Always re-encode to H.264 before sending:

```bash
ffmpeg -y -i input.mp4 -c:v libx264 -c:a aac -movflags +faststart output_h264.mp4
```

Then send with `mimeType: video/mp4`.

## Notes

- Public reels/posts work without login
- Private accounts require cookies: `yt-dlp --cookies-from-browser chrome <url>`
- Videos save to `~/clawd/media/videos/instagram/`
- For stories (ephemeral), must use cookies and download quickly
- yt-dlp must be installed (`brew install yt-dlp`)
- **Always re-encode VP9→H.264 before sending to Telegram**
