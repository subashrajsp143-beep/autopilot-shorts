import os
import sys
import json
import time

sys.stdout.reconfigure(encoding="utf-8")
sys.path.append("src")

from thumbnail_generator import ThumbnailGenerator
from youtube_uploader import YouTubeUploader

tg = ThumbnailGenerator(output_dir="output/fresh_thumbnails")

u1 = YouTubeUploader(token_path="config/youtube_token.json")
u1.authenticate()
if not u1.youtube:
    print("Error: Channel 1 authentication failed!")
    sys.exit(1)

with open("config/uploaded_history.json", "r", encoding="utf-8") as f:
    h = json.load(f)

logs = h.get("upload_logs", [])
ch1_today = [x for x in logs if x.get("youtube_id") and "2026-11-06" in x.get("timestamp", "") and ("Channel 1" in str(x.get("type")) or "FactTechz" in str(x.get("type")))]

print(f"Total Channel 1 videos to update: {len(ch1_today)}")

CLIP_MAP = {
    "झूठ": ("assets/ai_video_clips/bg_darkpsych.mp4", 2.0, "DARK PSYCHOLOGY SECRET! 🕵️"),
    "बात": ("assets/ai_video_clips/bg_darkpsych.mp4", 2.2, "SECRET PSYCHOLOGY RULE! 💡"),
    "इज्जत": ("assets/ai_video_clips/bg_psychology.mp4", 2.0, "DON'T MAKE THIS MISTAKE! ⚠️"),
    "पिरामिड": ("assets/ai_video_clips/bg_pyramid.mp4", 2.0, "EGYPT PYRAMID SECRETS! 🏛️"),
    "बरमूडा": ("assets/ai_video_clips/bg_bermuda.mp4", 3.0, "BERMUDA TRIANGLE TRUTH! ⚠️"),
    "मंदिर": ("assets/ai_video_clips/bg_temple.mp4", 1.8, "GRAVITY DEFYING TEMPLE! 🛕"),
    "एंटार्कटिका": ("assets/ai_video_clips/bg_space.mp4", 2.0, "FOUND UNDER 2-MILE ICE! ❄️"),
    "गहराई": ("assets/ai_video_clips/bg_deepsea.mp4", 2.5, "DEEP SEA SECRET REVEALED! 🌊"),
    "मेगालोडन": ("assets/ai_video_clips/bg_deepsea.mp4", 3.0, "MEGALODON SHARK EVIDENCE! 🦈"),
    "ब्लोप": ("assets/ai_video_clips/bg_ocean.mp4", 2.0, "MYSTERIOUS BLOOP SOUND! 🔊")
}

updated = 0
for idx, item in enumerate(ch1_today, 1):
    vid = item["youtube_id"]
    title = item["title"]

    matched_clip = "assets/ai_video_clips/bg_space.mp4"
    matched_time = 2.0
    matched_badge = "MIND-BLOWING FACT! 🤯"

    for kw, (cp, ts, badge) in CLIP_MAP.items():
        if kw in title:
            matched_clip = cp
            matched_time = ts
            matched_badge = badge
            break

    thumb_file = os.path.join("output/fresh_thumbnails", f"fresh_ch1_{vid}.jpg")
    try:
        tg.generate(
            video_path=matched_clip,
            output_thumb_path=thumb_file,
            badge_text=matched_badge,
            timestamp_sec=matched_time,
            slot_index=idx
        )
        if os.path.exists(thumb_file):
            res = u1.set_thumbnail(vid, thumb_file)
            if res:
                updated += 1
                print(f"[{idx}/10] Successfully updated {vid} -> '{matched_badge}'")
            else:
                print(f"[{idx}/10] Notice: Failed to set thumbnail for {vid}")
            time.sleep(3)  # Gentle spacing to avoid 429 rate limit
    except Exception as e:
        print(f"[{idx}/10] Error updating {vid}: {e}")

print(f"\n🎉 Successfully updated {updated} / {len(ch1_today)} Channel 1 thumbnails!")
