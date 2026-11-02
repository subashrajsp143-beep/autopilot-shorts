import os
import sys
import json
import time
from datetime import datetime, timedelta, timezone

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
from youtube_uploader import YouTubeUploader
from history_tracker import HistoryTracker

meta_file = "output/batch_today/daily_metadata.json"
with open(meta_file, "r", encoding="utf-8") as f:
    videos = json.load(f)

print(f"Loaded {len(videos)} videos ready for upload.", flush=True)

# Generate schedule starting from 4:30 PM IST today
ist = timezone(timedelta(hours=5, minutes=30))
now_ist = datetime.now(ist)

def get_today_evening_schedule(total=10):
    start_time = now_ist.replace(minute=30, second=0, microsecond=0)
    if start_time < now_ist:
        start_time = now_ist + timedelta(minutes=15)
    slots = []
    current = start_time
    for i in range(total):
        slots.append(current.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
        current += timedelta(minutes=40)
    return slots

schedules = get_today_evening_schedule(len(videos))

channels = [
    {"id": 1, "name": "Channel 1 (MiniTalesWorld)", "token": "config/youtube_token.json", "start_idx": 1},
    {"id": 2, "name": "Channel 2 (Pawsome Productions)", "token": "config/youtube_token_ch2.json", "start_idx": 0},
    {"id": 3, "name": "Channel 3 (Next Level Facts)", "token": "config/youtube_token_ch3.json", "start_idx": 0}
]

tracker = HistoryTracker()

# Record the already uploaded video 1 on Channel 1
v1 = videos[0]
tracker.record_upload(
    title=v1["title"],
    video_type=f"{v1['type']} [Channel 1 (MiniTalesWorld)]",
    youtube_video_id="6nNu8W_Q5jo",
    source_id=v1.get("source_id"),
    query=v1.get("query")
)

for ch in channels:
    if not os.path.exists(ch["token"]):
        print(f"Skipping {ch['name']} (token not found).", flush=True)
        continue

    print("\n" + "=" * 65, flush=True)
    print(f"🚀 UPLOADING BATCH TO {ch['name']}...", flush=True)
    print("=" * 65, flush=True)

    try:
        uploader = YouTubeUploader(token_path=ch["token"])
        start_i = ch.get("start_idx", 0)
        videos_to_upload = videos[start_i:]
        ch_success = 0

        for idx, v in enumerate(videos_to_upload, start=start_i):
            slot_utc = schedules[idx]
            print(f"\n[{idx+1}/{len(videos)}] Uploading to {ch['name']}: {v['title'][:50]}...", flush=True)
            print(f"    Schedule: {slot_utc} UTC | Video: {v['video_path']}", flush=True)
            try:
                res = uploader.upload_short(
                    video_path=v["video_path"],
                    title=v["title"],
                    description=v["description"],
                    tags=v["tags"],
                    publish_at=slot_utc,
                    thumbnail_path=v.get("thumbnail_path")
                )
                vid_id = res.get("video_id")
                print(f"    ✓ Uploaded! ID: {vid_id} -> https://youtube.com/shorts/{vid_id}", flush=True)
                ch_success += 1
                tracker.record_upload(
                    title=v["title"],
                    video_type=f"{v['type']} [{ch['name']}]",
                    youtube_video_id=vid_id,
                    source_id=v.get("source_id"),
                    query=v.get("query")
                )
                time.sleep(3)
            except Exception as e:
                print(f"    ❌ Failed: {e}", flush=True)
        print(f"\n✓ {ch_success} / {len(videos_to_upload)} videos uploaded to {ch['name']}!", flush=True)
    except Exception as e:
        print(f"❌ Failed channel {ch['name']}: {e}", flush=True)

print("\n🎉 ALL UPLOADS COMPLETED SUCCESSFULLY!", flush=True)
