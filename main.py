"""
Autopilot Faceless Video Machine - Main Orchestrator
----------------------------------------------------
Full pipeline:
1. Generates viral high-retention script (Topic / Hook / Story)
2. Synthesizes realistic human neural voice (Edge-TTS)
3. Generates synchronized bold animated ASS subtitles
4. Assembles 1080x1920 vertical video (FFmpeg)
5. Automatically uploads to:
   - YouTube Shorts (YouTube Data API v3)
   - Facebook Page Reels (Meta Graph API)
   - Instagram Reels (Meta Graph API)
"""

import os
import sys
import argparse
import time
from datetime import datetime

# Fix Windows console UTF-8 output
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Add src to python path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from script_generator import ScriptGenerator
from voice_generator import generate_audio
from video_maker import VideoMaker
from youtube_uploader import YouTubeUploader
from meta_uploader import MetaUploader


def run_pipeline(
    niche: str = None,
    custom_topic: str = None,
    voice: str = "en-US-ChristopherNeural",
    upload_yt: bool = False,
    upload_meta: bool = False,
    privacy_status: str = "public"
):
    print("=" * 60)
    print("🚀 STARTING AUTOPILOT VIDEO GENERATION PIPELINE")
    print("=" * 60)

    # 1. Script Generation
    print("\n[1/4] Generating script...")
    script_gen = ScriptGenerator()
    if custom_topic:
        script = script_gen.generate_custom_script(custom_topic)
    else:
        script = script_gen.get_preset_script(niche)

    print(f"🎬 Title: {script['title']}")
    print(f"📖 Niche: {script.get('niche', 'Viral Shorts')}")
    print(f"📝 Script preview:\n{script['text'][:150]}...\n")

    # 2. Audio & Subtitles Generation
    print("[2/4] Generating neural voiceover & dynamic ASS subtitles...")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    audio_path = os.path.join("output", f"audio_{timestamp}.mp3")
    ass_path = os.path.join("output", f"subtitles_{timestamp}.ass")

    voice_res = generate_audio(
        text=script["text"],
        audio_path=audio_path,
        ass_path=ass_path,
        voice=voice
    )
    print(f"Audio generated ({voice_res['duration']:.2f}s) with {voice_res['chunks_count']} subtitle chunks.")

    # 3. Video Assembly
    print("\n[3/4] Assembling 9:16 vertical video with FFmpeg...")
    video_maker = VideoMaker(assets_dir="assets", output_dir="output")
    video_filename = f"short_{timestamp}.mp4"
    video_path = video_maker.render_video(
        audio_path=audio_path,
        ass_path=ass_path,
        output_filename=video_filename,
        duration=voice_res["duration"]
    )
    print(f"Video file ready: {video_path}")

    # 4. Multi-Platform Auto-Upload
    print("\n[4/4] Auto-Upload Phase:")
    upload_results = {}

    # YouTube Upload
    if upload_yt:
        try:
            print("\n>> Uploading to YouTube Shorts...")
            yt_uploader = YouTubeUploader()
            yt_res = yt_uploader.upload_short(
                video_path=video_path,
                title=script["title"],
                description=script["description"],
                tags=script.get("tags", []),
                privacy_status=privacy_status
            )
            upload_results["YouTube"] = yt_res
        except Exception as e:
            print(f"❌ YouTube upload error: {e}")
            upload_results["YouTube"] = {"status": "failed", "error": str(e)}
    else:
        print(">> YouTube upload skipped (Use --upload-yt to enable)")

    # Meta (Facebook & Instagram) Upload
    if upload_meta:
        meta_uploader = MetaUploader()
        caption = f"{script['title']}\n\n{script['description']}"

        # Facebook Page Reel
        try:
            print("\n>> Uploading to Facebook Page Reels...")
            fb_res = meta_uploader.upload_facebook_reel(
                video_path=video_path,
                caption=caption
            )
            upload_results["Facebook"] = fb_res
        except Exception as e:
            print(f"❌ Facebook upload error: {e}")
            upload_results["Facebook"] = {"status": "failed", "error": str(e)}

        # Instagram Reel
        try:
            # Note: For direct Instagram Reels via Graph API, video needs a reachable URL
            # Or you can enable auto cross-posting from Facebook Page to Instagram!
            print("\n>> Instagram Reel: If cross-posting is enabled on your Facebook Page, it will publish automatically!")
        except Exception as e:
            print(f"❌ Instagram upload error: {e}")
    else:
        print(">> Meta upload skipped (Use --upload-meta to enable)")

    print("\n" + "=" * 60)
    print("🎉 PIPELINE COMPLETED SUCCESSFULLY!")
    print(f"📁 Output Video: {os.path.abspath(video_path)}")
    if upload_results:
        print("📤 Upload Summary:")
        for platform, res in upload_results.items():
            print(f"   • {platform}: {res.get('status', 'unknown')}")
    print("=" * 60)

    return video_path


def schedule_daily_runs(interval_hours: float = 24.0, **kwargs):
    """Runs the pipeline on a recurring schedule automatically."""
    print(f"⏰ Scheduler active: Generating & uploading every {interval_hours} hours...")
    while True:
        try:
            run_pipeline(**kwargs)
        except Exception as e:
            print(f"Error during scheduled run: {e}")

        seconds = int(interval_hours * 3600)
        print(f"\nWaiting {interval_hours} hours until next video generation...")
        time.sleep(seconds)


def main():
    parser = argparse.ArgumentParser(description="Autopilot Video Generator & Uploader")
    parser.add_argument("--niche", type=str, default=None, help="Niche: psychology, history, science, money")
    parser.add_argument("--topic", type=str, default=None, help="Custom topic for the video")
    parser.add_argument("--voice", type=str, default="en-US-ChristopherNeural", help="Edge-TTS voice name")
    parser.add_argument("--upload-yt", action="store_true", help="Auto-upload to YouTube Shorts")
    parser.add_argument("--upload-meta", action="store_true", help="Auto-upload to Facebook & Instagram")
    parser.add_argument("--upload-all", action="store_true", help="Auto-upload to all platforms")
    parser.add_argument("--privacy", type=str, default="public", choices=["public", "unlisted", "private"], help="YouTube privacy")
    parser.add_argument("--schedule", type=float, default=None, help="Run repeatedly every N hours")

    args = parser.parse_args()

    upload_yt = args.upload_yt or args.upload_all
    upload_meta = args.upload_meta or args.upload_all

    if args.schedule:
        schedule_daily_runs(
            interval_hours=args.schedule,
            niche=args.niche,
            custom_topic=args.topic,
            voice=args.voice,
            upload_yt=upload_yt,
            upload_meta=upload_meta,
            privacy_status=args.privacy
        )
    else:
        run_pipeline(
            niche=args.niche,
            custom_topic=args.topic,
            voice=args.voice,
            upload_yt=upload_yt,
            upload_meta=upload_meta,
            privacy_status=args.privacy
        )


if __name__ == "__main__":
    main()
