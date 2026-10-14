"""
Viral Creator Clipper Engine (MrBeast, IShowSpeed, Podcasts, Influencers)
Downloads real viral video clips, converts them into 9:16 vertical Shorts/Reels
with top eye-catching hook banners and original creator audio.
"""

import os
import subprocess
import json
import re
import glob
from typing import Dict, Any, Optional, List


VIRAL_CREATOR_PRESETS = [
    {
        "query": "MrBeast challenge viral moments",
        "title": "मिस्टर बीस्ट का 50 करोड़ का चैलेंज! 😱 MR BEAST CRAZY CHALLENGE #Shorts #MrBeastHindi #Viral",
        "description": "मिस्टर बीस्ट का अब तक का सबसे हैरान कर देने वाला चैलेंज!\n\n#Shorts #MrBeast #MrBeastHindi #ViralShorts #Trending",
        "tags": ["mrbeast hindi", "mrbeast", "shorts", "hindi shorts", "viral shorts", "trending"],
        "banner": "MR BEAST KA 50 CRORE CHALLENGE! 😱"
    },
    {
        "query": "IShowSpeed funny rage reaction moments",
        "title": "स्पीड का सबसे पागलपन भरा रिएक्शन! 😂🔥 SPEED CRAZY MOMENTS #Shorts #IShowSpeed #Hindi",
        "description": "स्पीड का यह रिएक्शन देखकर आपकी हंसी नहीं रुकेगी!\n\n#Shorts #IShowSpeed #SpeedHindi #FunnyShorts #Viral",
        "tags": ["ishowspeed", "speed clips", "funny shorts", "hindi shorts", "shorts", "viral"],
        "banner": "SPEED KA SABSE CRAZY REACTION! 😂"
    },
    {
        "query": "MrBeast giving away money reaction",
        "title": "मिस्टर बीस्ट ने दिया 10 लाख डॉलर कैश! 💰 MR BEAST CASH GIVEAWAY #Shorts #MrBeastHindi",
        "description": "जब मिस्टर बीस्ट ने अनजान लड़के को करोड़ों रुपये दे दिए!\n\n#Shorts #MrBeast #MrBeastHindi #MoneyChallenge #Viral",
        "tags": ["mrbeast hindi", "million dollars", "mrbeast giveaway", "shorts", "hindi"],
        "banner": "10 LAKH DOLLAR CASH DE DIYA! 💰"
    },
    {
        "query": "IShowSpeed meeting Ronaldo",
        "title": "स्पीड जब रोनाल्डो से पहली बार मिला! 🐐 SPEED FINALLY MEETS RONALDO #Shorts #IShowSpeed #CR7",
        "description": "स्पीड और क्रिस्टियानो रोनाल्डो का सबसे यादगार पल!\n\n#Shorts #IShowSpeed #Ronaldo #CR7 #HindiShorts",
        "tags": ["ishowspeed", "ronaldo", "cr7", "speed and ronaldo", "shorts", "hindi"],
        "banner": "SPEED MEETS RONALDO! 🐐🔥"
    },
    {
        "query": "MrBeast impossible escape room",
        "title": "दुनिया का सबसे खतरनाक एस्केप रूम! 🔒🔥 MR BEAST IMPOSSIBLE ESCAPE #Shorts #MrBeastHindi",
        "description": "क्या ये लोग दुनिया के सबसे मुश्किल कमरे से बाहर निकल पाए?\n\n#Shorts #MrBeast #EscapeRoom #ViralShorts #Hindi",
        "tags": ["mrbeast", "escape room", "mrbeast hindi", "challenge", "shorts"],
        "banner": "DUNIYA KA SABSE KHATARNAK ESCAPE! 🔒"
    }
]


