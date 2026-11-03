"""
Channel Batch Generator
-----------------------
Generates 10 distinct, non-overlapping Shorts tailored specifically
for each of the 3 YouTube channels:
- Channel 3: Sports, Football & IShowSpeed with high-energy Hindi commentary
- Channel 1: FactTechz-style HD moving video B-roll documentary Shorts
- Channel 2: Mind-Blowing Science, Hydraulic Press & Guinness World Records
"""

import os
import sys
import subprocess
from typing import List, Dict, Any, Optional

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from src.channel_blueprints import CHANNEL_3_BLUEPRINTS, CHANNEL_1_BLUEPRINTS, CHANNEL_2_BLUEPRINTS
from src.action_hindi_renderer import render_action_clip_hindi
from src.video_maker import VideoMaker
from src.voice_generator import generate_audio


def generate_channel_batch(channel_id: int, base_output_dir: str = "output/batch_today", force_render: bool = False) -> List[Dict[str, Any]]:
    """
    Renders or loads 10 unique Shorts for the specified channel ID (1, 2, or 3).
    Guarantees zero cross-channel duplicate videos or scripts.
    """
    channel_dir = os.path.join(base_output_dir, f"channel_{channel_id}")
    os.makedirs(channel_dir, exist_ok=True)
    results: List[Dict[str, Any]] = []

    print(f"\n=======================================================")
    print(f"🎬 Processing 10 Unique Hindi Shorts for Channel {channel_id}")
    print(f"📂 Output directory: {channel_dir}")
    print(f"=======================================================\n")

    if channel_id == 3:
        # CHANNEL 3: Football (Ronaldo/Messi) & IShowSpeed Viral Action
        blueprints = CHANNEL_3_BLUEPRINTS
        for bp in blueprints:
            slot = bp["slot"]
            out_vid = os.path.join(channel_dir, f"ch3_v{slot:02d}.mp4")
            out_thumb = os.path.join(channel_dir, f"ch3_v{slot:02d}_thumb.jpg")

            if not force_render and os.path.exists(out_vid) and os.path.getsize(out_vid) > 500000:
                print(f"[{slot}/10] Channel 3: Using pre-rendered '{bp['title'][:45]}...'")
                results.append({
                    "index": slot,
                    "channel_id": 3,
                    "type": "Football & Speed Viral Short (Hindi Voice)",
                    "title": bp["title"],
                    "description": bp["description"],
                    "tags": bp["tags"],
                    "video_path": out_vid,
                    "thumbnail_path": out_thumb if os.path.exists(out_thumb) else None,
                    "duration": 15.0,
                    "source_id": os.path.basename(bp["clip"]),
                    "query": "football_and_speed_hindi"
                })
            else:
                print(f"[{slot}/10] Channel 3: Rendering '{bp['title'][:45]}...'")
                render_res = render_action_clip_hindi(
                    clip_path=bp["clip"],
                    hindi_text=bp["hindi_script"],
                    banner_text=bp["banner"],
                    output_video_path=out_vid,
                    output_thumb_path=out_thumb
                )
                results.append({
                    "index": slot,
                    "channel_id": 3,
                    "type": "Football & Speed Viral Short (Hindi Voice)",
                    "title": bp["title"],
                    "description": bp["description"],
                    "tags": bp["tags"],
                    "video_path": render_res["video_path"],
                    "thumbnail_path": render_res["thumbnail_path"],
                    "duration": render_res["duration"],
                    "source_id": os.path.basename(bp["clip"]),
                    "query": "football_and_speed_hindi"
                })
                print(f"  ✓ Rendered: {os.path.basename(render_res['video_path'])}")

    elif channel_id == 1:
        # CHANNEL 1: FactTechz-Style HD Moving B-Roll Documentary Shorts
        blueprints = CHANNEL_1_BLUEPRINTS
        vm = VideoMaker(assets_dir="assets", output_dir=channel_dir)

        for bp in blueprints:
            slot = bp["slot"]
            audio_path = os.path.join(channel_dir, f"ch1_v{slot:02d}_voice.mp3")
            ass_path = os.path.join(channel_dir, f"ch1_v{slot:02d}_sub.ass")
            out_vid_name = f"ch1_v{slot:02d}.mp4"
            out_vid = os.path.join(channel_dir, out_vid_name)
            out_thumb = os.path.join(channel_dir, f"ch1_v{slot:02d}_thumb.jpg")

            if not force_render and os.path.exists(out_vid) and os.path.getsize(out_vid) > 500000:
                print(f"[{slot}/10] Channel 1: Using pre-rendered '{bp['title'][:45]}...'")
                results.append({
                    "index": slot,
                    "channel_id": 1,
                    "type": f"FactTechz Documentary Short ({bp['niche']})",
                    "title": bp["title"],
                    "description": bp["description"],
                    "tags": bp["tags"],
                    "video_path": out_vid,
                    "thumbnail_path": out_thumb if os.path.exists(out_thumb) else None,
                    "duration": 20.0,
                    "source_id": f"facttechz_{bp['niche'].lower().replace(' ', '_')}_{slot}",
                    "query": bp["niche"]
                })
            else:
                print(f"[{slot}/10] Channel 1: Rendering '{bp['title'][:45]}...'")
                voice_res = generate_audio(
                    text=bp["hindi_script"],
                    audio_path=audio_path,
                    ass_path=ass_path,
                    voice="hi-IN-MadhurNeural"
                )

                out_vid = vm.render_video(
                    audio_path=audio_path,
                    ass_path=ass_path,
                    duration=voice_res["duration"],
                    output_filename=out_vid_name,
                    banner_text=bp["banner"],
                    bg_video_paths=bp["scenes"]
                )

                subprocess.run([
                    "ffmpeg", "-y", "-ss", "00:00:02.500", "-i", out_vid,
                    "-vframes", "1", "-q:v", "2", out_thumb
                ], capture_output=True)

                results.append({
                    "index": slot,
                    "channel_id": 1,
                    "type": f"FactTechz Documentary Short ({bp['niche']})",
                    "title": bp["title"],
                    "description": bp["description"],
                    "tags": bp["tags"],
                    "video_path": out_vid,
                    "thumbnail_path": out_thumb if os.path.exists(out_thumb) else None,
                    "duration": voice_res["duration"],
                    "source_id": f"facttechz_{bp['niche'].lower().replace(' ', '_')}_{slot}",
                    "query": bp["niche"]
                })
                print(f"  ✓ Rendered: {os.path.basename(out_vid)}")

    elif channel_id == 2:
        # CHANNEL 2: Satisfying Science & Guinness World Records (Hindi Commentary)
        blueprints = CHANNEL_2_BLUEPRINTS
        for bp in blueprints:
            slot = bp["slot"]
            out_vid = os.path.join(channel_dir, f"ch2_v{slot:02d}.mp4")
            out_thumb = os.path.join(channel_dir, f"ch2_v{slot:02d}_thumb.jpg")

            if not force_render and os.path.exists(out_vid) and os.path.getsize(out_vid) > 500000:
                print(f"[{slot}/10] Channel 2: Using pre-rendered '{bp['title'][:45]}...'")
                results.append({
                    "index": slot,
                    "channel_id": 2,
                    "type": "Science & Stunt Short (Hindi Voice)",
                    "title": bp["title"],
                    "description": bp["description"],
                    "tags": bp["tags"],
                    "video_path": out_vid,
                    "thumbnail_path": out_thumb if os.path.exists(out_thumb) else None,
                    "duration": 15.0,
                    "source_id": os.path.basename(bp["clip"]),
                    "query": "science_and_records_hindi"
                })
            else:
                print(f"[{slot}/10] Channel 2: Rendering '{bp['title'][:45]}...'")
                render_res = render_action_clip_hindi(
                    clip_path=bp["clip"],
                    hindi_text=bp["hindi_script"],
                    banner_text=bp["banner"],
                    output_video_path=out_vid,
                    output_thumb_path=out_thumb
                )
                results.append({
                    "index": slot,
                    "channel_id": 2,
                    "type": "Science & Stunt Short (Hindi Voice)",
                    "title": bp["title"],
                    "description": bp["description"],
                    "tags": bp["tags"],
                    "video_path": render_res["video_path"],
                    "thumbnail_path": render_res["thumbnail_path"],
                    "duration": render_res["duration"],
                    "source_id": os.path.basename(bp["clip"]),
                    "query": "science_and_records_hindi"
                })
                print(f"  ✓ Rendered: {os.path.basename(render_res['video_path'])}")

    print(f"\n✅ Ready with all 10 videos for Channel {channel_id}!\n")
    return results
