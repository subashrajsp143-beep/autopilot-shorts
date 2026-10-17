"""
Red Hoodie Guy Presenter Engine
Animates a 3D Pixar-style Red Hoodie Guy host over dynamic themed background footage.
Features:
- Dynamic expression switching: Shocked/wonder hook (0-2.5s), active talking & idle gestures (2.5s-end)
- Clean chromakey green screen extraction with green despill
- Seamless multi-scene background footage cutting
- Top hook banner + Hormozi bold yellow subtitles
- Integrated voiceover & suspense music mixing
"""

import os
import sys
import subprocess
from typing import List, Optional

# Windows UTF-8 fix
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


class HoodiePresenterEngine:
    """Handles rendering shorts featuring the Red Hoodie Guy host character."""

    def __init__(self, assets_dir: str = "assets", output_dir: str = "output"):
        self.assets_dir = assets_dir
        self.output_dir = output_dir
        self.character_dir = os.path.join(assets_dir, "presenter_red_hoodie")
        self.music_dir = os.path.join(assets_dir, "music")

        self.img_idle = os.path.join(self.character_dir, "red_hoodie_idle.jpg")
        self.img_talking = os.path.join(self.character_dir, "red_hoodie_talking.jpg")
        self.img_shocked = os.path.join(self.character_dir, "red_hoodie_shocked.jpg")

    def _get_font_opt(self) -> str:
        """Finds suitable bold display font."""
        if os.path.exists("C:/Windows/Fonts/impact.ttf"):
            return "fontfile='C\\:/Windows/Fonts/impact.ttf':"
        elif os.path.exists("C:/Windows/Fonts/arialbd.ttf"):
            return "fontfile='C\\:/Windows/Fonts/arialbd.ttf':"
        elif os.path.exists("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
            return "fontfile='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf':"
        elif os.path.exists("/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"):
            return "fontfile='/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf':"
        return ""

    def build_animated_presenter_video(self, duration: float, output_path: str) -> str:
        """
        Creates an animated MP4 of the Red Hoodie Guy matching the duration:
        - 0.0 - 2.5s: Shocked face (hook)
        - 2.5s - end: Alternates talking and idle expressions with natural speech timing
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        concat_txt = os.path.join(self.output_dir, "hoodie_concat.txt")

        shocked_path = os.path.abspath(self.img_shocked).replace("\\", "/")
        talking_path = os.path.abspath(self.img_talking).replace("\\", "/")
        idle_path = os.path.abspath(self.img_idle).replace("\\", "/")

        lines = []
        # Hook: Shocked face
        hook_dur = min(2.5, duration)
        lines.append(f"file '{shocked_path}'")
        lines.append(f"duration {hook_dur:.2f}")

        # Body: Talking and idle rhythm
        cur = hook_dur
        is_talking = True
        while cur < duration:
            chunk = 0.38 if is_talking else 0.28
            img = talking_path if is_talking else idle_path
            lines.append(f"file '{img}'")
            lines.append(f"duration {chunk:.2f}")
            cur += chunk
            is_talking = not is_talking

        # Final idle frame to avoid trailing freeze
        lines.append(f"file '{idle_path}'")

        with open(concat_txt, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        cmd = [
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0", "-i", concat_txt,
            "-t", f"{duration:.2f}",
            "-pix_fmt", "yuv420p",
            "-r", "30",
            output_path
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if res.returncode != 0:
            err = res.stderr.decode("utf-8", errors="replace")[-300:] if res.stderr else "Unknown error"
            raise RuntimeError(f"Failed to generate animated presenter: {err}")

        return output_path

    def render_short_with_hoodie_presenter(
        self,
        audio_path: str,
        ass_path: str,
        bg_video_paths: List[str],
        output_filename: str,
        duration: float,
        banner_text: Optional[str] = None
    ) -> str:
        """
        Renders complete 1080x1920 Short:
        - Background: Real thematic moving video footage cut dynamically
        - Foreground: Red Hoodie Guy speaking with green screen removed
        - Top: Yellow Hook Banner
        - Center: Bold ASS Subtitles
        - Audio: Hindi Neural Voiceover + Suspense Background Music
        """
        output_path = os.path.join(self.output_dir, output_filename)
        os.makedirs(self.output_dir, exist_ok=True)

        # 1. Build presenter stream
        presenter_raw = os.path.join(self.output_dir, "temp_hoodie_presenter.mp4")
        self.build_animated_presenter_video(duration=duration, output_path=presenter_raw)

        # 2. Prepare background scenes
        valid_scenes = [p for p in bg_video_paths if p and os.path.exists(p)]
        if not valid_scenes:
            valid_scenes = ["assets/ai_video_clips/bg_space.mp4"]

        num_scenes = len(valid_scenes)
        scene_dur = duration / num_scenes

        cmd = ["ffmpeg", "-y"]
        filter_parts = []
        concat_inputs = []

        # Background inputs [0 to num_scenes-1]
        for idx, s_path in enumerate(valid_scenes):
            cmd += ["-stream_loop", "-1", "-i", s_path]
            filter_parts.append(
                f"[{idx}:v]trim=duration={scene_dur:.2f},scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setpts=PTS-STARTPTS[bg_{idx}]"
            )
            concat_inputs.append(f"[bg_{idx}]")

        # Concat background scenes
        concat_str = "".join(concat_inputs) + f"concat=n={num_scenes}:v=1:a=0[bg_full];"

        # Presenter input
        presenter_idx = num_scenes
        cmd += ["-i", presenter_raw]

        # Chromakey & overlay filter
        # Character is scaled to 1350px and positioned at bottom center
        presenter_filter = (
            f"[{presenter_idx}:v]chromakey=0x00b140:0.22:0.04,despill=type=green:mix=0.8,scale=1150:-1[fg_hoodie];"
            f"[bg_full][fg_hoodie]overlay=(W-w)/2:H-h+80[comp_base];"
        )

        # Banner & Subtitle filter
        escaped_ass = ass_path.replace("\\", "/").replace(":", "\\:")
        if banner_text:
            import re
            clean_banner = re.sub(r'[^\x00-\x7F]+', '', banner_text)
            clean_banner = clean_banner.replace(":", "\\:").replace("'", "").replace('"', "").strip()
            if clean_banner:
                font_opt = self._get_font_opt()
                final_v_filter = (
                    f"[comp_base]drawtext={font_opt}text='{clean_banner}':fontsize=52:fontcolor=yellow:box=1:boxcolor=black@0.85:boxborderw=18:x=(w-text_w)/2:y=280[v_banner];"
                    f"[v_banner]ass='{escaped_ass}'[vout]"
                )
            else:
                final_v_filter = f"[comp_base]ass='{escaped_ass}'[vout]"
        else:
            final_v_filter = f"[comp_base]ass='{escaped_ass}'[vout]"

        full_filter = ";".join(filter_parts) + ";" + concat_str + presenter_filter + final_v_filter

        # Audio inputs: Voiceover + Music
        voice_idx = presenter_idx + 1
        cmd += ["-i", audio_path]

        music_file = os.path.join(self.music_dir, "ambient_suspense.mp3")
        if os.path.exists(music_file):
            music_idx = voice_idx + 1
            cmd += ["-stream_loop", "-1", "-i", music_file]
            audio_filter = f"[{voice_idx}:a]volume=1.0[v];[{music_idx}:a]volume=0.10[m];[v][m]amix=inputs=2:duration=first[aout]"
            cmd += ["-filter_complex", f"{full_filter};{audio_filter}", "-map", "[vout]", "-map", "[aout]"]
        else:
            cmd += ["-filter_complex", full_filter, "-map", "[vout]", "-map", f"[{voice_idx}:a]"]

        cmd += [
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-crf", "22",
            "-pix_fmt", "yuv420p",
            "-r", "30",
            "-c:a", "aac",
            "-b:a", "192k",
            "-t", f"{duration:.2f}",
            output_path
        ]

        print(f"🎬 Rendering Red Hoodie Guy Short -> {output_path}...")
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if res.returncode != 0:
            err_msg = res.stderr.decode("utf-8", errors="replace")[-500:] if res.stderr else "Unknown error"
            print("FFmpeg error:", err_msg)
            raise RuntimeError(f"FFmpeg failed to render Red Hoodie Short: {err_msg[-200:]}")

        print(f"✓ Red Hoodie Guy Short rendered successfully: {output_path}")
        return output_path


if __name__ == "__main__":
    engine = HoodiePresenterEngine()
    print("HoodiePresenterEngine initialized.")
