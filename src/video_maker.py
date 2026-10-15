"""
Video Maker Engine
Assembles vertical 9:16 (1080x1920) videos using FFmpeg.
Features:
- Auto-scales & crops any input footage to 9:16 vertical
- Burns styled animated ASS subtitles
- Adds quiet background music if available
- Generates procedural animated ambient backgrounds if no footage is provided
"""

import os
import random
import subprocess
import glob
from typing import Optional, Dict, Any


class VideoMaker:
    """Assembles final YouTube Shorts / Reels video."""

    def __init__(self, assets_dir: str = "assets", output_dir: str = "output"):
        self.assets_dir = assets_dir
        self.backgrounds_dir = os.path.join(assets_dir, "backgrounds")
        self.music_dir = os.path.join(assets_dir, "music")
        self.output_dir = output_dir

        os.makedirs(self.backgrounds_dir, exist_ok=True)
        os.makedirs(self.music_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)

    def _get_random_background_video(self) -> Optional[str]:
        """Finds an MP4 file in backgrounds directory."""
        candidates = glob.glob(os.path.join(self.backgrounds_dir, "*.mp4")) + \
                     glob.glob(os.path.join(self.backgrounds_dir, "*.mov"))
        if candidates:
            return random.choice(candidates)
        return None

    def _get_random_music(self) -> Optional[str]:
        """Finds an ambient MP3 file in music directory."""
        candidates = glob.glob(os.path.join(self.music_dir, "*.mp3"))
        if candidates:
            return random.choice(candidates)
        return None

    def render_video(
        self,
        audio_path: str,
        ass_path: str,
        output_filename: str,
        duration: float,
        bg_video_path: Optional[str] = None,
        bg_video_paths: Optional[List[str]] = None
    ) -> str:
        """
        Renders a full 1080x1920 vertical video with burned subtitles and audio.
        Supports both single background video and multi-scene dynamic video montages.
        """
        output_path = os.path.join(self.output_dir, output_filename)
        bg_music = self._get_random_music()

        # Format subtitle path for FFmpeg filter (escape colons and backslashes for Windows)
        escaped_ass = ass_path.replace("\\", "/").replace(":", "\\:")

        valid_scenes = [p for p in (bg_video_paths or []) if p and os.path.exists(p)]

        # MULTI-SCENE DYNAMIC MONTAGE
        if valid_scenes and len(valid_scenes) > 1:
            num_clips = len(valid_scenes)
            clip_dur = duration / num_clips
            cmd = ["ffmpeg", "-y"]
            filter_parts = []
            concat_inputs = []

            for idx, vp in enumerate(valid_scenes):
                cmd += ["-stream_loop", "-1", "-i", vp]
                filter_parts.append(
                    f"[{idx}:v]trim=duration={clip_dur:.2f},scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setpts=PTS-STARTPTS[v{idx}]"
                )
                concat_inputs.append(f"[v{idx}]")

            concat_filter = "".join(concat_inputs) + f"concat=n={num_clips}:v=1:a=0[vcat];[vcat]ass={escaped_ass}[vout]"
            full_video_filter = ";".join(filter_parts) + ";" + concat_filter

            cmd += ["-i", audio_path]
            audio_idx = num_clips

            if bg_music:
                cmd += ["-stream_loop", "-1", "-i", bg_music]
                music_idx = audio_idx + 1
                audio_filter = f"[{audio_idx}:a]volume=1.0[v];[{music_idx}:a]volume=0.12[m];[v][m]amix=inputs=2:duration=first[aout]"
                cmd += ["-filter_complex", f"{full_video_filter};{audio_filter}", "-map", "[vout]", "-map", "[aout]"]
            else:
                cmd += ["-filter_complex", full_video_filter, "-map", "[vout]", "-map", f"{audio_idx}:a"]

        # SINGLE VIDEO BACKGROUND
        else:
            cmd = ["ffmpeg", "-y"]
            bg_video = bg_video_path or (valid_scenes[0] if valid_scenes else None) or self._get_random_background_video()

            if bg_video and os.path.exists(bg_video):
                cmd += ["-stream_loop", "-1", "-i", bg_video]
                video_filter = f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,ass={escaped_ass}"
            else:
                cmd += [
                    "-f", "lavfi",
                    "-i", f"color=c=0x0a0f1d:s=1080x1920:d={duration + 1.0}"
                ]
                video_filter = f"ass={escaped_ass}"

            cmd += ["-i", audio_path]

            if bg_music:
                cmd += ["-stream_loop", "-1", "-i", bg_music]
                audio_filter = "[1:a]volume=1.0[v];[2:a]volume=0.12[m];[v][m]amix=inputs=2:duration=first[aout]"
                cmd += ["-filter_complex", f"[0:v]{video_filter}[vout];{audio_filter}", "-map", "[vout]", "-map", "[aout]"]
            else:
                cmd += ["-vf", video_filter, "-map", "0:v", "-map", "1:a"]

        # Encoding settings: Fast H.264, 30 fps, vertical 9:16
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

        print(f"Rendering video with FFmpeg -> {output_path}...")
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            print("FFmpeg error output:\n", result.stderr[-1000:])
            raise RuntimeError(f"FFmpeg failed with exit code {result.returncode}")

        print(f"Video rendered successfully: {output_path}")
        return output_path


if __name__ == "__main__":
    maker = VideoMaker(assets_dir="../assets", output_dir="../output")
    # Test rendering using test files
    maker.render_video(
        audio_path="../output/test_voice.mp3",
        ass_path="../output/test_voice.ass",
        output_filename="test_rendered_short.mp4",
        duration=9.43
    )
