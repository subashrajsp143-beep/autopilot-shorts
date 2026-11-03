"""
Action Hindi Renderer
---------------------
Takes viral creator / sports / science action footage, formats into 1080x1920
with sleek high-retention top hook banner, crisp original audio (or optional Hindi commentary),
and lower-third subtitles.
"""

import os
import sys
import re
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
    if os.path.exists("C:/Windows/Fonts/arialbd.ttf"):
        return "fontfile='C\\:/Windows/Fonts/arialbd.ttf':"
    if os.path.exists("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
        return "fontfile='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf':"
    return ""


def clean_text(text: str) -> str:
    """Cleans text for FFmpeg drawtext."""
    clean = re.sub(r'[^\w\s!?,.$#@\-%/:]', '', text)
    clean = clean.replace(":", "\\:").replace("'", "").replace('"', "").strip()
    return clean or "VIRAL MOMENT"


def render_action_clip_hindi(
    clip_path: str,
    hindi_text: str,
    banner_text: str,
    output_video_path: str,
    output_thumb_path: Optional[str] = None,
    target_duration: Optional[float] = None,
    use_ai_voice: bool = False
) -> Dict[str, Any]:
    """
    Renders an action short formatted to vertical 1080x1920 with a sleek top-hook banner.
    If use_ai_voice is False, preserves 100% of authentic original sound (crowd roar, live screams, commentary).
    """
    os.makedirs(os.path.dirname(output_video_path), exist_ok=True)
    base_name = os.path.splitext(output_video_path)[0]
    font_opt = get_font_option()
    clean_banner = clean_text(banner_text)

    # Sleek Red Pill Top Hook Banner at y=160
    banner_filter = (
        f"drawtext={font_opt}text='{clean_banner}':"
        f"fontsize=50:fontcolor=white:box=1:boxcolor=0xDD0000@0.95:boxborderw=16:"
        f"x=(w-text_w)/2:y=160"
    )

    if not use_ai_voice or not hindi_text:
        # PURE AUTHENTIC ORIGINAL SOUND (No AI voice)
        # Probe duration of clip
        try:
            dur_cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", clip_path]
            clip_dur = float(subprocess.check_output(dur_cmd, text=True).strip())
        except Exception:
            clip_dur = 25.0

        duration = min(clip_dur, target_duration or 30.0)

        filter_complex = f"[0:v]trim=duration={duration:.2f},scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,{banner_filter}[vout]"

        cmd = [
            "ffmpeg", "-y",
            "-i", clip_path,
            "-filter_complex", filter_complex,
            "-map", "[vout]",
            "-map", "0:a?",
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-crf", "18",
            "-pix_fmt", "yuv420p",
            "-r", "30",
            "-c:a", "aac",
            "-b:a", "192k",
            "-t", f"{duration:.2f}",
            output_video_path
        ]
        voice_duration = 0.0
    else:
        # Optional AI Voiceover with lower-third subtitles
        audio_path = f"{base_name}_voice.mp3"
        ass_path = f"{base_name}_sub.ass"

        voice_res = generate_audio(
            text=hindi_text,
            audio_path=audio_path,
            ass_path=ass_path,
            voice="hi-IN-MadhurNeural"
        )
        voice_duration = voice_res["duration"]
        duration = target_duration if target_duration and target_duration > voice_duration else voice_duration + 0.5

        escaped_ass = ass_path.replace("\\", "/").replace(":", r"\:")
        filter_complex = (
            f"[0:v]trim=duration={duration:.2f},scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,{banner_filter},subtitles='{escaped_ass}'[vout];"
            f"[0:a]volume=0.20[bg_audio];"
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
            "-crf", "18",
            "-pix_fmt", "yuv420p",
            "-r", "30",
            "-c:a", "aac",
            "-b:a", "192k",
            "-t", f"{duration:.2f}",
            output_video_path
        ]

    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"FFmpeg render failed: {res.stderr[-400:]}")

    # Generate High-Impact Thumbnail at 2.5s
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
