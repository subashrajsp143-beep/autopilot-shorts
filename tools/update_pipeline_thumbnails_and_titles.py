import os
import re

print("Updating channel_blueprints.py...")
with open("src/channel_blueprints.py", "r", encoding="utf-8") as f:
    bp_code = f.read().replace("\r\n", "\n")

# Replace Part {day_offset + 1} in Channel 1
old_c1 = """            if tracker.is_title_used(title):
                title = f"{title.split('#')[0].strip()} Part {day_offset + 1} #Shorts\""""

new_c1 = """            if tracker.is_title_used(title):
                VIRAL_HOOKS = [
                    "यह सच जानकर होश उड़ जाएंगे! 😱",
                    "99% लोग यह गलती करते हैं! ⚠️",
                    "दुनिया का सबसे रहस्यमयी सच! 🤯",
                    "क्या आप इसका असली सच जानते हैं? 🧐",
                    "कभी किसी ने यह नहीं सोचा था! ⚡",
                    "इतिहास का सबसे खौफनाक रहस्य! 💀",
                    "वैज्ञानिक भी हैरान रह गए! 🔬",
                    "1 सेकंड में होश उड़ाने वाला सच! 🧠"
                ]
                clean_core = re.sub(r'\\s*Part\\s*\\d+', '', title.split('#')[0]).strip()
                hook = VIRAL_HOOKS[day_offset % len(VIRAL_HOOKS)]
                title = f"{clean_core} ⚠️ {hook} #Shorts"
                if len(title) > 95:
                    title = title[:92].rsplit(' ', 1)[0] + " #Shorts\""""

# Replace Part {day_offset + 1} in Channel 2
old_c2 = """            if tracker.is_title_used(title):
                candidate = dict(candidate)
                candidate["title"] = f"{title.split('#')[0].strip()} Part {day_offset + 1} #{title.split('#')[-1] if '#' in title else 'Shorts'}\""""

new_c2 = """            if tracker.is_title_used(title):
                candidate = dict(candidate)
                SCIENCE_HOOKS = [
                    "क्या आपने कभी ऐसा देखा है? 🤯",
                    "1 सेकंड में होश उड़ जाएंगे! 😱",
                    "गुरुत्वाकर्षण को किया पूरी तरह फेल! ⚡",
                    "दुनिया का सबसे संतोषजनक पल! ✨",
                    "यह नामुमकिन स्टंट देखकर आंखें खुली रह जाएंगी! 🔥",
                    "100 टन का भयानक दबाव! 💥",
                    "इंटरनेट का सबसे क्रेजी एक्सपेरिमेंट! 🚀"
                ]
                clean_core = re.sub(r'\\s*Part\\s*\\d+', '', title.split('#')[0]).strip()
                hook = SCIENCE_HOOKS[day_offset % len(SCIENCE_HOOKS)]
                candidate["title"] = f"{clean_core} | {hook} #Shorts"
                if len(candidate["title"]) > 95:
                    candidate["title"] = candidate["title"][:92].rsplit(' ', 1)[0] + " #Shorts\""""

assert old_c1 in bp_code, "old_c1 not found in channel_blueprints.py"
assert old_c2 in bp_code, "old_c2 not found in channel_blueprints.py"

bp_code = bp_code.replace(old_c1, new_c1).replace(old_c2, new_c2)

with open("src/channel_blueprints.py", "w", encoding="utf-8", newline="\n") as f:
    f.write(bp_code)

print("channel_blueprints.py successfully updated!")

print("Updating channel_generator.py...")
with open("src/channel_generator.py", "r", encoding="utf-8") as f:
    cg_code = f.read().replace("\r\n", "\n")

# Import ThumbnailGenerator in channel_generator.py
if "from src.thumbnail_generator import ThumbnailGenerator" not in cg_code:
    cg_code = "from src.thumbnail_generator import ThumbnailGenerator\n" + cg_code

# Update Channel 3 render_action_clip_hindi call to pass thumb_time and slot
old_ch3_render = """                render_res = render_action_clip_hindi(
                    clip_path=bp["clip"],
                    hindi_text=bp.get("hindi_script", ""),
                    banner_text=bp["banner"],
                    output_video_path=out_vid,
                    output_thumb_path=out_thumb,
                    use_ai_voice=False  # Authentic crowd / stream audio! Zero AI voice
                )"""

new_ch3_render = """                render_res = render_action_clip_hindi(
                    clip_path=bp["clip"],
                    hindi_text=bp.get("hindi_script", ""),
                    banner_text=bp["banner"],
                    output_video_path=out_vid,
                    output_thumb_path=out_thumb,
                    use_ai_voice=False,  # Authentic crowd / stream audio! Zero AI voice
                    thumb_time=bp.get("thumb_time", 3.2),
                    slot_index=slot
                )"""

# Update Channel 1 thumbnail generation (use ThumbnailGenerator on clean B-roll, NOT on burned video!)
old_ch1_thumb = """                subprocess.run([
                    "ffmpeg", "-y", "-ss", "00:00:02.500", "-i", out_vid,
                    "-vframes", "1", "-q:v", "2", out_thumb
                ], capture_output=True)"""

new_ch1_thumb = """                # High-CTR Thumbnail from pristine B-roll (Zero subtitle clutter!)
                try:
                    tg = ThumbnailGenerator(output_dir=channel_dir)
                    clean_bg = bp["scenes"][0] if (bp.get("scenes") and os.path.exists(bp["scenes"][0])) else out_vid
                    tg.generate(
                        video_path=clean_bg,
                        output_thumb_path=out_thumb,
                        badge_text=bp["banner"],
                        timestamp_sec=bp.get("thumb_time", 2.0),
                        slot_index=slot
                    )
                except Exception as tg_err:
                    print(f"Notice: Ch1 thumbnail fallback: {tg_err}")
                    subprocess.run([
                        "ffmpeg", "-y", "-ss", "00:00:02.500", "-i", out_vid,
                        "-vframes", "1", "-q:v", "2", out_thumb
                    ], capture_output=True)"""

# Update Channel 2 render_action_clip_hindi call to pass thumb_time and slot
old_ch2_render = """                render_res = render_action_clip_hindi(
                    clip_path=bp["clip"],
                    hindi_text=bp["hindi_script"],
                    banner_text=bp["banner"],
                    output_video_path=out_vid,
                    output_thumb_path=out_thumb,
                    use_ai_voice=False  # Authentic crunch / stunt sounds! Zero robotic AI voice
                )"""

new_ch2_render = """                render_res = render_action_clip_hindi(
                    clip_path=bp["clip"],
                    hindi_text=bp["hindi_script"],
                    banner_text=bp["banner"],
                    output_video_path=out_vid,
                    output_thumb_path=out_thumb,
                    use_ai_voice=False,  # Authentic crunch / stunt sounds! Zero robotic AI voice
                    thumb_time=bp.get("thumb_time", 4.0),
                    slot_index=slot
                )"""

assert old_ch3_render in cg_code, "old_ch3_render not found in channel_generator.py"
assert old_ch1_thumb in cg_code, "old_ch1_thumb not found in channel_generator.py"
assert old_ch2_render in cg_code, "old_ch2_render not found in channel_generator.py"

cg_code = cg_code.replace(old_ch3_render, new_ch3_render)
cg_code = cg_code.replace(old_ch1_thumb, new_ch1_thumb)
cg_code = cg_code.replace(old_ch2_render, new_ch2_render)

with open("src/channel_generator.py", "w", encoding="utf-8", newline="\n") as f:
    f.write(cg_code)

print("channel_generator.py successfully updated!")
