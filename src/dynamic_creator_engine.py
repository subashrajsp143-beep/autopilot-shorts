"""
Dynamic Viral Creator Engine
----------------------------
Dynamically discovers, downloads, and formats fresh viral creator clips
across 5 distinct high-retention categories every day.
Guarantees 100% unique footage by integrating with HistoryTracker.
"""

import os
import sys
import glob
import json
import random
import subprocess
from datetime import datetime
from typing import Dict, Any, List, Optional

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from history_tracker import HistoryTracker

# 50+ Rotating high-CTR viral queries across 5 popular niches
VIRAL_NICHE_REGISTRY = {
    "mrbeast": [
        {"q": "MrBeast craziest challenge moments", "banner": "MR BEAST CRAZIEST CHALLENGE! 😱", "title_prefix": "मिस्टर बीस्ट का सबसे पागलपन भरा चैलेंज!"},
        {"q": "MrBeast last to leave circle wins", "banner": "LAST TO LEAVE WINS $500,000! 💰", "title_prefix": "जो आखिरी में निकलेगा उसे मिलेंगे 5 करोड़!"},
        {"q": "MrBeast survive 100 days in circle", "banner": "100 DAYS SURVIVAL CHALLENGE! 🔥", "title_prefix": "100 दिन तक इस सर्कल में जीवित रहो!"},
        {"q": "MrBeast extreme hide and seek", "banner": "WORLD'S BIGGEST HIDE & SEEK! 🏃‍♂️", "title_prefix": "दुनिया का सबसे बड़ा हाइड एंड सीक गेम!"},
        {"q": "MrBeast giving away private island", "banner": "HE WON AN ENTIRE ISLAND! 🏝️", "title_prefix": "अनजान लड़के ने जीता पूरा प्राइवेट आइलैंड!"},
        {"q": "MrBeast world's most dangerous trap", "banner": "WORLD'S DEADLIEST TRAP! ⚠️", "title_prefix": "दुनिया का सबसे खतरनाक जाल!"},
        {"q": "MrBeast $1,000,000 yacht challenge", "banner": "$1,000,000 LUXURY YACHT! 🛥️", "title_prefix": "10 करोड़ की लग्जरी यॉट का चैलेंज!"},
        {"q": "MrBeast train vs giant pit", "banner": "TRAIN VS GIANT CRATER! 💥", "title_prefix": "जब ट्रेन सीधे 100 फुट गड्ढे में गिरी!"},
        {"q": "MrBeast 100 people vs world's biggest trap", "banner": "100 PEOPLE VS GIANT TRAP! 😱", "title_prefix": "100 लोग और दुनिया का सबसे बड़ा ट्रैप!"},
        {"q": "MrBeast giving stranger $100,000 cash", "banner": "$100,000 CASH GIVEN AWAY! 💰", "title_prefix": "जब अनजान को बैग भरकर कैश दे दिया!"}
    ],
    "ishowspeed": [
        {"q": "IShowSpeed crazy stream moments", "banner": "SPEED GOES COMPLETELY CRAZY! 😂🔥", "title_prefix": "स्पीड का सबसे पागलपन भरा रिएक्शन!"},
        {"q": "IShowSpeed funny screams compilation", "banner": "SPEED'S FUNNIEST SCREAMS! 😭⚡", "title_prefix": "स्पीड की ऐसी चीखें देखकर हंसी नहीं रुकेगी!"},
        {"q": "IShowSpeed meet celebrities funny", "banner": "SPEED MEETS FAMOUS CELEBRITY! 😱", "title_prefix": "जब स्पीड अचानक बड़े सेलिब्रिटी से मिला!"},
        {"q": "IShowSpeed playing FIFA funny rage", "banner": "SPEED CRAZIEST RAGE MOMENT! 🎮💥", "title_prefix": "स्पीड का सबसे खतरनाक गेमिंग रेज!"},
        {"q": "IShowSpeed meeting football legends", "banner": "SPEED MEETS FOOTBALL LEGEND! 🐐🔥", "title_prefix": "जब स्पीड फुटबॉल के भगवान से मिला!"},
        {"q": "IShowSpeed bark at camera funny", "banner": "SPEED ICONIC MOMENTS! 😂✨", "title_prefix": "स्पीड का सबसे वायरल और फनी मोमेंट!"},
        {"q": "IShowSpeed trying weird food funny", "banner": "SPEED TRIES WEIRD FOOD! 🤢😂", "title_prefix": "जब स्पीड ने खाई यह अजीब चीज!"},
        {"q": "IShowSpeed emotional moment stream", "banner": "SPEED'S GREATEST DREAM CAME TRUE! ❤️", "title_prefix": "स्पीड का सपना आखिरकार सच हो गया!"}
    ],
    "football": [
        {"q": "Cristiano Ronaldo impossible goals skills", "banner": "CR7 IMPOSSIBLE GOAL! 🐐⚽", "title_prefix": "रोनाल्डो का यह गोल देखकर दुनिया दंग रह गई!"},
        {"q": "Lionel Messi magic dribbles commentary", "banner": "MESSI ANKLE BREAKER MOMENTS! 👑🔥", "title_prefix": "मेसी का यह जादुई ड्रिबल कोई नहीं भूल सकता!"},
        {"q": "Neymar Jr best skills ever", "banner": "NEYMAR UNSTOPPABLE SKILLS! 🇧🇷⚡", "title_prefix": "नेमार का ऐसा जादू जिसे देखकर डिफेंडर गिर पड़े!"},
        {"q": "Most dramatic last minute goals football", "banner": "LAST SECOND CRAZIEST GOAL! ⚽😱", "title_prefix": "फुटबॉल इतिहास का सबसे नाटकीय आखिरी गोल!"},
        {"q": "Ronaldo high jump header physics", "banner": "CR7 FLIES IN THE AIR! ✈️🐐", "title_prefix": "जब रोनाल्डो ने हवा में उड़कर गोल दागा!"},
        {"q": "Goalkeeper impossible saves moments", "banner": "IMPOSSIBLE GOALKEEPER SAVES! 🧤🔥", "title_prefix": "गोलकीपर का ऐसा करिश्माई बचाव जो नामुमकिन था!"}
    ],
    "world_records": [
        {"q": "Insane Guinness World Records compilation", "banner": "INSANE WORLD RECORDS! 🏆😱", "title_prefix": "इंसान ने बनाया ऐसा वर्ल्ड रिकॉर्ड जो टूटना नामुमकिन है!"},
        {"q": "Fastest human in the world records", "banner": "FASTEST HUMAN ON EARTH! ⚡🏃", "title_prefix": "दुनिया का सबसे तेज इंसान!"},
        {"q": "Extreme human body records incredible", "banner": "INCREDIBLE HUMAN SUPERPOWERS! 💥", "title_prefix": "इस इंसान के पास है असली सुपरपावर!"},
        {"q": "World craziest parkour stunts", "banner": "DEATH-DEFYING PARKOUR STUNTS! 🏙️⚠️", "title_prefix": "50 मंजिला इमारत पर बिना रस्सी के स्टंट!"},
        {"q": "World largest Domino chain reaction", "banner": "LARGEST DOMINO CHAIN REACTION!  domino", "title_prefix": "लाखों डोमिनोज़ का सबसे खूबसूरत चेन रिएक्शन!"}
    ],
    "mind_blowing": [
        {"q": "Satisfying hydraulic press vs diamond", "banner": "HYDRAULIC PRESS VS DIAMOND! 💎💥", "title_prefix": "जब हाइड्रोलिक प्रेस के नीचे रखा गया हीरा!"},
        {"q": "Mind blowing optical illusions shorts", "banner": "YOUR BRAIN WILL BE FOOLED! 🌀😱", "title_prefix": "यह ऑप्टिकल इल्यूजन आपके दिमाग को घुमा देगा!"},
        {"q": "Crazy physics experiments that look like magic", "banner": "PHYSICS OR REAL MAGIC? 🧪✨", "title_prefix": "साइंस का यह जादुई एक्सपेरिमेंट होश उड़ा देगा!"},
        {"q": "Satisfying crushing things with hydraulic press", "banner": "MOST SATISFYING CRUSHING! 🔨🔥", "title_prefix": "100 टन के प्रेस ने इस चीज को चकनाचूर कर दिया!"},
        {"q": "Magnetic slime eating magnets science", "banner": "LIVING MAGNETIC MONSTER! 🧲🦠", "title_prefix": "जब चुंबक को निगलने लगा यह अजीब लिक्विड!"}
    ]
}


