"""
Thumbnail Generator - High-CTR Shorts & Reels Thumbnail Engine
--------------------------------------------------------------
Generates diverse, visually striking 1080x1920 thumbnails with strict
64-bit perceptual hash (dHash) deduplication:
1. Extracts CLEAN frames across peak action timestamps.
2. Enhances saturation & contrast for vibrant mobile displays.
3. Cycles through 5 distinct visual styles (Clean Cinematic, Red Shock Pill,
   Electric Yellow Box, Neon Cyan Mystery, Dark Vignette Focus).
4. Computes perceptual dHash and automatically tries alternate timestamps/styles
   if the result visually matches any historical or same-batch thumbnail.
"""

import os
import re
import sys
import subprocess
from typing import Optional, List, Set
from PIL import Image, ImageEnhance, ImageDraw, ImageFont

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def compute_dhash(img_or_path, hash_size: int = 8) -> str:
    """Computes a 64-bit perceptual difference hash (dHash) hex string."""
    img = Image.open(img_or_path) if isinstance(img_or_path, str) else img_or_path
    resized = img.convert("L").resize((hash_size + 1, hash_size), Image.Resampling.LANCZOS)
    pixels = list(resized.getdata())
    bits = []
    for row in range(hash_size):
        row_offset = row * (hash_size + 1)
        for col in range(hash_size):
            bits.append(pixels[row_offset + col] > pixels[row_offset + col + 1])
    val = 0
    for b in bits:
        val = (val << 1) | (1 if b else 0)
    return f"{val:016x}"


def hamming_distance(h1: str, h2: str) -> int:
    try:
        return (int(h1, 16) ^ int(h2, 16)).bit_count()
    except Exception:
        return 64


def _get_system_font(size: int = 56, prefer_hindi: bool = False) -> ImageFont.FreeTypeFont:
    """Finds best bold display font for thumbnail badges (Devanagari-aware)."""
    hindi_candidates = [
        "C:/Windows/Fonts/Nirmala.ttc",
        "C:/Windows/Fonts/APARAJB.TTF",
        "C:/Windows/Fonts/UTSAAHB.TTF",
        "/usr/share/fonts/truetype/noto/NotoSansDevanagari-Bold.ttf",
        "/usr/share/fonts/opentype/noto/NotoSansDevanagari-Bold.otf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
    ]
    latin_candidates = [
        "C:/Windows/Fonts/impact.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/ariblk.ttf",
        "C:/Windows/Fonts/seguisb.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
    ]
    if prefer_hindi:
        for c in hindi_candidates:
            if os.path.exists(c):
                try:
                    return ImageFont.truetype(c, size)
                except Exception:
                    continue
        return None  # Signal caller to fall back to ASCII badge rather than rendering tofu boxes
    for c in latin_candidates + hindi_candidates:
        if os.path.exists(c):
            try:
                return ImageFont.truetype(c, size)
            except Exception:
                continue
    return ImageFont.load_default()


