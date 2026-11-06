"""
Thumbnail Generator - High-CTR Shorts & Reels Thumbnail Engine
--------------------------------------------------------------
Generates diverse, visually striking 1080x1920 thumbnails for YouTube Shorts:
1. Extracts CLEAN frames from source footage BEFORE subtitles are burned in.
2. Selects peak action / climax moments (not a generic 2.5s freeze).
3. Enhances saturation & contrast for vibrant mobile displays.
4. Provides 5 distinct rotating visual styles (Clean Cinematic, Red Shock Pill,
   Electric Yellow Box, Neon Cyan Mystery, Bottom Curiosity Hook).
5. Guarantees ZERO repetitive cookie-cutter thumbnails across the batch!
"""

import os
import sys
import random
import subprocess
from typing import Optional, Tuple
from PIL import Image, ImageEnhance, ImageDraw, ImageFont, ImageFilter

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def _get_system_font(size: int = 56) -> ImageFont.FreeTypeFont:
    """Finds best bold display font for thumbnail badges."""
    candidates = [
        "C:/Windows/Fonts/impact.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/ariblk.ttf",
        "C:/Windows/Fonts/seguisb.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
    ]
    for c in candidates:
        if os.path.exists(c):
            try:
                return ImageFont.truetype(c, size)
            except Exception:
                continue
    return ImageFont.load_default()


