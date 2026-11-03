import os
import sys
import subprocess

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

sys.path.append(r"C:\Users\Subhash Kumar\.gemini\antigravity\scratch\autopilot_shorts")
sys.path.append(r"C:\Users\Subhash Kumar\.gemini\antigravity\scratch\autopilot_shorts\src")

from voice_generator import generate_audio

demo_dir = r"C:\Users\Subhash Kumar\.gemini\antigravity\scratch\autopilot_shorts\output\demo_hindi_ronaldo"
os.makedirs(demo_dir, exist_ok=True)

# 1. Hindi Commentary Script for Ronaldo's Bicycle Kick
hindi_commentary = "रोनाल्डो का यह बाइसिकल किक गोल देखकर विरोधी टीम के फैंस भी खड़े होकर तालियां बजाने लगे! जब हवा में करीब आठ फीट ऊपर उछलकर रोनाल्डो ने यह नामुमकिन गोल दागा, तो साइंस भी हैरान रह गई!"
banner_text = "RONALDO BICYCLE KICK! 🚲🐐"
video_clip = r"C:\Users\Subhash Kumar\.gemini\antigravity\scratch\autopilot_shorts\assets\creator_clips\football_01_ronaldo_bicycle.mp4"

audio_path = os.path.join(demo_dir, "ronaldo_hindi_voice.mp3")
ass_path = os.path.join(demo_dir, "ronaldo_hindi_sub.ass")
output_video = os.path.join(demo_dir, "Ronaldo_Hindi_Voice_Short.mp4")

print("1. Synthesizing Hindi Commentary with hi-IN-MadhurNeural...")
voice_res = generate_audio(
    text=hindi_commentary,
    audio_path=audio_path,
    ass_path=ass_path,
    voice="hi-IN-MadhurNeural"
)
duration = voice_res["duration"]
print(f"✓ Hindi voice generated: {duration:.2f}s")

# 2. FFmpeg: Combine Video + Lower Original Stadium Audio + Add Hindi Voice + Add Banner + Add Synced Subtitles
print("2. Assembling video with FFmpeg...")
escaped_ass = ass_path.replace("\\", "/").replace(":", r"\:")

font_opt = "fontfile='C\\:/Windows/Fonts/impact.ttf':" if os.path.exists("C:/Windows/Fonts/impact.ttf") else ""
banner_filter = f"drawtext={font_opt}text='{banner_text}':fontsize=54:fontcolor=yellow:box=1:boxcolor=black@0.85:boxborderw=20:x=(w-text_w)/2:y=280,"

filter_complex = (
    f"[0:v]trim=duration={duration:.2f},scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,{banner_filter}subtitles='{escaped_ass}'[vout];"
    f"[0:a]volume=0.15[bg_audio];"
    f"[1:a]volume=1.0[voice_audio];"
    f"[voice_audio][bg_audio]amix=inputs=2:duration=first[aout]"
)

cmd = [
    "ffmpeg", "-y",
    "-stream_loop", "-1", "-i", video_clip,
    "-i", audio_path,
    "-filter_complex", filter_complex,
    "-map", "[vout]",
    "-map", "[aout]",
    "-c:v", "libx264",
    "-preset", "veryfast",
    "-crf", "22",
    "-pix_fmt", "yuv420p",
    "-r", "30",
    "-c:a", "aac",
    "-b:a", "192k",
    "-t", f"{duration:.2f}",
    output_video
]

res = subprocess.run(cmd, capture_output=True, text=True)
if res.returncode != 0:
    print("Error:", res.stderr[-800:])
else:
    print("✓ Successfully rendered Ronaldo Hindi Voice Short:", output_video)

    # Copy to Desktop for immediate user listening
    desktop = os.path.join(os.environ.get("USERPROFILE", ""), "Desktop")
    if os.path.exists(desktop):
        import shutil
        desktop_dest = os.path.join(desktop, "Ronaldo_Hindi_Voice_Demo.mp4")
        shutil.copy2(output_video, desktop_dest)
        print("✓ Copied to Desktop:", desktop_dest)

    # Extract 2 preview frames to brain artifact dir
    artifact_dir = r"C:\Users\Subhash Kumar\.gemini\antigravity\brain\280b60c6-1590-475d-8014-8df89c2cea7c"
    f1 = os.path.join(artifact_dir, "ronaldo_hindi_frame_1.jpg")
    f2 = os.path.join(artifact_dir, "ronaldo_hindi_frame_2.jpg")
    subprocess.run(["ffmpeg", "-y", "-ss", "00:00:02", "-i", output_video, "-vframes", "1", "-q:v", "2", f1], capture_output=True)
    subprocess.run(["ffmpeg", "-y", "-ss", "00:00:06", "-i", output_video, "-vframes", "1", "-q:v", "2", f2], capture_output=True)
    print("✓ Preview frames saved to brain artifacts.")