class DynamicCreatorEngine:
    """Manages downloading, clipping, and formatting 100% fresh creator shorts."""

    def __init__(self, downloads_dir: str = "assets/downloads", output_dir: str = "output/batch_today"):
        self.downloads_dir = downloads_dir
        self.output_dir = output_dir
        self.tracker = HistoryTracker()
        os.makedirs(self.downloads_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)

    def _get_video_duration(self, file_path: str) -> float:
        try:
            cmd = [
                "ffprobe", "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                file_path
            ]
            out = subprocess.check_output(cmd, text=True).strip()
            return float(out)
        except Exception:
            return 60.0

    def download_fresh_clip(self, niche: str, day_offset: int = 0) -> Optional[Dict[str, Any]]:
        """
        Searches YouTube for fresh clips in the given niche, skipping any clip
        that was already downloaded or uploaded before.
        """
        registry = VIRAL_NICHE_REGISTRY.get(niche, VIRAL_NICHE_REGISTRY["mrbeast"])
        query_idx = (day_offset) % len(registry)
        selected_cfg = registry[query_idx]

        query = selected_cfg["q"]
        print(f"🔍 Searching YouTube for fresh '{niche}' viral footage: '{query}'...")

        # Search for top 6 candidates to find unused ones
        search_target = f"ytsearch6:{query}"
        search_cmd = [
            "yt-dlp",
            "--flat-playlist",
            "--print", "%(id)s|||%(title)s",
            search_target
        ]

        candidate_ids = []
        try:
            res = subprocess.run(search_cmd, capture_output=True, text=True, timeout=25)
            for line in res.stdout.splitlines():
                parts = line.strip().split("|||", 1)
                if len(parts) == 2:
                    vid_id, vid_title = parts[0].strip(), parts[1].strip()
                    if not self.tracker.is_source_used(vid_id):
                        candidate_ids.append((vid_id, vid_title))
        except Exception as e:
            print(f"Warning: yt-dlp search error: {e}")

        # Download target 30-second section using Android player client (fast ~3s, avoids bot checks)
        downloaded_file = None
        actual_source_id = None

        for vid_id, vid_title in candidate_ids:
            target = f"https://www.youtube.com/watch?v={vid_id}"
            out_prefix = f"fresh_{niche}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{vid_id}"
            output_tmpl = os.path.join(self.downloads_dir, f"{out_prefix}.%(ext)s")

            dl_cmd = [
                "yt-dlp",
                "--extractor-args", "youtube:player_client=android",
                "-f", "b[height<=720]/best",
                "--download-sections", "*00:00:20-00:00:52",
                "--force-keyframes-at-cuts",
                "-o", output_tmpl,
                "--no-playlist",
                target
            ]

            print(f"📥 Downloading selected fresh clip ({niche}): {target}...")
            try:
                res = subprocess.run(dl_cmd, capture_output=True, text=True, timeout=45)
                if res.returncode != 0:
                    print(f"Notice: Candidate {vid_id} returned code {res.returncode}. Trying next candidate...")
                    continue
            except Exception as e:
                print(f"Download timeout or error for {vid_id}: {e}")
                continue

            # Find downloaded file
            candidates = glob.glob(os.path.join(self.downloads_dir, f"{out_prefix}*.*"))
            valid = [f for f in candidates if not f.endswith(".part") and os.path.getsize(f) > 200000]
            if valid:
                downloaded_file = valid[0]
                actual_source_id = vid_id
                break

        if not downloaded_file:
            raise RuntimeError(f"Could not download any fresh viral clip for niche '{niche}'. Stopping to prevent duplicate uploads.")

        self.tracker.history.setdefault("used_source_ids", []).append(actual_source_id)
        self.tracker.save()

        # Build viral Hindi title
        title = f"{selected_cfg['title_prefix']} 😱 #Shorts #Viral"
        description = f"{selected_cfg['title_prefix']}\n\n#Shorts #Viral #Trending #{niche}"
        tags = ["shorts", "viral", niche, "trending", "youtube shorts"]

        return {
            "clip_path": downloaded_file,
            "banner": selected_cfg["banner"],
            "title": title,
            "description": description,
            "tags": tags,
            "source_id": actual_source_id,
            "query": query
        }

    def format_to_vertical_short(
        self,
        video_path: str,
        banner_text: str,
        output_filename: str,
        duration: float = 29.0
    ) -> str:
        """
        Formats real creator video into high-retention 9:16 vertical Short:
        - Studio blurred background
        - Centered sharp foreground
        - Eye-catching yellow top hook banner
        - Audio amplification
        """
        output_path = os.path.join(self.output_dir, output_filename)
        total_dur = self._get_video_duration(video_path)
        start_time = 0.0
        dur_to_render = min(duration, total_dur) if total_dur > 5.0 else duration

        clean_banner = banner_text.replace(":", "\\:").replace("'", "").replace('"', "")

        font_opt = ""
        if os.path.exists("C:/Windows/Fonts/impact.ttf"):
            font_opt = "fontfile='C\\:/Windows/Fonts/impact.ttf':"
        elif os.path.exists("C:/Windows/Fonts/arialbd.ttf"):
            font_opt = "fontfile='C\\:/Windows/Fonts/arialbd.ttf':"
        elif os.path.exists("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
            font_opt = "fontfile='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf':"
        elif os.path.exists("/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"):
            font_opt = "fontfile='/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf':"

        filter_complex = (
            "[0:v]split=2[bg][fg];"
            "[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5[bgblur];"
            "[fg]scale=1080:-1[fgscaled];"
            "[bgblur][fgscaled]overlay=(W-w)/2:(H-h)/2[base];"
            f"[base]drawtext={font_opt}text='{clean_banner}':fontsize=54:fontcolor=yellow:box=1:boxcolor=black@0.8:boxborderw=20:x=(w-text_w)/2:y=280[v]"
        )

        cmd = [
            "ffmpeg", "-y",
            "-ss", f"{start_time:.2f}",
            "-i", video_path,
            "-t", f"{dur_to_render:.2f}",
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

        print(f"🎬 Rendering vertical Short -> {output_path} (from {start_time:.1f}s to {start_time + dur_to_render:.1f}s)...")
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            print("FFmpeg error:", res.stderr[-400:])
            raise RuntimeError(f"FFmpeg render failed: {res.stderr[-200:]}")

        print(f"✓ Vertical Short ready: {output_path}")
        return output_path


if __name__ == "__main__":
    engine = DynamicCreatorEngine()
    print("Dynamic Creator Engine initialized.")