class CreatorClipper:
    """Clips real creator videos into 9:16 vertical Shorts."""

    def __init__(self, downloads_dir: str = "assets/downloads", output_dir: str = "output"):
        self.downloads_dir = downloads_dir
        self.output_dir = output_dir
        os.makedirs(self.downloads_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)

    def download_by_search_or_url(self, search_query_or_url: str, output_prefix: str = "creator") -> str:
        """Downloads a video clip using yt-dlp search or direct URL."""
        if search_query_or_url.startswith("http://") or search_query_or_url.startswith("https://"):
            target = search_query_or_url
        else:
            target = f"ytsearch1:{search_query_or_url}"

        output_tmpl = os.path.join(self.downloads_dir, f"{output_prefix}_%(id)s.%(ext)s")
        cmd = [
            "yt-dlp",
            "-f", "bv*[height<=1080]+ba/b[height<=1080]/bv*+ba/best",
            "--merge-output-format", "mp4",
            "-o", output_tmpl,
            "--no-playlist",
            target
        ]

        print(f"Downloading creator clip for: '{search_query_or_url}'...")
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode != 0:
            print("yt-dlp warning:", res.stderr[-300:])
            # Fallback format if error
            cmd_fb = [
                "yt-dlp",
                "-f", "best",
                "-o", output_tmpl,
                "--no-playlist",
                target
            ]
            res = subprocess.run(cmd_fb, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Detect downloaded file
        candidates = glob.glob(os.path.join(self.downloads_dir, f"{output_prefix}_*.*"))
        valid = [f for f in candidates if not f.endswith(".part") and os.path.getsize(f) > 100000]
        if valid:
            valid.sort(key=os.path.getmtime, reverse=True)
            return valid[0]

        # Scan any downloaded mp4/webm in downloads
        all_vids = glob.glob(os.path.join(self.downloads_dir, "*.*"))
        vids = [f for f in all_vids if f.endswith((".mp4", ".webm", ".mkv")) and not f.endswith(".part")]
        if vids:
            vids.sort(key=os.path.getmtime, reverse=True)
            return vids[0]

        raise FileNotFoundError(f"Failed to download clip for '{search_query_or_url}'.")

    def create_viral_short_clip(
        self,
        video_path: str,
        banner_text: str,
        output_filename: str,
        start_time: float = 0,
        duration: float = 30.0
    ) -> str:
        """
        Converts real creator video into a 1080x1920 vertical Short.
        - Studio blurred background
        - Sharp centered moving creator video
        - Top viral hook banner
        - Original creator sound and voice
        """
        output_path = os.path.join(self.output_dir, output_filename)
        clean_banner = banner_text.replace(":", "\\:").replace("'", "").replace('"', "")

        # Select available font cross-platform (Windows & Linux / Ubuntu)
        font_opt = ""
        if os.path.exists("C:/Windows/Fonts/impact.ttf"):
            font_opt = "fontfile='C\\:/Windows/Fonts/impact.ttf':"
        elif os.path.exists("C:/Windows/Fonts/arialbd.ttf"):
            font_opt = "fontfile='C\\:/Windows/Fonts/arialbd.ttf':"
        elif os.path.exists("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
            font_opt = "fontfile='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf':"
        elif os.path.exists("/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"):
            font_opt = "fontfile='/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf':"
        elif os.path.exists("/usr/share/fonts/truetype/freefont/FreeSansBold.ttf"):
            font_opt = "fontfile='/usr/share/fonts/truetype/freefont/FreeSansBold.ttf':"

        filter_complex = (
            "[0:v]split=2[bg][fg];"
            "[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5[bgblur];"
            "[fg]scale=1080:-1[fgscaled];"
            "[bgblur][fgscaled]overlay=(W-w)/2:(H-h)/2[base];"
            f"[base]drawtext={font_opt}text='{clean_banner}':fontsize=54:fontcolor=yellow:box=1:boxcolor=black@0.75:boxborderw=20:x=(w-text_w)/2:y=280[v]"
        )

        cmd = [
            "ffmpeg", "-y",
            "-ss", str(start_time),
            "-i", video_path,
            "-t", str(duration),
            "-filter_complex", filter_complex,
            "-map", "[v]",
            "-map", "0:a?",
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "22",
            "-c:a", "aac",
            "-b:a", "192k",
            output_path
        ]

        print(f"Rendering 9:16 vertical short -> {output_path}...")
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode != 0:
            print("FFmpeg error:", res.stderr[-500:])
            raise RuntimeError(f"FFmpeg clipping failed: {res.stderr[-200:]}")

        print(f"✓ Creator short rendered: {output_path}")
        return output_path


if __name__ == "__main__":
    clipper = CreatorClipper()
    print("Creator Clipper initialized.")
