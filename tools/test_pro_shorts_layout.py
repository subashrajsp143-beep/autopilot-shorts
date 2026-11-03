import os
import subprocess

video_clip = r"assets\creator_clips\football_01_ronaldo_bicycle.mp4"
output_video = r"output\test_pro_ronaldo.mp4"
artifact_dir = r"C:\Users\Subhash Kumar\.gemini\antigravity\brain\280b60c6-1590-475d-8014-8df89c2cea7c"
os.makedirs("output", exist_ok=True)

# Test modern pro layout:
# 1. Background [bg]: scale to 1080x1920 (increase), crop 1080:1920, boxblur=25:5, darken
# 2. Foreground [fg]: scale to 1080:-1 (fits 1080 width, perfectly crisp HD, 0% cropped)
# 3. Overlay [fg] on [bg] in center (y=(H-h)/2)
# 4. Top Hook Banner: Clean rounded appearance
# 5. Bottom Caption: High energy punchy text in lower third (never covers players)

font_opt = "fontfile='C\\:/Windows/Fonts/impact.ttf':" if os.path.exists("C:/Windows/Fonts/impact.ttf") else ""

top_text = "RONALDO IMPOSSIBLE BICYCLE KICK!"
sub_text = "HE FLEW 8 FEET IN THE AIR!"

filter_complex = (
    # Background blurred layer
    "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5,eq=brightness=-0.15[bg];"
    # Crisp foreground layer
    "[0:v]scale=1080:-2[fg];"
    # Overlay in center
    "[bg][fg]overlay=0:(H-h)/2[base];"
    # Top banner (y=220)
    f"[base]drawtext={font_opt}text='{top_text}':fontsize=52:fontcolor=white:box=1:boxcolor=0xCC0000@0.9:boxborderw=18:x=(w-text_w)/2:y=220,"
    # Bottom punch subtitle in lower third (y=1420)
    f"drawtext={font_opt}text='{sub_text}':fontsize=62:fontcolor=yellow:bordercolor=black:borderw=5:shadowcolor=black@0.8:shadowx=3:shadowy=3:x=(w-text_w)/2:y=1420[vout]"
)

cmd = [
    "ffmpeg", "-y",
    "-ss", "00:00:01",
    "-i", video_clip,
    "-filter_complex", filter_complex,
    "-map", "[vout]",
    "-map", "0:a",
    "-c:v", "libx264",
    "-preset", "veryfast",
    "-crf", "20",
    "-pix_fmt", "yuv420p",
    "-t", "5.0",
    output_video
]

res = subprocess.run(cmd, capture_output=True, text=True)
if res.returncode == 0:
    print("✓ Successfully generated test_pro_ronaldo.mp4")
    out_frame = os.path.join(artifact_dir, "pro_ronaldo_frame.jpg")
    subprocess.run(["ffmpeg", "-y", "-ss", "00:00:02", "-i", output_video, "-vframes", "1", "-q:v", "2", out_frame], capture_output=True)
    print("✓ Saved pro_ronaldo_frame.jpg")
else:
    print("Error:", res.stderr[-500:])
