"""
Dynamic Visual Storyboard Engine
Fetches topic-accurate HD visuals (Animals, Universe, Humans, Pyramids, Brain, Money)
and stitches them into a cinematic multi-scene 9:16 vertical video matching the voiceover.
"""

import os
import urllib.request
import json
import subprocess
from typing import List, Dict, Any, Optional
from PIL import Image, ImageDraw

USER_AGENT = "AutopilotShorts/1.0 (mailto:subashkum05@gmail.com)"

TOPIC_VISUAL_MAP = {
    # Animals & Nature
    "जानवर": "Wildlife",
    "सांप": "Snake",
    "शेर": "Lion",
    "टाइगर": "Tiger",
    "समुद्र": "Ocean",
    "मरियाना": "Mariana_Trench",
    "जीव": "Marine_biology",
    "प्रकृति": "Nature",
    
    # Universe & Science
    "चांद": "Moon",
    "अंतरिक्ष": "Universe",
    "ब्लैक होल": "Black_hole",
    "सूर्य": "Sun",
    "तारे": "Milky_Way",
    "वैज्ञानिक": "Albert_Einstein",
    "विज्ञान": "Science",

    # Humans & Psychology
    "इंसान": "Human",
    "आंख": "Human_eye",
    "दिमाग": "Human_brain",
    "पर्सनालिटी": "Face",
    "नींद": "Sleep",
    "चेहरा": "Portrait",
    "सोच": "Mind",
    "मजाक": "Human_behavior",

    # History & Ancient Wonders
    "पिरामिड": "Great_Pyramid_of_Giza",
    "मिस्र": "Ancient_Egypt",
    "इतिहास": "Ancient_history",
    "पत्थर": "Megalith",

    # Money & Success
    "पैसा": "Wealth",
    "अमीर": "Gold",
    "बैंक": "Banknotes",
    "कमाई": "Investment",
    "संपत्ति": "Real_estate",
}


class VisualStoryboard:
    """Manages scene detection, HD visual fetching, and video concatenation."""

    def __init__(self, cache_dir: str = "assets/image_cache"):
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)

    def _generate_fallback_image(self, filename: str, topic_label: str = "Universe") -> str:
        """Generates a high-res gradient background with Pillow if download fails."""
        filepath = os.path.join(self.cache_dir, filename)
        if os.path.exists(filepath):
            return filepath

        img = Image.new("RGB", (1080, 1920), color=(18, 22, 38))
        draw = ImageDraw.Draw(img)
        # Subtle dark ambient tones
        for y in range(0, 1920, 2):
            val = int(18 + (y / 1920) * 35)
            draw.line([(0, y), (1080, y)], fill=(val, val + 5, val + 20))
        img.save(filepath, "JPEG")
        return filepath

    def fetch_image_by_keyword(self, query: str) -> Optional[str]:
        """Fetches direct HD image URL from Wikimedia API."""
        try:
            url = f"https://en.wikipedia.org/w/api.php?action=query&titles={query}&prop=pageimages&format=json&pithumbsize=1080"
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=6) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                pages = data.get("query", {}).get("pages", {})
                for p in pages.values():
                    if "thumbnail" in p:
                        return p["thumbnail"]["source"]
        except Exception as e:
            print(f"Notice: Could not fetch image for '{query}': {e}")
        return None

    def download_image(self, image_url: str, filename: str) -> str:
        """Downloads image to local cache with fallback."""
        local_path = os.path.join(self.cache_dir, filename)
        if os.path.exists(local_path):
            return local_path

        try:
            req = urllib.request.Request(image_url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=8) as resp:
                with open(local_path, "wb") as f:
                    f.write(resp.read())
                return local_path
        except Exception:
            pass

        return self._generate_fallback_image(filename)

    def get_visual_for_text(self, text: str, fallback_query: str = "Universe") -> str:
        """Finds matching visual keyword from text or falls back to topic."""
        for word, keyword in TOPIC_VISUAL_MAP.items():
            if word in text:
                safe_name = f"{keyword}.jpg"
                local_cached = os.path.join(self.cache_dir, safe_name)
                if os.path.exists(local_cached):
                    return local_cached

                img_url = self.fetch_image_by_keyword(keyword)
                if img_url:
                    return self.download_image(img_url, safe_name)

        # Fallback query
        safe_fallback = f"{fallback_query}.jpg"
        local_cached = os.path.join(self.cache_dir, safe_fallback)
        if os.path.exists(local_cached):
            return local_cached

        img_url = self.fetch_image_by_keyword(fallback_query)
        if img_url:
            return self.download_image(img_url, safe_fallback)

        return self._generate_fallback_image(safe_fallback, fallback_query)

    def create_cinematic_clip_from_image(
        self,
        image_path: str,
        duration: float,
        output_clip_path: str
    ) -> str:
        """
        Converts a still photo into a dynamic 1080x1920 video clip with slow zoom motion.
        """
        # Slow zoom in Ken Burns style
        cmd = [
            "ffmpeg", "-y",
            "-loop", "1",
            "-i", image_path,
            "-vf", (
                "scale=1080:1920:force_original_aspect_ratio=increase,"
                "crop=1080:1920,"
                "zoompan=z='min(zoom+0.0012,1.18)':d=125:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920"
            ),
            "-t", f"{duration:.2f}",
            "-c:v", "libx264",
            "-preset", "ultrafast",
            "-pix_fmt", "yuv420p",
            "-r", "30",
            output_clip_path
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if res.returncode != 0:
            # Fallback simple crop if zoompan encounters extreme aspect ratio
            simple_cmd = [
                "ffmpeg", "-y",
                "-loop", "1",
                "-i", image_path,
                "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
                "-t", f"{duration:.2f}",
                "-c:v", "libx264",
                "-preset", "ultrafast",
                "-pix_fmt", "yuv420p",
                "-r", "30",
                output_clip_path
            ]
            subprocess.run(simple_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        return output_clip_path

    def build_multi_scene_background(
        self,
        sentences: List[Dict[str, Any]],
        output_bg_video: str
    ) -> str:
        """
        Builds a multi-scene background video where each sentence has its own matching image.
        """
        clip_paths: List[str] = []

        print(f"\n🎬 Assembling {len(sentences)} dynamic visual scenes...")
        for i, sent in enumerate(sentences):
            text = sent["text"]
            dur = max(2.0, sent["duration"])
            clip_file = os.path.join(self.cache_dir, f"scene_{i:02d}.mp4")

            # Determine image
            image_path = self.get_visual_for_text(text, fallback_query="Universe")
            print(f"  • Scene {i+1}: Visual '{os.path.basename(image_path)}' ({dur:.1f}s)")

            # Create video clip
            self.create_cinematic_clip_from_image(image_path, dur, clip_file)
            clip_paths.append(clip_file)

        # Concatenate all clips using FFmpeg concat demuxer
        concat_txt = os.path.join(self.cache_dir, "clips.txt")
        with open(concat_txt, "w", encoding="utf-8") as f:
            for cp in clip_paths:
                clean_p = os.path.abspath(cp).replace("\\", "/")
                f.write(f"file '{clean_p}'\n")

        cmd = [
            "ffmpeg", "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", concat_txt,
            "-c:v", "libx264",
            "-preset", "ultrafast",
            "-pix_fmt", "yuv420p",
            output_bg_video
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if res.returncode != 0:
            raise RuntimeError("Failed to concatenate scenes into background video.")

        print(f"✓ Multi-scene background ready: {output_bg_video}")
        return output_bg_video
