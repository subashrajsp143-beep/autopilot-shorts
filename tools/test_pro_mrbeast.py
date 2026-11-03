import os
import subprocess
import sys

sys.path.insert(0, ".")
from src.voice_generator import generate_audio

demo_dir = "output/test_pro_mrbeast"
os.makedirs(demo_dir, exist_ok=True)

video_clip = r"assets\creator_clips\mrbeast_01_giving_cash.mp4"
audio_path = os.path.join(demo_dir, "voice.mp3")
ass_path = os.path.join(demo_dir, "sub.ass")
output_video = os.path.join(demo_dir, "MrBeast_Pro_Hindi.mp4")

hindi_script = "मिस्टर बीस्ट ने इस अनजान लड़के को दस हजार डॉलर से भरा ब्रीफकेस थमा दिया! जैसे ही लड़के ने ब्रीफकेस खोला, उसकी आंखें फटी की फटी रह गईं!"

# 1. Synthesize Hindi Voice
voice_res = generate_audio(hindi_script, audio_path, ass_path, voice="hi-IN-MadhurNeural")
duration = voice_res["duration"]

# 2. Build modern ASS subtitle with clean English/Hinglish punch text in LOWER THIRD
# MarginV = 360 (Clean lower third, safely below the action, above phone navigation)
ass_content = f"""[Script Info]
Title: Viral Pro Subtitles
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: ProYellow,Impact,64,&H0000FFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,4,2,2,40,40,360,1
Style: ProWhite,Impact,64,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,4,2,2,40,40,360,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,0:00:02.50,ProYellow,,0,0,0,,MRBEAST GIVES $10,000 CASH!
Dialogue: 0,0:00:02.50,0:00:05.00,ProWhite,,0,0,0,,HE HANDED HIM THE BRIEFCASE!
Dialogue: 0,0:00:05.00,0:00:07.50,ProYellow,,0,0,0,,WHEN HE OPENED IT...
Dialogue: 0,0:00:07.50,0:00:10.50,ProWhite,,0,0,0,,HIS JAW DROPPED IN SHOCK!
"""

with open(ass_path, "w", encoding="utf-8") as f:
    f.write(ass_content)

escaped_ass = ass_path.replace("\\", "/").replace(":", "\\:")
font_opt = "fontfile='C\\:/Windows/Fonts/impact.ttf':" if os.path.exists("C:/Windows/Fonts/impact.ttf") else ""

# Top Hook Banner (Modern Red & White Pill)
top_text = "MRBEAST SECRET $10,000 BRIEFCASE!"
banner_filter = f"drawtext={font_opt}text='{top_text}':fontsize=48:fontcolor=white:box=1:boxcolor=0xDD0000@0.92:boxborderw=16:x=(w-text_w)/2:y=180,"

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
    "-crf", "20",
    "-pix_fmt", "yuv420p",
    "-r", "30",
    "-c:a", "aac",
    "-b:a", "192k",
    "-t", f"{duration:.2f}",
    output_video
]

res = subprocess.run(cmd, capture_output=True, text=True)
if res.returncode == 0:
    print("SUCCESS: Rendered", output_video)
    artifact_dir = r"C:\Users\Subhash Kumar\.gemini\antigravity\brain\280b60c6-1590-475d-8014-8df89c2cea7c"
    out_frame = os.path.join(artifact_dir, "pro_mrbeast_frame.jpg")
    subprocess.run(["ffmpeg", "-y", "-ss", "00:00:03", "-i", output_video, "-vframes", "1", "-q:v", "2", out_frame], capture_output=True)
    print("Saved frame to", out_frame)
else:
    print("Error:", res.stderr[-500:])