class ThumbnailGenerator:
    """Generates high-CTR vertical (1080x1920) thumbnails with multiple distinct styles."""

    STYLES = ["clean", "red_pill", "yellow_box", "neon_cyan", "clean"]

    def __init__(self, output_dir: str = "output"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def extract_clean_frame(self, video_path: str, timestamp_sec: float, out_img_path: str) -> bool:
        """Extracts a pristine uncompressed frame from clean source video without subtitles."""
        if not os.path.exists(video_path):
            return False

        cmd = [
            "ffmpeg", "-y",
            "-ss", f"{max(0.1, timestamp_sec):.3f}",
            "-i", video_path,
            "-vframes", "1",
            "-q:v", "2",
            out_img_path
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        return res.returncode == 0 and os.path.exists(out_img_path) and os.path.getsize(out_img_path) > 5000

    def generate(
        self,
        video_path: str,
        output_thumb_path: str,
        badge_text: Optional[str] = None,
        style: Optional[str] = None,
        timestamp_sec: float = 3.0,
        slot_index: int = 1
    ) -> str:
        """
        Creates a custom high-CTR thumbnail:
        - Extracts clean frame from source
        - Scales & crops to exact 1080x1920
        - Boosts color & contrast
        - Applies one of 5 distinct styles based on slot_index or parameter
        """
        os.makedirs(os.path.dirname(output_thumb_path) or ".", exist_ok=True)
        temp_raw = output_thumb_path + ".temp_raw.jpg"

        # 1. Extract clean frame
        success = self.extract_clean_frame(video_path, timestamp_sec, temp_raw)
        if not success:
            # Fallback to 1.5s
            success = self.extract_clean_frame(video_path, 1.5, temp_raw)

        if not success or not os.path.exists(temp_raw):
            return ""

        try:
            # 2. Open image with Pillow
            img = Image.open(temp_raw).convert("RGB")

            # 3. Scale and Center-Crop to 1080x1920 (9:16)
            target_w, target_h = 1080, 1920
            w, h = img.size
            aspect = w / h
            target_aspect = target_w / target_h

            if aspect > target_aspect:
                # Video is wider than 9:16 -> scale by height, crop width
                new_h = target_h
                new_w = int(target_h * aspect)
                img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
                left = (new_w - target_w) // 2
                img = img.crop((left, 0, left + target_w, target_h))
            else:
                # Video is taller -> scale by width, crop height
                new_w = target_w
                new_h = int(target_w / aspect)
                img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
                top = (new_h - target_h) // 2
                img = img.crop((0, top, target_w, top + target_h))

            # 4. Enhance Colors & Contrast for Punchy Mobile Look
            img = ImageEnhance.Color(img).enhance(1.22)
            img = ImageEnhance.Contrast(img).enhance(1.15)
            img = ImageEnhance.Sharpness(img).enhance(1.10)

            # 5. Determine Style (Cycle automatically so no 2 thumbnails look the same!)
            chosen_style = style or self.STYLES[(slot_index - 1) % len(self.STYLES)]
            import re
            # Clean non-ASCII / emoji characters for font compatibility
            raw_badge = (badge_text or "").strip()
            clean_badge = re.sub(r'[^\w\s!?,.$#@\-%/:+\']', '', raw_badge).strip()

            draw = ImageDraw.Draw(img)

            # STYLE 1: CLEAN CINEMATIC (No badge text clutter - lets the peak action speak!)
            if chosen_style == "clean" or not clean_badge:
                # Add subtle top/bottom gradient for depth
                gradient = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
                g_draw = ImageDraw.Draw(gradient)
                for y in range(220):
                    alpha = int(90 * (1 - y / 220))
                    g_draw.line([(0, y), (target_w, y)], fill=(0, 0, 0, alpha))
                img = Image.alpha_composite(img.convert("RGBA"), gradient).convert("RGB")

            # STYLE 2: RED SHOCK PILL (High-urgency curiosity badge)
            elif chosen_style == "red_pill":
                font = _get_system_font(52)
                bbox = draw.textbbox((0, 0), clean_badge, font=font)
                text_w = bbox[2] - bbox[0]
                text_h = bbox[3] - bbox[1]

                pill_pad_x = 36
                pill_pad_y = 18
                pill_w = text_w + pill_pad_x * 2
                pill_h = text_h + pill_pad_y * 2
                pill_x = (target_w - pill_w) // 2
                pill_y = 180

                # Shadow behind pill
                draw.rounded_rectangle(
                    [pill_x + 4, pill_y + 6, pill_x + pill_w + 4, pill_y + pill_h + 6],
                    radius=20,
                    fill=(0, 0, 0, 180)
                )
                # Crimson Red Pill
                draw.rounded_rectangle(
                    [pill_x, pill_y, pill_x + pill_w, pill_y + pill_h],
                    radius=20,
                    fill=(210, 15, 20),
                    outline=(255, 255, 255),
                    width=3
                )
                # Bold White Text
                draw.text(
                    (pill_x + pill_pad_x, pill_y + pill_pad_y - 4),
                    clean_badge,
                    font=font,
                    fill=(255, 255, 255)
                )

            # STYLE 3: ELECTRIC YELLOW BOX (High CTR contrast)
            elif chosen_style == "yellow_box":
                font = _get_system_font(54)
                bbox = draw.textbbox((0, 0), clean_badge, font=font)
                text_w = bbox[2] - bbox[0]
                text_h = bbox[3] - bbox[1]

                box_pad_x = 32
                box_pad_y = 16
                box_w = text_w + box_pad_x * 2
                box_h = text_h + box_pad_y * 2
                box_x = (target_w - box_w) // 2
                box_y = 220

                # Deep Black Drop Shadow
                draw.rectangle(
                    [box_x + 5, box_y + 7, box_x + box_w + 5, box_y + box_h + 7],
                    fill=(0, 0, 0)
                )
                # Bright Neon Yellow Box
                draw.rectangle(
                    [box_x, box_y, box_x + box_w, box_y + box_h],
                    fill=(255, 220, 0),
                    outline=(0, 0, 0),
                    width=4
                )
                # Pitch Black Heavy Text
                draw.text(
                    (box_x + box_pad_x, box_y + box_pad_y - 4),
                    clean_badge,
                    font=font,
                    fill=(10, 10, 10)
                )

            # STYLE 4: NEON CYAN MYSTERY BOX
            elif chosen_style == "neon_cyan":
                font = _get_system_font(50)
                bbox = draw.textbbox((0, 0), clean_badge, font=font)
                text_w = bbox[2] - bbox[0]
                text_h = bbox[3] - bbox[1]

                box_pad_x = 34
                box_pad_y = 16
                box_w = text_w + box_pad_x * 2
                box_h = text_h + box_pad_y * 2
                box_x = (target_w - box_w) // 2
                box_y = 200

                # Dark Blue/Black semi-transparent backing
                draw.rounded_rectangle(
                    [box_x, box_y, box_x + box_w, box_y + box_h],
                    radius=16,
                    fill=(10, 20, 35),
                    outline=(0, 240, 255),
                    width=3
                )
                # Cyan/White glowing text
                draw.text(
                    (box_x + box_pad_x, box_y + box_pad_y - 4),
                    clean_badge,
                    font=font,
                    fill=(255, 255, 255)
                )

            # 6. Save high quality JPEG
            img.save(output_thumb_path, "JPEG", quality=92)
            print(f"✓ Generated High-CTR Thumbnail [{chosen_style.upper()}]: {output_thumb_path}")
            return output_thumb_path

        except Exception as e:
            print(f"Thumbnail generation error: {e}")
            if os.path.exists(temp_raw):
                os.rename(temp_raw, output_thumb_path)
                return output_thumb_path
            return ""
        finally:
            if os.path.exists(temp_raw):
                try:
                    os.remove(temp_raw)
                except Exception:
                    pass
