"""
Viral Creator Clipper Engine (MrBeast, Podcasts, Influencers)
Downloads long YouTube videos, extracts viral 30-50s moments,
converts them into 9:16 vertical Shorts/Reels with top hook banners.
"""

import os
import subprocess
import json
import re
from typing import Dict, Any, Optional, List


class CreatorClipper:
    """Clips long-form creator videos into 9:16 vertical Shorts."""

    def __init__(self, downloads_dir: str = "assets/downloads", output_dir: str = "output"):
        self.downloads_dir = downloads_dir
        self.output_dir = output_dir
        os.makedirs(self.downloads_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)

    def download_youtube_video(self, url: str, filename_prefix: str = "video") -> str:
        """Downloads YouTube video in 1080p/720p MP4 format using yt-dlp."""
        output_template = os.path.join(self.downloads_dir, f"{filename_prefix}_%(id)s.%(ext)s")
        cmd = [
            "yt-dlp",
            "-f", "bestvideo[ext=mp4][height<=1080]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "--merge-output-format", "mp4",
            "-o", output_template,
            url
        ]

        print(f"Downloading video from {url}...")
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode != 0:
            print("yt-dlp error:", res.stderr[-500:])
            raise RuntimeError(f"Failed to download video: {res.stderr[-200:]}")

        # Find downloaded file
        for line in res.stdout.splitlines():
            if "[Merger] Merging formats into" in line or "[download] Destination:" in line:
                match = re.search(r'"([^"]+\.mp4)"|Destination:\s*(.+)$', line)
                if match:
                    path = match.group(1) or match.group(2)
                    if os.path.exists(path):
                        return path

        # Fallback: scan downloads dir
        files = [os.path.join(self.downloads_dir, f) for f in os.listdir(self.downloads_dir) if f.endswith(".mp4")]
        if files:
            files.sort(key=os.path.getmtime, reverse=True)
            return files[0]

        raise FileNotFoundError("Could not find downloaded MP4 video.")

    def create_viral_short_clip(
        self,
        video_path: str,
        start_time: str,
        duration: float,
        banner_text: str,
        output_filename: str,
        style: str = "blurred_bg"  # 'blurred_bg' or 'center_crop'
    ) -> str:
        """
        Clips the video segment and reformats it into a 1080x1920 vertical Short.
        Adds a top eye-catching hook banner in viral creator style.
        """
        output_path = os.path.join(self.output_dir, output_filename)

        # Clean banner text for FFmpeg drawtext
        clean_banner = banner_text.replace(":", "\\:").replace("'", "").replace('"', "")

        cmd = [
            "ffmpeg", "-y",
            "-ss", str(start_time),
            "-i", video_path,
            "-t", str(duration)
        ]

        if style == "blurred_bg":
            # Studio blurred background with sharp centered video + top banner
            filter_complex = (
                "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=20:5[bg];"
                "[0:v]scale=1080:720:force_original_aspect_ratio=decrease[fg];"
                "[bg][fg]overlay=(W-w)/2:(H-h)/2[combined];"
                f"[combined]drawtext=font='Arial':text='{clean_banner}':fontsize=48:fontcolor=white:box=1:boxcolor=black@0.7:boxborderw=14:x=(w-text_w)/2:y=180[vout]"
            )
            cmd += ["-filter_complex", filter_complex, "-map", "[vout]", "-map", "0:a?"]
        else:
            # Direct center crop
            filter_complex = (
                "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
                f"drawtext=font='Arial':text='{clean_banner}':fontsize=48:fontcolor=white:box=1:boxcolor=black@0.7:boxborderw=14:x=(w-text_w)/2:y=180"
            )
            cmd += ["-vf", filter_complex]

        cmd += [
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-crf", "22",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "192k",
            output_path
        ]

        print(f"Creating viral short clip -> {output_path}...")
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode != 0:
            print("FFmpeg error:", res.stderr[-500:])
            raise RuntimeError(f"FFmpeg clipping failed: {res.stderr[-200:]}")

        print(f"Viral clip ready: {output_path}")
        return output_path


if __name__ == "__main__":
    clipper = CreatorClipper()
    print("Creator Clipper initialized.")
