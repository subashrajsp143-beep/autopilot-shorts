import os
import sys
import subprocess

sys.path.append(r"C:\Users\Subhash Kumar\.gemini\antigravity\scratch\autopilot_shorts")
sys.path.append(r"C:\Users\Subhash Kumar\.gemini\antigravity\scratch\autopilot_shorts\src")

from voice_generator import generate_audio
from video_maker import VideoMaker

demo_output_dir = r"C:\Users\Subhash Kumar\.gemini\antigravity\scratch\autopilot_shorts\output\demo_test"
os.makedirs(demo_output_dir, exist_ok=True)

# 1. Script
script_text = "क्या आप जानते हैं? अगर कोई बात करते समय अपनी बाईं तरफ ऊपर देखे, तो साइकोलॉजी कहती है कि 90% चांस है कि वह झूठ बोलने की तैयारी कर रहा है! क्योंकि हमारा दिमाग झूठ बोलने के लिए अपनी इमेजिनेशन का इस्तेमाल करता है।"
top_banner = "DARK PSYCHOLOGY FACT 🧠⚡"

audio_path = os.path.join(demo_output_dir, "demo_hindi_audio.mp3")
ass_path = os.path.join(demo_output_dir, "demo_hindi_sub.ass")
output_video_path = os.path.join(demo_output_dir, "demo_hindi_short.mp4")

print("1. Generating Hindi Neural Voice (hi-IN-MadhurNeural)...")
voice_res = generate_audio(
    text=script_text,
    audio_path=audio_path,
    ass_path=ass_path,
    voice="hi-IN-MadhurNeural"
)
duration = voice_res["duration"]
print(f"✓ Audio generated: {duration:.2f}s")

# 2. Render Video with VideoMaker
print("2. Rendering 1080x1920 Cinematic Video with HD B-Roll...")
video_maker = VideoMaker(
    assets_dir=r"C:\Users\Subhash Kumar\.gemini\antigravity\scratch\autopilot_shorts\assets",
    output_dir=demo_output_dir
)

bg_scenes = [
    r"C:\Users\Subhash Kumar\.gemini\antigravity\scratch\autopilot_shorts\assets\ai_video_clips\bg_darkpsych.mp4",
    r"C:\Users\Subhash Kumar\.gemini\antigravity\scratch\autopilot_shorts\assets\ai_video_clips\bg_psychology.mp4",
    r"C:\Users\Subhash Kumar\.gemini\antigravity\scratch\autopilot_shorts\assets\ai_video_clips\bg_brain.mp4"
]

rendered_video = video_maker.render_video(
    audio_path=audio_path,
    ass_path=ass_path,
    output_filename="demo_hindi_short.mp4",
    duration=duration,
    bg_video_paths=bg_scenes,
    presenter_video_path=None,
    banner_text=top_banner
)

print(f"✓ Video rendered successfully: {rendered_video}")

# 3. Extract preview frames for inspection
artifact_dir = r"C:\Users\Subhash Kumar\.gemini\antigravity\brain\280b60c6-1590-475d-8014-8df89c2cea7c"
os.makedirs(artifact_dir, exist_ok=True)

frame1 = os.path.join(artifact_dir, "hindi_demo_frame_1.jpg")
frame2 = os.path.join(artifact_dir, "hindi_demo_frame_2.jpg")
frame3 = os.path.join(artifact_dir, "hindi_demo_frame_3.jpg")

subprocess.run(["ffmpeg", "-y", "-ss", "00:00:02", "-i", rendered_video, "-vframes", "1", "-q:v", "2", frame1], capture_output=True)
subprocess.run(["ffmpeg", "-y", "-ss", "00:00:06", "-i", rendered_video, "-vframes", "1", "-q:v", "2", frame2], capture_output=True)
subprocess.run(["ffmpeg", "-y", "-ss", "00:00:10", "-i", rendered_video, "-vframes", "1", "-q:v", "2", frame3], capture_output=True)

print("✓ Preview frames extracted to artifact dir:")
print(f"Frame 1: {frame1} (exists: {os.path.exists(frame1)})")
print(f"Frame 2: {frame2} (exists: {os.path.exists(frame2)})")
print(f"Frame 3: {frame3} (exists: {os.path.exists(frame3)})")