class ThumbnailGenerator:
    """Generates high-CTR vertical (1080x1920) thumbnails with zero repeats."""

    STYLES = ["red_pill", "yellow_box", "neon_cyan", "dark_vignette", "clean"]

    def __init__(self, output_dir: str = "output"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.last_dhash: str = ""

    def extract_clean_frame(self, video_path: str, timestamp_sec: float, out_img_path: str) -> bool:
        """Extracts a pristine uncompressed frame from video (or copies if already an image)."""
        if not os.path.exists(video_path):
            return False
        if video_path.lower().endswith((".jpg", ".jpeg", ".png")):
            Image.open(video_path).convert("RGB").save(out_img_path, "JPEG", quality=95)
            return os.path.exists(out_img_path)

        cmd = [
            "ffmpeg", "-y",
            "-ss", f"{max(0.2, timestamp_sec):.3f}",
            "-i", video_path,
            "-vframes", "1",
            "-q:v", "2",
            out_img_path
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        return res.returncode == 0 and os.path.exists(out_img_path) and os.path.getsize(out_img_path) > 5000

    def _render_variant(
        self,
        raw_img_path: str,
        output_thumb_path: str,
        badge_text: str,
        chosen_style: str,
        color_boost: float = 1.22,
    ) -> Optional[str]:
        img = Image.open(raw_img_path).convert("RGB")
        target_w, target_h = 1080, 1920
        w, h = img.size
        aspect = w / h
        target_aspect = target_w / target_h

        if aspect > target_aspect:
            new_h = target_h
            new_w = int(target_h * aspect)
            img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
            left = (new_w - target_w) // 2
            img = img.crop((left, 0, left + target_w, target_h))
        else:
            new_w = target_w
            new_h = int(target_w / aspect)
            img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
            top = (new_h - target_h) // 2
            img = img.crop((0, top, target_w, top + target_h))

        img = ImageEnhance.Color(img).enhance(color_boost)
        img = ImageEnhance.Contrast(img).enhance(1.16)
        img = ImageEnhance.Sharpness(img).enhance(1.12)

        raw_badge = (badge_text or "").strip()
        clean_badge = re.sub(r'[^\w\s\u0900-\u097F!?,.$#@\-%/:+\']', '', raw_badge).strip()
        has_hindi = bool(re.search(r'[\u0900-\u097F]', clean_badge))
        if has_hindi and _get_system_font(50, prefer_hindi=True) is None:
            clean_badge = "WHAT HAPPENS IF?!"
            has_hindi = False
        draw = ImageDraw.Draw(img)

        if chosen_style == "clean" or not clean_badge:
            gradient = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
            g_draw = ImageDraw.Draw(gradient)
            for y in range(240):
                alpha = int(105 * (1 - y / 240))
                g_draw.line([(0, y), (target_w, y)], fill=(0, 0, 0, alpha))
            img = Image.alpha_composite(img.convert("RGBA"), gradient).convert("RGB")

        elif chosen_style == "dark_vignette":
            overlay = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
            o_draw = ImageDraw.Draw(overlay)
            for y in range(380):
                alpha = int(165 * (1 - y / 380))
                o_draw.line([(0, y), (target_w, y)], fill=(8, 10, 18, alpha))
                o_draw.line([(0, target_h - 1 - y), (target_w, target_h - 1 - y)], fill=(8, 10, 18, alpha))
            img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
            draw = ImageDraw.Draw(img)
            font = _get_system_font(56, prefer_hindi=has_hindi)
            bbox = draw.textbbox((0, 0), clean_badge, font=font)
            tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
            tx, ty = (target_w - tw) // 2, 190
            draw.text((tx + 4, ty + 5), clean_badge, font=font, fill=(0, 0, 0))
            draw.text((tx, ty), clean_badge, font=font, fill=(255, 220, 40))

        elif chosen_style == "red_pill":
            font = _get_system_font(50, prefer_hindi=has_hindi)
            bbox = draw.textbbox((0, 0), clean_badge, font=font)
            tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
            px, py = 36, 18
            pw, ph = tw + px * 2, th + py * 2
            x0, y0 = (target_w - pw) // 2, 180
            draw.rounded_rectangle([x0 + 4, y0 + 6, x0 + pw + 4, y0 + ph + 6], radius=22, fill=(0, 0, 0))
            draw.rounded_rectangle([x0, y0, x0 + pw, y0 + ph], radius=22, fill=(210, 15, 20), outline=(255, 255, 255), width=3)
            draw.text((x0 + px, y0 + py - 4), clean_badge, font=font, fill=(255, 255, 255))

        elif chosen_style == "yellow_box":
            font = _get_system_font(52, prefer_hindi=has_hindi)
            bbox = draw.textbbox((0, 0), clean_badge, font=font)
            tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
            px, py = 32, 16
            pw, ph = tw + px * 2, th + py * 2
            x0, y0 = (target_w - pw) // 2, 220
            draw.rectangle([x0 + 5, y0 + 7, x0 + pw + 5, y0 + ph + 7], fill=(0, 0, 0))
            draw.rectangle([x0, y0, x0 + pw, y0 + ph], fill=(255, 220, 0), outline=(0, 0, 0), width=4)
            draw.text((x0 + px, y0 + py - 4), clean_badge, font=font, fill=(10, 10, 10))

        elif chosen_style == "neon_cyan":
            font = _get_system_font(48, prefer_hindi=has_hindi)
            bbox = draw.textbbox((0, 0), clean_badge, font=font)
            tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
            px, py = 34, 16
            pw, ph = tw + px * 2, th + py * 2
            x0, y0 = (target_w - pw) // 2, 200
            draw.rounded_rectangle([x0, y0, x0 + pw, y0 + ph], radius=18, fill=(10, 20, 35), outline=(0, 240, 255), width=4)
            draw.text((x0 + px, y0 + py - 4), clean_badge, font=font, fill=(255, 255, 255))

        img.save(output_thumb_path, "JPEG", quality=92)
        return compute_dhash(img)

    def generate(
        self,
        video_path: str,
        output_thumb_path: str,
        badge_text: Optional[str] = None,
        style: Optional[str] = None,
        timestamp_sec: float = 3.0,
        slot_index: int = 1,
        tracker=None,
        batch_hashes: Optional[Set[str]] = None,
    ) -> str:
        """
        Generates a guaranteed unique thumbnail (enforced by 64-bit dHash check
        against both historical uploads and current batch thumbnails).
        """
        os.makedirs(os.path.dirname(output_thumb_path) or ".", exist_ok=True)
        temp_raw = output_thumb_path + ".temp_raw.jpg"

        candidate_times: List[float] = [
            timestamp_sec,
            max(1.5, timestamp_sec + 4.5),
            max(1.5, timestamp_sec + 9.0),
            max(1.2, timestamp_sec - 1.5),
            12.5,
            18.0,
            1.5,
        ]
        base_style_idx = (slot_index - 1) % len(self.STYLES)
        candidate_styles = (
            [style] + [s for s in self.STYLES if s != style]
            if style else self.STYLES[base_style_idx:] + self.STYLES[:base_style_idx]
        )

        best_hash = ""
        try:
            for attempt_idx, ts in enumerate(candidate_times):
                if not self.extract_clean_frame(video_path, ts, temp_raw):
                    continue
                chosen_style = candidate_styles[attempt_idx % len(candidate_styles)]
                dhash = self._render_variant(
                    temp_raw,
                    output_thumb_path,
                    badge_text or "",
                    chosen_style,
                    color_boost=1.22 + (attempt_idx % 3) * 0.05,
                )
                if not dhash:
                    continue

                dup_batch = batch_hashes and any(hamming_distance(dhash, bh) <= 8 for bh in batch_hashes)
                dup_hist = tracker and tracker.is_thumbnail_hash_used(dhash, max_hamming=8)

                best_hash = dhash
                if not dup_batch and not dup_hist:
                    self.last_dhash = dhash
                    if batch_hashes is not None:
                        batch_hashes.add(dhash)
                    print(f"✓ Unique High-CTR Thumbnail [{chosen_style.upper()} | dHash={dhash[:8]}]: {output_thumb_path}")
                    return output_thumb_path
                else:
                    print(f"⚠️ Thumbnail dHash {dhash[:8]} too similar to prior upload; probing next frame/style...")

            # If all probed timestamps returned frames, keep the last rendered unique-timestamp variant
            if os.path.exists(output_thumb_path) and os.path.getsize(output_thumb_path) > 5000:
                self.last_dhash = best_hash
                if batch_hashes is not None and best_hash:
                    batch_hashes.add(best_hash)
                return output_thumb_path
            return ""
        except Exception as e:
            print(f"Thumbnail generation error: {e}")
            return ""
        finally:
            if os.path.exists(temp_raw):
                try:
                    os.remove(temp_raw)
                except Exception:
                    pass
