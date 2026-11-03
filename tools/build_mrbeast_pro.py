import os
import sys
import subprocess
import shutil

video_input = "output/test_beast_hindi.mp4.webm"
output_video = "output/MrBeast_Real_Hindi_Dub.mp4"

font_opt = "fontfile='C\\:/Windows/Fonts/impact.ttf':" if os.path.exists("C:/Windows/Fonts/impact.ttf") else ""
top_text = "MRBEAST $10,000 CASH DROP IN HINDI!"

# Filter: scale to 1080:1920, add sleek top hook banner, keep original audio
banner_filter = f"drawtext={font_opt}text='{top_text}':fontsize=50:fontcolor=white:box=1:boxcolor=0xDD0000@0.95:boxborderw=16:x=(w-text_w)/2:y=160"

filter_complex = f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,{banner_filter}[vout]"

cmd = [
    "ffmpeg", "-y",
    "-i", video_input,
    "-filter_complex", filter_complex,
    "-map", "[vout]",
    "-map", "0:a:0",
    "-c:v", "libx264",
    "-preset", "veryfast",
    "-crf", "18",
    "-pix_fmt", "yuv420p",
    "-r", "30",
    "-c:a", "aac",
    "-b:a", "192k",
    output_video
]

print("Rendering MrBeast Real Hindi Dub Short...")
res = subprocess.run(cmd, capture_output=True, text=True)
if res.returncode == 0:
    print("SUCCESS: Rendered", output_video)
    artifact_dir = r"C:\Users\Subhash Kumar\.gemini\antigravity\brain\280b60c6-1590-475d-8014-8df89c2cea7c"
    out_frame = os.path.join(artifact_dir, "pro_mrbeast_real_hindi_frame.jpg")
    subprocess.run(["ffmpeg", "-y", "-ss", "00:00:03", "-i", output_video, "-vframes", "1", "-q:v", "2", out_frame], capture_output=True)
    print("Saved frame to", out_frame)
    
    # Copy to Desktop
    desktop_dir = r"C:\Users\Subhash Kumar\OneDrive\Desktop"
    if os.path.exists(desktop_dir):
        dest_desktop = os.path.join(desktop_dir, "MrBeast_Real_Hindi_Dub.mp4")
        shutil.copy2(output_video, dest_desktop)
        print("Copied to Desktop:", dest_desktop)
else:
    print("Error:", res.stderr[-500:])
