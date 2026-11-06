import os
import re

print("Patching mrbeast_hindi_engine.py...")
with open("src/mrbeast_hindi_engine.py", "r", encoding="utf-8") as f:
    text = f.read()

target = """        # 4. Generate high-impact thumbnail at 2.5s
        thumb_path = output_thumb_path or os.path.splitext(output_video_path)[0] + "_thumb.jpg"
        thumb_cmd = [
            "ffmpeg", "-y",
            "-ss", "00:00:02.500",
            "-i", output_video_path,
            "-vframes", "1",
            "-q:v", "2",
            thumb_path
        ]
        subprocess.run(thumb_cmd, capture_output=True, text=True)"""

replacement = """        # 4. Generate high-impact thumbnail using ThumbnailGenerator
        thumb_path = output_thumb_path or os.path.splitext(output_video_path)[0] + "_thumb.jpg"
        try:
            tg = ThumbnailGenerator(output_dir=os.path.dirname(thumb_path))
            thumb_source = downloaded_raw if (downloaded_raw and os.path.exists(downloaded_raw)) else output_video_path
            best_time = item.get("thumb_time", 2.8)
            tg.generate(
                video_path=thumb_source,
                output_thumb_path=thumb_path,
                badge_text=item.get("banner", "MRBEAST HINDI"),
                timestamp_sec=best_time,
                slot_index=item.get("slot", 1)
            )
        except Exception as e:
            print(f"Notice: MrBeast thumbnail generator fallback: {e}")
            thumb_cmd = [
                "ffmpeg", "-y",
                "-ss", "00:00:02.500",
                "-i", output_video_path,
                "-vframes", "1",
                "-q:v", "2",
                thumb_path
            ]
            subprocess.run(thumb_cmd, capture_output=True, text=True)"""

text_norm = text.replace('\r\n', '\n')
target_norm = target.replace('\r\n', '\n')
replacement_norm = replacement.replace('\r\n', '\n')

if target_norm in text_norm:
    text_norm = text_norm.replace(target_norm, replacement_norm, 1)
    with open("src/mrbeast_hindi_engine.py", "w", encoding="utf-8", newline="\n") as f:
        f.write(text_norm)
    print("✓ Successfully patched src/mrbeast_hindi_engine.py!")
else:
    print("Warning: target not found in src/mrbeast_hindi_engine.py")
