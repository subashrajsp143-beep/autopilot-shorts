import os
import sys
import json
import time

sys.stdout.reconfigure(encoding="utf-8")
sys.path.append("src")

from thumbnail_generator import ThumbnailGenerator
from youtube_uploader import YouTubeUploader

tg = ThumbnailGenerator(output_dir="output/fresh_thumbnails")

with open("config/uploaded_history.json", "r", encoding="utf-8") as f:
    h = json.load(f)

logs = h.get("upload_logs", [])
recent = [x for x in logs if x.get("youtube_id") and ("2026-11-05" in x.get("timestamp", "") or "2026-11-06" in x.get("timestamp", ""))]

print(f"Total recent videos to refresh thumbnails for: {len(recent)}")

# Pre-authenticate uploaders
uploaders = {}
if os.path.exists("config/youtube_token.json"):
    u1 = YouTubeUploader(token_path="config/youtube_token.json")
    u1.authenticate()
    if u1.youtube:
        uploaders[1] = u1
if os.path.exists("config/youtube_token_ch2.json"):
    u2 = YouTubeUploader(token_path="config/youtube_token_ch2.json")
    u2.authenticate()
    if u2.youtube:
        uploaders[2] = u2
if os.path.exists("config/youtube_token_ch3.json"):
    u3 = YouTubeUploader(token_path="config/youtube_token_ch3.json")
    u3.authenticate()
    if u3.youtube:
        uploaders[3] = u3

# Mapping of keywords to source clips for high-CTR clean thumbnail frames
CLIP_MAP = {
    "ronaldo": ("assets/creator_clips/football_01_ronaldo_bicycle.mp4", 4.2, "CR7 IMPOSSIBLE BICYCLE! 😱"),
    "speed": ("assets/creator_clips/speed_01_dude_perfect.mp4", 3.5, "SPEED CRAZY REACTION! 🔥"),
    "free-kick": ("assets/creator_clips/football_02_ronaldo_freekick.mp4", 5.0, "RONALDO 40-YARD KNUCKLEBALL! 🚀"),
    "backflip": ("assets/creator_clips/speed_02_backflips.mp4", 2.2, "SPEED INSANE STUNT! 🤯"),
    "mrbeast": ("assets/creator_clips/mrbeast_01_giving_cash.mp4", 3.0, "MRBEAST CASH GIVEAWAY! 💰"),
    "सिक्का": ("assets/creator_clips/mrbeast_02_briefcase.mp4", 2.5, "WIN $30,000 COIN FLIP! 🪙"),
    "सब्सक्राइब": ("assets/creator_clips/speed_04_iphone_duo.mp4", 4.0, "FREE IPHONE GIVEAWAY! 📱"),
    "ट्रैफिक": ("assets/creator_clips/mrbeast_01_giving_cash.mp4", 3.2, "PAID EVERYONE IN TRAFFIC! 🚦"),
    "फोन": ("assets/creator_clips/speed_04_iphone_duo.mp4", 3.8, "ANSWER PHONE TO WIN $10K! 📞"),
    "तिजोरी": ("assets/creator_clips/mrbeast_02_briefcase.mp4", 3.0, "SECRET VAULT UNLOCKED! 🏦"),
    "हेलमेट": ("assets/creator_clips/science_01_helmet_press.mp4", 7.5, "100-TON PRESS VS HELMET! 🔨"),
    "टेनिस": ("assets/creator_clips/records_01_table_tennis.mp4", 3.0, "IMPOSSIBLE PING PONG SHOT! 🏓"),
    "पत्ते": ("assets/creator_clips/science_03_cards_press.mp4", 5.5, "HYDRAULIC PRESS VS CARDS! 💥"),
    "हैंडस्टैंड": ("assets/creator_clips/records_02_levitation_handstand.mp4", 4.0, "ZERO GRAVITY HANDSTAND! 🤸"),
    "सोलर": ("assets/creator_clips/science_04_solar_panel.mp4", 6.2, "SOLAR PANEL EXPLOSION! ☀️"),
    "तलवार": ("assets/creator_clips/records_03_juggling_sword.mp4", 3.5, "BLINDFOLDED SWORD STUNT! 🗡️"),
    "क्रंच": ("assets/creator_clips/science_02_prettiest_crunch.mp4", 3.5, "ULTIMATE SATISFYING CRUNCH! ✨"),
    "गुलेल": ("assets/creator_clips/records_04_human_catapult.mp4", 4.0, "HUMAN CATAPULT 100 FT! 🚀"),
    "पिरामिड": ("assets/ai_video_clips/bg_pyramid.mp4", 2.0, "EGYPT PYRAMID SECRETS! 🏛️"),
    "बरमूडा": ("assets/ai_video_clips/bg_bermuda.mp4", 3.0, "BERMUDA TRIANGLE MYSTERY! ⚠️"),
    "मंदिर": ("assets/ai_video_clips/bg_temple.mp4", 1.8, "ANCIENT TEMPLE MIRACLE! 🛕"),
    "समुद्र": ("assets/ai_video_clips/bg_deepsea.mp4", 2.5, "DEEP SEA MONSTER DETECTED! 🌊"),
    "मेगालोडन": ("assets/ai_video_clips/bg_deepsea.mp4", 3.0, "MEGALODON CAUGHT ON CAMERA! 🦈"),
    "ब्लोप": ("assets/ai_video_clips/bg_ocean.mp4", 2.0, "THE BLOOP SOUND MYSTERY! 🔊"),
    "झूठ": ("assets/ai_video_clips/bg_darkpsych.mp4", 2.0, "DARK PSYCHOLOGY TRICK! 🕵️"),
    "अमीर": ("assets/ai_video_clips/bg_wealth.mp4", 1.5, "BILLIONAIRE WEALTH SECRETS! 💰"),
    "नींद": ("assets/ai_video_clips/bg_sleepbrain.mp4", 2.0, "SLEEP SCIENCE SECRETS! 😴"),
    "दिमाग": ("assets/ai_video_clips/bg_brain.mp4", 2.0, "BRAIN POWER SECRETS! 🧠"),
    "सूरज": ("assets/ai_video_clips/bg_space.mp4", 2.5, "WHAT IF SUN DISAPPEARS? ☀️"),
    "चांद": ("assets/ai_video_clips/bg_space.mp4", 2.0, "MOON MYSTERY UNLOCKED! 🌙"),
    "एंटार्कटिका": ("assets/ai_video_clips/bg_deepsea.mp4", 2.0, "FOUND UNDER ANTARCTICA ICE! ❄️")
}

