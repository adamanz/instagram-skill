#!/usr/bin/env python3
"""Instagram video/reel downloader + metadata extractor via yt-dlp."""

import argparse
import json
import subprocess
import sys
import os
from pathlib import Path

MEDIA_DIR = Path.home() / "clawd" / "media" / "videos" / "instagram"


def get_info(url: str) -> dict:
    """Extract metadata without downloading."""
    r = subprocess.run(
        ["yt-dlp", "--no-download", "--dump-json", "--no-playlist", url],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        print(f"Error: {r.stderr.strip()}", file=sys.stderr)
        sys.exit(1)
    return json.loads(r.stdout)


def download(url: str, output: str | None = None, transcode: bool = True) -> str:
    """Download video, return file path. Auto-transcodes VP9→H.264 for Telegram compatibility."""
    MEDIA_DIR.mkdir(parents=True, exist_ok=True)
    template = output or str(MEDIA_DIR / "%(uploader)s_%(id)s.%(ext)s")
    r = subprocess.run(
        ["yt-dlp", "--no-playlist", "-o", template, url],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        print(f"Error: {r.stderr.strip()}", file=sys.stderr)
        sys.exit(1)
    # Parse output path from yt-dlp
    raw_path = None
    for line in r.stdout.splitlines():
        if "Destination:" in line:
            raw_path = line.split("Destination:", 1)[1].strip()
            break
        if "has already been downloaded" in line:
            raw_path = line.split("]", 1)[1].strip().replace(" has already been downloaded", "")
            break
    if not raw_path:
        raw_path = r.stdout.strip()

    if not transcode:
        return raw_path

    # Check codec and transcode VP9→H.264 if needed
    probe = subprocess.run(
        ["ffprobe", "-v", "quiet", "-select_streams", "v:0",
         "-show_entries", "stream=codec_name", "-of", "csv=p=0", raw_path],
        capture_output=True, text=True,
    )
    codec = probe.stdout.strip()
    if codec and codec != "h264":
        h264_path = raw_path.rsplit(".", 1)[0] + "_h264.mp4"
        subprocess.run(
            ["ffmpeg", "-y", "-i", raw_path, "-c:v", "libx264",
             "-c:a", "aac", "-movflags", "+faststart", h264_path],
            capture_output=True,
        )
        return h264_path
    return raw_path


def info_cmd(args):
    data = get_info(args.url)
    out = {
        "id": data.get("id"),
        "title": data.get("title"),
        "uploader": data.get("uploader"),
        "uploader_id": data.get("uploader_id"),
        "description": data.get("description", "")[:500],
        "duration": data.get("duration"),
        "view_count": data.get("view_count"),
        "like_count": data.get("like_count"),
        "comment_count": data.get("comment_count"),
        "timestamp": data.get("timestamp"),
        "url": data.get("webpage_url"),
    }
    print(json.dumps(out, indent=2))


def download_cmd(args):
    path = download(args.url, args.output)
    print(json.dumps({"status": "ok", "path": path}))


def watch_cmd(args):
    """Download + extract key frames for vision analysis."""
    path = download(args.url, args.output)
    info = get_info(args.url)
    print(json.dumps({
        "status": "ok",
        "path": path,
        "uploader": info.get("uploader"),
        "description": info.get("description", "")[:500],
        "duration": info.get("duration"),
    }, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Instagram video tool")
    sub = parser.add_subparsers(dest="command", required=True)

    p_info = sub.add_parser("info", help="Get video metadata")
    p_info.add_argument("url")
    p_info.set_defaults(func=info_cmd)

    p_dl = sub.add_parser("download", help="Download video")
    p_dl.add_argument("url")
    p_dl.add_argument("-o", "--output", help="Output path template")
    p_dl.set_defaults(func=download_cmd)

    p_watch = sub.add_parser("watch", help="Download + prepare for analysis")
    p_watch.add_argument("url")
    p_watch.add_argument("-o", "--output", help="Output path template")
    p_watch.set_defaults(func=watch_cmd)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
