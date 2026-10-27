"""
Daily Views & Performance Tracker
---------------------------------
Fetches latest Shorts performance from channel @MiniTalesWorldTV,
ranks them by view count, and provides actionable retention feedback.
"""

import os
import sys
import json
import subprocess

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def track_views(limit: int = 25):
    channel_url = "https://www.youtube.com/@MiniTalesWorldTV/shorts"
    print(f"📊 Fetching latest {limit} Shorts performance from {channel_url}...\n")

    cmd = [
        "yt-dlp",
        "--flat-playlist",
        "--dump-json",
        channel_url
    ]

    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error fetching data: {res.stderr[:200]}")
        return

    videos = []
    for line in res.stdout.splitlines():
        if line.strip():
            try:
                data = json.loads(line)
                videos.append({
                    "id": data.get("id"),
                    "title": data.get("title", ""),
                    "views": data.get("view_count") or 0,
                    "url": f"https://youtube.com/shorts/{data.get('id')}"
                })
            except Exception:
                pass

    if not videos:
        print("No videos found.")
        return

    recent_videos = videos[:limit]
    total_recent_views = sum(v["views"] for v in recent_videos)

    print("=" * 75)
    print(f"🔥 TOP PERFORMING SHORTS (Last {len(recent_videos)} uploads | Total: {total_recent_views} views)")
    print("=" * 75)
    print(f"{'VIEWS':>8}  |  {'VIDEO ID':<12}  |  {'TITLE'}")
    print("-" * 75)

    sorted_vids = sorted(recent_videos, key=lambda x: x["views"], reverse=True)
    for v in sorted_vids:
        print(f"{v['views']:>8}  |  {v['id']:<12}  |  {v['title'][:48]}")

    print("=" * 75)


if __name__ == "__main__":
    track_views()