success_count = 0
for idx, item in enumerate(recent, 1):
    vid = item.get("youtube_id")
    title = item.get("title", "")
    item_type = item.get("type", "")

    # Determine channel
    ch_id = 3
    if "Channel 1" in item_type or "MiniTalesWorld" in item_type or "FactTechz" in item_type:
        ch_id = 1
    elif "Channel 2" in item_type or "Pawsome" in item_type or "Science" in item_type:
        ch_id = 2

    uploader = uploaders.get(ch_id)
    if not uploader:
        continue

    # Find matching clip
    matched_clip = None
    matched_time = 2.5
    matched_badge = "VIRAL MOMENT! 🔥"

    for keyword, (clip_p, t_sec, badge) in CLIP_MAP.items():
        if keyword in title.lower() or keyword in item_type.lower():
            if os.path.exists(clip_p):
                matched_clip = clip_p
                matched_time = t_sec
                matched_badge = badge
                break

    if not matched_clip:
        # Default fallback clip based on channel
        if ch_id == 1:
            matched_clip = "assets/ai_video_clips/bg_space.mp4"
            matched_badge = "MIND-BLOWING FACT! 🤯"
        elif ch_id == 2:
            matched_clip = "assets/creator_clips/science_01_helmet_press.mp4"
            matched_badge = "100-TON CRUNCH! 💥"
        else:
            matched_clip = "assets/creator_clips/football_01_ronaldo_bicycle.mp4"
            matched_badge = "IMPOSSIBLE MOMENT! 😱"

    thumb_file = os.path.join("output/fresh_thumbnails", f"fresh_{vid}.jpg")
    try:
        tg.generate(
            video_path=matched_clip,
            output_thumb_path=thumb_file,
            badge_text=matched_badge,
            timestamp_sec=matched_time,
            slot_index=idx
        )
        if os.path.exists(thumb_file):
            res = uploader.set_thumbnail(vid, thumb_file)
            if res:
                success_count += 1
                print(f"[{idx}/{len(recent)}] [CH {ch_id}] Updated {vid} -> '{matched_badge}'")
            time.sleep(1)
    except Exception as e:
        print(f"[{idx}/{len(recent)}] Error updating {vid}: {e}")

print(f"\n🎉 Successfully updated {success_count} / {len(recent)} thumbnails on YouTube!")
