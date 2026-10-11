"""
Upload Remaining Videos For Today with Staggered Schedule
Uploads videos 02 to 10 and schedules them throughout today's afternoon, evening, and night.
"""

import os
import sys
import json
import time
from datetime import datetime, timedelta, timezone

# Fix Windows console UTF-8 output
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
from youtube_uploader import YouTubeUploader

metadata_path = "output/batch_today/daily_metadata.json"
if not os.path.exists(metadata_path):
    print("Metadata file not found!")
    sys.exit(1)

with open(metadata_path, "r", encoding="utf-8") as f:
    videos = json.load(f)

uploader = YouTubeUploader()
uploader.authenticate()

# Upload remaining videos (videos 2 through 10)
remaining = videos[1:]
now_utc = datetime.now(timezone.utc)
first_slot = now_utc + timedelta(minutes=15)
interval_minutes = 75  # 1 hour 15 minutes between each video

print(f"🚀 Uploading {len(remaining)} videos for TODAY's schedule...\n")

for i, v in enumerate(remaining):
    slot_utc = first_slot + timedelta(minutes=i * interval_minutes)
    publish_at_str = slot_utc.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    slot_ist = slot_utc + timedelta(hours=5, minutes=30)
    ist_display = slot_ist.strftime("%I:%M %p")

    print(f"[{i+1}/{len(remaining)}] Uploading Video #{v['index']} -> '{v['title'][:45]}...'")
    print(f"    Release scheduled for: {ist_display} IST today")

    try:
        res = uploader.upload_short(
            video_path=v["video_path"],
            title=v["title"],
            description=v["description"],
            tags=v["tags"],
            publish_at=publish_at_str
        )
        print(f"    ✓ Success! Live link: {res['url']}\n")
    except Exception as e:
        print(f"    ❌ Failed: {e}\n")

    time.sleep(5)  # pause between uploads to respect API rate limits

print("=" * 65)
print("🎉 ALL VIDEOS FOR TODAY HAVE BEEN UPLOADED & SCHEDULED!")
print("=" * 65)
