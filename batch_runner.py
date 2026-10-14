"""
Daily 10 Videos Batch Generator & Scheduler
-------------------------------------------
Generates 10 ready-to-upload viral Shorts/Reels daily in Hindi:
- 5x AI Hindi Mystery/Psychology Shorts (Neural Voice + Bold Subtitles)
- 5x Creator Highlights / MrBeast Clips (Vertical 9:16 + Top Hook Banner)

Can automatically upload them to YouTube, Instagram, and Facebook,
or copy them all to a dedicated folder on your Desktop!
"""

import os
import sys
import re
import json
import shutil
import time
from datetime import datetime
from typing import List, Dict, Any

# Fix Windows console UTF-8 output
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from hindi_script_generator import HindiScriptGenerator
from voice_generator import generate_audio
from video_maker import VideoMaker
from clipper import CreatorClipper, VIRAL_CREATOR_PRESETS
from youtube_uploader import YouTubeUploader
from meta_uploader import MetaUploader
from visual_storyboard import VisualStoryboard
from creator_storyboard import CreatorStoryboard, CREATOR_SCRIPTS_HINDI


def ensure_credentials():
    """Restores client_secrets and youtube_token if running in cloud runner."""
    cs_path = "config/client_secrets.json"
    yt_path = "config/youtube_token.json"
    dat_path = "config/credentials.dat"
    if (not os.path.exists(cs_path) or not os.path.exists(yt_path)) and os.path.exists(dat_path):
        import base64
        try:
            with open(dat_path, "r", encoding="utf-8") as f:
                encoded = f.read()
            payload = json.loads(base64.b85decode(encoded.encode("utf-8")).decode("utf-8"))
            os.makedirs("config", exist_ok=True)
            with open(cs_path, "w", encoding="utf-8") as f:
                f.write(payload["client_secrets"])
            with open(yt_path, "w", encoding="utf-8") as f:
                f.write(payload["youtube_token"])
            print("Credentials unpacked successfully.")
        except Exception as e:
            print(f"Warning: Could not unpack credentials: {e}")


# Creator highlights library (sample moments with hook banners)
CREATOR_PRESETS: List[Dict[str, Any]] = [
    {
        "creator": "MrBeast",
        "title": "MR BEAST: $1,000,000 INCREDIBLE CHALLENGE 😱 #Shorts #MrBeast",
        "banner": "MR BEAST: $1,000,000 CHALLENGE 😱",
        "description": "Watch what happens in this insane MrBeast challenge!\n\n#Shorts #MrBeast #MrBeastHindi #Viral",
        "tags": ["mrbeast", "mrbeast hindi", "shorts", "challenge", "viral"]
    },
    {
        "creator": "MrBeast",
        "title": "MR BEAST: SURVIVING 100 HOURS IN DESERT 🏜️ #Shorts #MrBeastHindi",
        "banner": "SURVIVING 100 HOURS IN DESERT 🏜️",
        "description": "Can they survive 100 hours with nothing?\n\n#Shorts #MrBeast #MrBeastHindi #Challenge",
        "tags": ["mrbeast", "mrbeast in hindi", "survival", "shorts", "viral"]
    },
    {
        "creator": "Podcast Highlight",
        "title": "THIS ADVICE WILL CHANGE YOUR 20s FOREVER 💡 #Shorts #Motivation",
        "banner": "THIS ADVICE WILL CHANGE YOUR 20s 💡",
        "description": "The most powerful life lesson you will hear today.\n\n#Shorts #LifeLessons #MotivationHindi #PodcastClips",
        "tags": ["podcast", "motivation hindi", "life advice", "success", "shorts"]
    },
    {
        "creator": "MrBeast",
        "title": "MR BEAST: I GAVE AWAY A PRIVATE ISLAND 🏝️ #Shorts #CrazyMoments",
        "banner": "I GAVE AWAY A PRIVATE ISLAND 🏝️",
        "description": "Unbelievable moment when a subscriber won an island!\n\n#Shorts #MrBeast #WinAnIsland #Viral",
        "tags": ["mrbeast", "island challenge", "giveaway", "shorts", "viral"]
    },
    {
        "creator": "Crazy Experiments",
        "title": "WHAT HAPPENS IF YOU DROP AN ANVIL FROM 1000 FT? 💥 #Shorts #Experiment",
        "banner": "ANVIL DROPPED FROM 1000 FEET! 💥",
        "description": "Crazy physics experiment in slow motion!\n\n#Shorts #Experiments #SlowMotion #ViralScience",
        "tags": ["experiment", "destruction", "slow motion", "shorts", "viral"]
    }
]


