"""
Action Hindi Renderer
---------------------
Takes viral creator / sports / science action footage, generates high-energy
Hindi neural voiceover commentary (hi-IN-MadhurNeural), ducks background
audio to 15%, adds dynamic center-screen yellow subtitles (Hormozi style),
and burns a high-impact top banner.
"""

import os
import sys
import subprocess
from typing import Dict, Any, Optional

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from src.voice_generator import generate_audio


def get_font_option() -> str:
    """Finds best font for Windows and Linux."""
    if os.path.exists("C:/Windows/Fonts/impact.ttf"):
        return "fontfile='C\\:/Windows/Fonts/impact.ttf':"
    if os.path.exists("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
        return "fontfile='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf':"
    return ""


def clean_text(text: str) -> str:
    """Cleans text for FFmpeg drawtext."""
    import re
    # Remove emojis and non-ascii for drawtext safety
    clean = re.sub(r'[^\x00-\x7F]+', '', text)
    clean = clean.replace(":", "\\:").replace("'", "").replace('"', "").strip()
    return clean or "VIRAL MOMENT"


def render_action_clip_hindi(
    clip_path: str,
    hindi_text: str,
    banner_text: str,
    output_video_path: str,
    output_thumb_path: Optional[str] = None,
    target_duration: Optional[float] = None
) -> Dict[str, Any]:
    """
    Renders an action short with Hindi neural voiceover, ducked original sound,
    synced yellow subtitles, and high-impact top banner.
    """
    os.makedirs(os.path.dirname(output_video_path), exist_ok=True)
    base_name = os.path.splitext(output_video_path)[0]
    audio_path = f"{base_name}_voice.mp3"
    ass_path = f"{base_name}_sub.ass"

    # 1. Synthesize Hindi Commentary
    voice_res = generate_audio(
        text=hindi_text,
        audio_path=audio_path,
        ass_path=ass_path,
        voice="hi-IN-MadhurNeural"
    )
    voice_duration = voice_res["duration"]
    duration = target_duration if target_duration and target_duration > voice_duration else voice_duration + 0.5

    # 2. Build FFmpeg Filter Complex
    escaped_ass = ass_path.replace("\\", "/").replace(":", r"\:")
    font_opt = get_font_option()
    clean_banner = clean_text(banner_text)
    banner_filter = f"drawtext={font_opt}text='{clean_banner}':fontsize=52:fontcolor=yellow:box=1:boxcolor=black@0.85:boxborderw=20:x=(w-text_w)/2:y=280,"

    filter_complex = (
        f"[0:v]trim=duration={duration:.2f},scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,{banner_filter}subtitles='{escaped_ass}'[vout];"
        f"[0:a]volume=0.15[bg_audio];"
        f"[1:a]volume=1.0[voice_audio];"
        f"[voice_audio][bg_audio]amix=inputs=2:duration=first[aout]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-stream_loop", "-1", "-i", clip_path,
        "-i", audio_path,
        "-filter_complex", filter_complex,
        "-map", "[vout]",
        "-map", "[aout]",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "22",
        "-pix_fmt", "yuv420p",
        "-r", "30",
        "-c:a", "aac",
        "-b:a", "192k",
        "-t", f"{duration:.2f}",
        output_video_path
    ]

    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        # Fallback if source video has no audio stream
        fallback_filter = (
            f"[0:v]trim=duration={duration:.2f},scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,{banner_filter}subtitles='{escaped_ass}'[vout]"
        )
        cmd_no_bg = [
            "ffmpeg", "-y",
            "-stream_loop", "-1", "-i", clip_path,
            "-i", audio_path,
            "-filter_complex", fallback_filter,
            "-map", "[vout]",
            "-map", "1:a",
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-crf", "22",
            "-pix_fmt", "yuv420p",
            "-r", "30",
            "-c:a", "aac",
            "-b:a", "192k",
            "-t", f"{duration:.2f}",
            output_video_path
        ]
        res2 = subprocess.run(cmd_no_bg, capture_output=True, text=True)
        if res2.returncode != 0:
            raise RuntimeError(f"FFmpeg render failed: {res.stderr[-400:]}")

    # 3. Generate High-Impact Thumbnail
    thumb_path = output_thumb_path or f"{base_name}_thumb.jpg"
    thumb_cmd = [
        "ffmpeg", "-y",
        "-ss", "00:00:02.500",
        "-i", output_video_path,
        "-vframes", "1",
        "-q:v", "2",
        thumb_path
    ]
    subprocess.run(thumb_cmd, capture_output=True, text=True)

    return {
        "video_path": output_video_path,
        "thumbnail_path": thumb_path if os.path.exists(thumb_path) else None,
        "duration": duration,
        "voice_duration": voice_duration
    }
