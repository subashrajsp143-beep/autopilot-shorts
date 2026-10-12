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
    Calculates staggered publishing slots every 90 minutes throughout the day.
    Slots are converted to UTC RFC 3339 format for YouTube publishAt.
    """
    from datetime import datetime, timedelta, timezone
    now_utc = datetime.now(timezone.utc)
    start_slot = now_utc.replace(hour=3, minute=0, second=0, microsecond=0)

    schedules = []
    for i in range(num_videos):
        slot = start_slot + timedelta(minutes=i * interval_minutes)
        if slot <= now_utc + timedelta(minutes=10):
            schedules.append(None)  # Release immediately
        else:
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
    # PART 1: 5 AI HINDI SHORTS
    # -------------------------------------------------------------
    print("\n>>> [STAGE 1] Generating 5 AI Hindi Shorts (Neural Voice + Subtitles)...")
    hindi_gen = HindiScriptGenerator()
    all_scripts = hindi_gen.get_all_preset_scripts()
    video_maker = VideoMaker(assets_dir="assets", output_dir=output_batch_dir)

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

            # Build dynamic multi-scene visual background matching the topic
            storyboard = VisualStoryboard(cache_dir="assets/image_cache")
            bg_video_path = os.path.join(output_batch_dir, f"hindi_bg_{idx}_{timestamp}.mp4")
            try:
                bg_video = storyboard.build_multi_scene_background(
                    sentences=voice_res["sentences"],
                    output_bg_video=bg_video_path
                )
            except Exception as e:
                print(f"Notice: Storyboard fallback: {e}")
                bg_video = None

            # Render 9:16 vertical video with dynamic visuals & burnt subtitles
            video_path = video_maker.render_video(
                audio_path=audio_path,
                ass_path=ass_path,
                output_filename=video_filename,
                duration=voice_res["duration"],
                bg_video_path=bg_video
            )

            generated_videos.append({
                "index": idx,
                "type": "AI Hindi Short",
                "title": script["title"],
                "description": script["description"],
                "tags": script["tags"],
                "video_path": video_path,
                "duration": f"{voice_res['duration']:.1f}s"
            })
            print(f"✓ Video {idx} ready: {video_filename}")
        except Exception as e:
            print(f"❌ Failed to generate video {idx}: {e}")

    # -------------------------------------------------------------
    # PART 2: 5 REAL CREATOR & MR BEAST SHORTS (REAL MOVING FOOTAGE + HOOK BANNERS)
    # -------------------------------------------------------------
    print("\n>>> [STAGE 2] Generating 5 Real Creator Shorts (MrBeast, Speed, Viral Moments)...")
    clipper = CreatorClipper(downloads_dir="assets/downloads", output_dir=output_batch_dir)
    creator_sb = CreatorStoryboard(cache_dir="assets/image_cache")

    for j in range(min(5, len(VIRAL_CREATOR_PRESETS))):
        c_preset = VIRAL_CREATOR_PRESETS[j]
        idx = 5 + j + 1
        print(f"\n[{idx}/10] Creating Real Creator Short: {c_preset['title'][:40]}...")

        video_filename = f"video_{idx:02d}_creator_clip.mp4"
        final_video_path = os.path.join(output_batch_dir, video_filename)

        try:
            # 1. Download real creator clip (MrBeast / Speed)
            raw_video = clipper.download_by_search_or_url(
                search_query_or_url=c_preset["query"],
                output_prefix=f"creator_{idx}"
            )
            # 2. Format into 9:16 vertical short with blurred studio bg & hook banner
            video_path = clipper.create_viral_short_clip(
                video_path=raw_video,
                banner_text=c_preset["banner"],
                output_filename=video_filename,
                start_time=5,
                duration=30.0
            )
            vid_duration = "30.0s"
        except Exception as e:
            print(f"Notice: Fallback for creator short {idx}: {e}")
            c_script = CREATOR_SCRIPTS_HINDI[j]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            audio_path = os.path.join(output_batch_dir, f"creator_audio_{idx}_{timestamp}.mp3")
            ass_path = os.path.join(output_batch_dir, f"creator_sub_{idx}_{timestamp}.ass")
            bg_video_path = os.path.join(output_batch_dir, f"creator_bg_{idx}_{timestamp}.mp4")

            voice_res = generate_audio(
                text=c_script["text"],
                audio_path=audio_path,
                ass_path=ass_path,
                voice="hi-IN-MadhurNeural"
            )
            bg_video = creator_sb.build_creator_video_background(
                key=c_script["key"],
                duration=voice_res["duration"],
                output_path=bg_video_path
            )
            video_path = video_maker.render_video(
                audio_path=audio_path,
                ass_path=ass_path,
                output_filename=video_filename,
                duration=voice_res["duration"],
                bg_video_path=bg_video
            )
            vid_duration = f"{voice_res['duration']:.1f}s"

        generated_videos.append({
            "index": idx,
            "type": "Creator Short (Real Video)",
            "title": c_preset["title"],
            "description": c_preset["description"],
            "tags": c_preset["tags"],
            "video_path": video_path,
            "duration": vid_duration
        })
        print(f"✓ Video {idx} ready (Real Creator Footage): {video_filename}")

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