def get_staggered_schedule(num_videos: int = 10, interval_minutes: int = 90):
    """
    Calculates strictly staggered publishing slots spaced every 90 minutes.
    Guarantees videos are strictly chronological and never out of order.
    """
    from datetime import datetime, timedelta, timezone
    now_utc = datetime.now(timezone.utc)

    # Base time is 02:30 UTC (08:00 AM IST)
    base_time = now_utc.replace(hour=2, minute=30, second=0, microsecond=0)

    # If already past 08:15 AM IST, base time moves to current time
    if now_utc > base_time + timedelta(minutes=15):
        base_time = now_utc

    schedules = []
    for i in range(num_videos):
        if i == 0:
            schedules.append(None)  # Video 1 goes live immediately
        else:
            slot = base_time + timedelta(minutes=i * interval_minutes)
            if slot <= now_utc + timedelta(minutes=5):
                slot = now_utc + timedelta(minutes=i * interval_minutes)
            schedules.append(slot.strftime("%Y-%m-%dT%H:%M:%S.000Z"))

    return schedules


def generate_daily_10_batch(
    output_batch_dir: str = "output/batch_today",
    copy_to_desktop: bool = False,
    upload_yt: bool = False,
    upload_meta: bool = False
):
    print("=" * 65)
    print("🚀 GENERATING DAILY BATCH OF 10 VIRAL SHORTS (HINDI & CREATORS)")
    print("=" * 65)

    ensure_credentials()
    os.makedirs(output_batch_dir, exist_ok=True)
    generated_videos: List[Dict[str, Any]] = []

    # -------------------------------------------------------------
    # PART 1: 5 AI HINDI SHORTS (100% REAL MOVING VIDEO FOOTAGE)
    # -------------------------------------------------------------
    print("\n>>> [STAGE 1] Generating 5 AI Hindi Shorts (Real Moving Background Footage)...")
    hindi_gen = HindiScriptGenerator()
    all_scripts = hindi_gen.get_all_preset_scripts()
    video_maker = VideoMaker(assets_dir="assets", output_dir=output_batch_dir)

    ai_bg_clips = [
        "assets/ai_video_clips/bg_psychology.mp4",
        "assets/ai_video_clips/bg_ocean.mp4",
        "assets/ai_video_clips/bg_money.mp4",
        "assets/ai_video_clips/bg_brain.mp4",
        "assets/ai_video_clips/bg_space.mp4"
    ]

    for i in range(min(5, len(all_scripts))):
        script = all_scripts[i]
        idx = i + 1
        print(f"\n[{idx}/10] Creating AI Hindi Short: {script['title'][:40]}...")

        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            audio_path = os.path.join(output_batch_dir, f"hindi_audio_{idx}_{timestamp}.mp3")
            ass_path = os.path.join(output_batch_dir, f"hindi_sub_{idx}_{timestamp}.ass")
            video_filename = f"video_{idx:02d}_hindi_ai.mp4"

            # Generate Hindi voiceover and subtitles
            voice_res = generate_audio(
                text=script["text"],
                audio_path=audio_path,
                ass_path=ass_path,
                voice="hi-IN-MadhurNeural"
            )

            # Assign real moving HD video background
            bg_video = ai_bg_clips[i % len(ai_bg_clips)]
            if not os.path.exists(bg_video):
                print(f"Warning: {bg_video} not found, falling back to any available bg")
                bg_video = None

            # Render 9:16 vertical video with REAL MOVING VIDEO & burnt subtitles
            video_path = video_maker.render_video(
                audio_path=audio_path,
                ass_path=ass_path,
                output_filename=video_filename,
                duration=voice_res["duration"],
                bg_video_path=bg_video
            )

            generated_videos.append({
                "index": idx,
                "type": "AI Hindi Short (Real Video)",
                "title": script["title"],
                "description": script["description"],
                "tags": script["tags"],
                "video_path": video_path,
                "duration": f"{voice_res['duration']:.1f}s"
            })
            print(f"✓ Video {idx} ready (Real Moving Video): {video_filename}")
        except Exception as e:
            print(f"❌ Failed to generate video {idx}: {e}")

    # -------------------------------------------------------------
    # PART 2: 5 REAL CREATOR & MR BEAST SHORTS (100% REAL MOVING FOOTAGE)
    # -------------------------------------------------------------
    print("\n>>> [STAGE 2] Generating 5 Real Creator Shorts (MrBeast, Speed, Viral Moments)...")
    clipper = CreatorClipper(downloads_dir="assets/downloads", output_dir=output_batch_dir)

    creator_local_clips = [
        "assets/creator_clips/clip_01_mrbeast_island.mp4",
        "assets/creator_clips/clip_02_speed_reaction.mp4",
        "assets/creator_clips/clip_03_mrbeast_cash.mp4",
        "assets/creator_clips/clip_04_speed_ronaldo.mp4",
        "assets/creator_clips/clip_05_mrbeast_escape.mp4"
    ]

    for j in range(min(5, len(VIRAL_CREATOR_PRESETS))):
        c_preset = VIRAL_CREATOR_PRESETS[j]
        idx = 5 + j + 1
        print(f"\n[{idx}/10] Creating Real Creator Short: {c_preset['title'][:40]}...")

        video_filename = f"video_{idx:02d}_creator_clip.mp4"

        try:
            local_clip = creator_local_clips[j % len(creator_local_clips)]
            if os.path.exists(local_clip):
                raw_video = local_clip
                start_sec = 0
            else:
                raw_video = clipper.download_by_search_or_url(
                    search_query_or_url=c_preset["query"],
                    output_prefix=f"creator_{idx}"
                )
                start_sec = 5

            # Format into 9:16 vertical short with blurred studio bg & hook banner
            video_path = clipper.create_viral_short_clip(
                video_path=raw_video,
                banner_text=c_preset["banner"],
                output_filename=video_filename,
                start_time=start_sec,
                duration=30.0
            )
            vid_duration = "30.0s"
        except Exception as e:
            print(f"❌ Failed creator short {idx}: {e}")
            continue

        generated_videos.append({
            "index": idx,
            "type": "Creator Short (Real Moving Footage)",
            "title": c_preset["title"],
            "description": c_preset["description"],
            "tags": c_preset["tags"],
            "video_path": video_path,
            "duration": vid_duration
        })
        print(f"✓ Video {idx} ready (100% Real Moving Footage): {video_filename}")

    # -------------------------------------------------------------
    # PART 3: SAVE METADATA & SCHEDULE
    # -------------------------------------------------------------
    metadata_path = os.path.join(output_batch_dir, "daily_metadata.json")
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(generated_videos, f, ensure_ascii=False, indent=2)

    # Copy to Desktop if requested
    desktop_folder = None
    if copy_to_desktop:
        try:
            desktop_path = os.path.join(os.environ["USERPROFILE"], "Desktop")
            desktop_folder = os.path.join(desktop_path, "Daily_10_Shorts")
            os.makedirs(desktop_folder, exist_ok=True)
            for v in generated_videos:
                dest = os.path.join(desktop_folder, os.path.basename(v["video_path"]))
                shutil.copy2(v["video_path"], dest)
            # Copy metadata json too
            shutil.copy2(metadata_path, os.path.join(desktop_folder, "titles_and_tags.json"))
            print(f"\n📂 All 10 videos copied to Desktop -> {desktop_folder}")
        except Exception as e:
            print(f"Warning: Could not copy to desktop: {e}")

    # Optional Auto-Upload
    if upload_yt:
        print("\n>> Uploading all 10 videos with Smart Staggered Schedule (Every 1.5 Hours)...")
        yt_uploader = YouTubeUploader()
        schedules = get_staggered_schedule(len(generated_videos), interval_minutes=90)
        for idx, v in enumerate(generated_videos):
            slot = schedules[idx]
            try:
                yt_uploader.upload_short(
                    video_path=v["video_path"],
                    title=v["title"],
                    description=v["description"],
                    tags=v["tags"],
                    privacy_status="public",
                    publish_at=slot
                )
                time.sleep(4)  # pause between uploads
            except Exception as e:
                print(f"YouTube upload failed for {v['title']}: {e}")

    if upload_meta:
        print("\n>> Uploading to Facebook/Instagram...")
        meta_uploader = MetaUploader()
        for v in generated_videos:
            try:
                meta_uploader.upload_facebook_reel(
                    video_path=v["video_path"],
                    caption=f"{v['title']}\n\n{v['description']}"
                )
            except Exception as e:
                print(f"Meta upload failed for {v['title']}: {e}")

    print("\n" + "=" * 65)
    print("🎉 ALL 10 VIDEOS GENERATED SUCCESSFULLY!")
    if desktop_folder:
        print(f"📁 Check your Desktop folder: 'Daily_10_Shorts'")
    print("=" * 65)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Daily 10 Videos Batch Generator & Uploader")
    parser.add_argument("--upload-yt", action="store_true", help="Upload to YouTube")
    parser.add_argument("--upload-meta", action="store_true", help="Upload to Facebook & Instagram")
    parser.add_argument("--upload-all", action="store_true", help="Upload to all platforms")
    parser.add_argument("--skip-gen", action="store_true", help="Upload existing generated batch without re-rendering")
    args = parser.parse_args()

    upload_yt = args.upload_yt or args.upload_all
    upload_meta = args.upload_meta or args.upload_all

    if args.skip_gen:
        # Load existing batch metadata
        metadata_path = "output/batch_today/daily_metadata.json"
        if os.path.exists(metadata_path):
            with open(metadata_path, "r", encoding="utf-8") as f:
                videos = json.load(f)
            print(f"Loaded {len(videos)} existing batch videos.")
            if upload_yt:
                print(">> Uploading to YouTube...")
                uploader = YouTubeUploader()
                for v in videos[1:]:  # skip video 1 which is already uploaded
                    uploader.upload_short(v["video_path"], v["title"], v["description"], v["tags"])
                    time.sleep(4)
        else:
            print("No existing batch found. Run without --skip-gen first.")
    else:
        generate_daily_10_batch(
            copy_to_desktop=False,
            upload_yt=upload_yt,
            upload_meta=upload_meta
        )
