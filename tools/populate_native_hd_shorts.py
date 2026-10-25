"""
Download Native 1080x1920 Full-Screen HD Shorts
-----------------------------------------------
Downloads 100% REAL creator footage directly from official Shorts tabs:
- @MrBeast/shorts (Native 1080x1920 full-screen)
- @IShowSpeed/shorts (Native 1080x1920 full-screen)
- @GuinnessWorldRecords/shorts (Native 1080x1920 full-screen)
- @HydraulicPressChannel/shorts (Native 1080x1920 full-screen)
- Top Cristiano Ronaldo / Messi HD 1080p Full-Screen Shorts

Zero blurred bars. 100% Full-Screen 9:16 HD. High Thumbnail Quality.
"""

import os
import sys
import json
import glob
import subprocess

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Official verified Native Vertical 9:16 Shorts IDs
NATIVE_SHORTS_REGISTRY = [
    # --- MRBEAST (Official @MrBeast/shorts) ---
    {
        "id": "mrbeast_native_01",
        "niche": "mrbeast",
        "url": "https://www.youtube.com/shorts/aNI2jv7lBPQ",
        "filename": "mrbeast_01_giving_cash.mp4",
        "banner": "GIVING $10,000 TO A SUBSCRIBER! 💰",
        "title": "मिस्टर बीस्ट ने अनजान लड़के को दिए 10 लाख रुपये! 💰😱 #Shorts #MrBeast",
        "description": "MrBeast Giving $10,000 to a random subscriber! Watch his reaction! #Shorts #MrBeast #Viral #Trending",
        "tags": ["mrbeast", "mrbeast hindi", "giving money", "shorts", "viral"]
    },
    {
        "id": "mrbeast_native_02",
        "niche": "mrbeast",
        "url": "https://www.youtube.com/shorts/CEJXqm2eiJ0",
        "filename": "mrbeast_02_briefcase.mp4",
        "banner": "WHAT'S INSIDE THE SECRET BRIEFCASE? 💼",
        "title": "इस सीक्रेट ब्रीफकेस के अंदर क्या था? 😱💼 #Shorts #MrBeast",
        "description": "What is inside MrBeast's secret mystery briefcase? #Shorts #MrBeast #Mystery #Viral",
        "tags": ["mrbeast", "briefcase", "mystery", "shorts", "viral"]
    },
    {
        "id": "mrbeast_native_03",
        "niche": "mrbeast",
        "url": "https://www.youtube.com/shorts/mND4T0lzg_g",
        "filename": "mrbeast_03_subscribers.mp4",
        "banner": "TREATING PEOPLE BY SUBSCRIBERS! 🏆",
        "title": "सब्सक्राइबर्स के हिसाब से लोगों के साथ बर्ताव! 😱🔥 #Shorts #MrBeast",
        "description": "How people treat you based on your subscriber count! #Shorts #MrBeast #Viral",
        "tags": ["mrbeast", "subscribers", "experiment", "shorts", "viral"]
    },
    {
        "id": "mrbeast_native_04",
        "niche": "mrbeast",
        "url": "https://www.youtube.com/shorts/Y8IJi7iP5vk",
        "filename": "mrbeast_04_last_to_fall.mp4",
        "banner": "LAST TO FALL WINS $100,000! 🧗‍♂️",
        "title": "जो आखिरी तक नहीं गिरेगा उसे मिलेंगे 80 लाख! 💰😱 #Shorts #MrBeast",
        "description": "Last to fall wins massive cash challenge! #Shorts #MrBeast #Challenge #Viral",
        "tags": ["mrbeast", "challenge", "last to fall", "shorts", "viral"]
    },

    # --- ISHOWSPEED (Official @IShowSpeed/shorts) ---
    {
        "id": "speed_native_01",
        "niche": "ishowspeed",
        "url": "https://www.youtube.com/shorts/NDFE8W8wQ-Y",
        "filename": "speed_01_dude_perfect.mp4",
        "banner": "SPEED VS DUDE PERFECT GAUNTLET! ⚡💥",
        "title": "स्पीड vs डूड परफेक्ट का सबसे खतरनाक चैलेंज! 😱⚡ #Shorts #IShowSpeed",
        "description": "IShowSpeed vs Dude Perfect insane obstacle gauntlet! #Shorts #IShowSpeed #Viral",
        "tags": ["ishowspeed", "speed", "dude perfect", "shorts", "viral"]
    },
    {
        "id": "speed_native_02",
        "niche": "ishowspeed",
        "url": "https://www.youtube.com/shorts/iPjKK-KJ9iU",
        "filename": "speed_02_backflips.mp4",
        "banner": "BACKFLIPS BUT CEILING GETS LOWER! ⚠️🤸",
        "title": "बैकफ्लिप लेकिन छत हर बार नीचे आती गई! 😱🤸 #Shorts #IShowSpeed",
        "description": "IShowSpeed doing backflips as the ceiling gets lowered! #Shorts #IShowSpeed #Stunt",
        "tags": ["ishowspeed", "speed", "backflip", "shorts", "viral"]
    },
    {
        "id": "speed_native_03",
        "niche": "ishowspeed",
        "url": "https://www.youtube.com/shorts/WsxRjmuT5ZQ",
        "filename": "speed_03_silence_challenge.mp4",
        "banner": "SPEED 60 SECONDS SILENCE CHALLENGE! 🤫😭",
        "title": "स्पीड 60 सेकंड तक चुप रहने का चैलेंज! 😂🤫 #Shorts #IShowSpeed",
        "description": "IShowSpeed tries to stay silent for 60 seconds and fails hilariously! #Shorts #IShowSpeed #Funny",
        "tags": ["ishowspeed", "speed", "silence challenge", "shorts", "funny"]
    },
    {
        "id": "speed_native_04",
        "niche": "ishowspeed",
        "url": "https://www.youtube.com/shorts/CRUtic_pytc",
        "filename": "speed_04_iphone_duo.mp4",
        "banner": "SPEED GIVING AWAY BRAND NEW IPHONES! 📱🔥",
        "title": "स्पीड ने सड़क पर बांटे नए आईफोन! 📱😱 #Shorts #IShowSpeed",
        "description": "IShowSpeed giving away iPhones to subscribers! #Shorts #IShowSpeed #Giveaway",
        "tags": ["ishowspeed", "speed", "iphone giveaway", "shorts", "viral"]
    },

    # --- FOOTBALL (Cristiano Ronaldo / Champions League Native Shorts) ---
    {
        "id": "football_native_01",
        "niche": "football",
        "url": "https://www.youtube.com/shorts/p5Uf4k44E3w",
        "filename": "football_01_ronaldo_bicycle.mp4",
        "banner": "CR7 IMPOSSIBLE BICYCLE KICK IN 4K! 🚲🐐",
        "title": "रोनाल्डो का वो बाइसिकल किक गोल जो दुनिया कभी नहीं भूलेगी! 🐐🔥 #Shorts #Ronaldo",
        "description": "Cristiano Ronaldo iconic overhead bicycle kick goal against Juventus! #Shorts #CR7 #Ronaldo #Football",
        "tags": ["ronaldo", "cr7", "bicycle kick", "football", "shorts"]
    },
    {
        "id": "football_native_02",
        "niche": "football",
        "url": "https://www.youtube.com/shorts/KRqgjpiwrY8",
        "filename": "football_02_ronaldo_freekick.mp4",
        "banner": "CR7 GREATEST WORLD CUP FREE KICK! ⚽🎯",
        "title": "रोनाल्डो का वर्ल्ड कप में ऐतिहासिक फ्री किक गोल! 🎯🔥 #Shorts #Ronaldo #FIFA",
        "description": "Cristiano Ronaldo legendary 88th minute hat-trick free kick vs Spain! #Shorts #Ronaldo #WorldCup",
        "tags": ["ronaldo", "cr7", "free kick", "world cup", "football"]
    },
    {
        "id": "football_native_03",
        "niche": "football",
        "url": "https://www.youtube.com/shorts/T8vcb08cHnI",
        "filename": "football_03_ronaldo_juventus.mp4",
        "banner": "THE WHOLE STADIUM GAVE CR7 STANDING OVATION! 👏🐐",
        "title": "जब विरोधी टीम के पूरे स्टेडियम ने खड़े होकर तालियां बजाई! 👏🐐 #Shorts #CR7",
        "description": "Juventus fans giving Cristiano Ronaldo standing ovation for wonder goal! #Shorts #Ronaldo #Football",
        "tags": ["ronaldo", "cr7", "standing ovation", "football", "shorts"]
    },
    {
        "id": "football_native_04",
        "niche": "football",
        "url": "https://www.youtube.com/shorts/XpHeu--eQ8Q",
        "filename": "football_04_impossible_clearance.mp4",
        "banner": "GREATEST GOALLINE CLEARANCE IN HISTORY! 🧤⚡",
        "title": "फुटबॉल इतिहास का सबसे करिश्माई गोललाइन बचाव! 🧤😱 #Shorts #Football",
        "description": "Most impossible and miraculous football clearance ever captured! #Shorts #Football #Defense",
        "tags": ["football", "clearance", "defense", "goal", "shorts"]
    },

    # --- GUINNESS WORLD RECORDS (Official @GuinnessWorldRecords/shorts) ---
    {
        "id": "records_native_01",
        "niche": "world_records",
        "url": "https://www.youtube.com/shorts/uvmh92cHiyw",
        "filename": "records_01_table_tennis.mp4",
        "banner": "IMPOSSIBLE SPEED PING PONG RECORD! 🏓⚡",
        "title": "टेबल टेनिस बैट के हैंडल पर ऐसा पागलपन भरा वर्ल्ड रिकॉर्ड! 🏓😱 #Shorts #WorldRecord",
        "description": "Most bounces of table tennis ball on bat handle Guinness record! #Shorts #WorldRecord #Guinness",
        "tags": ["worldrecord", "guinness", "tabletennis", "shorts", "viral"]
    },
    {
        "id": "records_native_02",
        "niche": "world_records",
        "url": "https://www.youtube.com/shorts/OvOH9zCWInQ",
        "filename": "records_02_levitation_handstand.mp4",
        "banner": "LONGEST HANDSTAND ON LEVITATING PERSON! 🧘‍♂️✨",
        "title": "हवा में उड़ते इंसान पर हैंडस्टैंड का जादुई वर्ल्ड रिकॉर्ड! 😱🧘 #Shorts #WorldRecord",
        "description": "Longest handstand on person performing levitation trick! #Shorts #WorldRecord #Magic",
        "tags": ["worldrecord", "levitation", "handstand", "shorts", "magic"]
    },
    {
        "id": "records_native_03",
        "niche": "world_records",
        "url": "https://www.youtube.com/shorts/3rAr4NTRNXY",
        "filename": "records_03_juggling_sword.mp4",
        "banner": "JUGGLING SWORDS ON A SKATEBOARD! 🗡️🛹",
        "title": "स्केटबोर्ड चलाते हुए असली तलवारों से करतब! 😱🗡️ #Shorts #WorldRecord",
        "description": "Juggling sharp swords whilst skateboarding Guinness record! #Shorts #WorldRecord #Stunt",
        "tags": ["worldrecord", "stunt", "swords", "skateboard", "shorts"]
    },
    {
        "id": "records_native_04",
        "niche": "world_records",
        "url": "https://www.youtube.com/shorts/g0MVgnbsHN4",
        "filename": "records_04_human_catapult.mp4",
        "banner": "HUMAN CATAPULT RECORD LAUNCH! 🚀😱",
        "title": "इंसान को आसमान में लॉन्च करने का रोंगटे खड़े करने वाला रिकॉर्ड! 🚀😱 #Shorts #WorldRecord",
        "description": "Insane human catapult world record launch! #Shorts #WorldRecord #Guinness #Extreme",
        "tags": ["worldrecord", "extreme", "catapult", "shorts", "viral"]
    },

    # --- HYDRAULIC PRESS CHANNEL (Official @HydraulicPressChannel/shorts) ---
    {
        "id": "science_native_01",
        "niche": "mind_blowing",
        "url": "https://www.youtube.com/shorts/sNr1HXyUY8U",
        "filename": "science_01_helmet_press.mp4",
        "banner": "300 TON HYDRAULIC PRESS VS FIRE HELMET! 🔨🔥",
        "title": "300 टन के हाइड्रोलिक प्रेस के नीचे रखा फायर फाइटर हेलमेट! 🔨😱 #Shorts #Science",
        "description": "Old vintage firefighter helmet vs 300 ton hydraulic press crushing! #Shorts #HydraulicPress #Satisfying",
        "tags": ["hydraulicpress", "satisfying", "crushing", "science", "shorts"]
    },
    {
        "id": "science_native_02",
        "niche": "mind_blowing",
        "url": "https://www.youtube.com/shorts/_BaYx7c8QRw",
        "filename": "science_02_prettiest_crunch.mp4",
        "banner": "MOST SATISFYING CRUNCH EVER! 💎💥",
        "title": "इंटरनेट का सबसे सुकून देने वाला क्रंच वीडियो! 💎✨ #Shorts #Satisfying",
        "description": "The prettiest and most satisfying crunch destruction ever! #Shorts #OddlySatisfying #Crunchy",
        "tags": ["satisfying", "oddlysatisfying", "crunch", "hydraulicpress", "shorts"]
    },
    {
        "id": "science_native_03",
        "niche": "mind_blowing",
        "url": "https://www.youtube.com/shorts/khuzqEvvPyQ",
        "filename": "science_03_cards_press.mp4",
        "banner": "HYDRAULIC PRESS VS PLAYING CARDS! 🃏💥",
        "title": "जब हाइड्रोलिक प्रेस ने ताश की गड्डी को कुचल दिया! 🃏😱 #Shorts #Satisfying",
        "description": "Satisfying playing cards explosion under massive hydraulic press! #Shorts #Satisfying #HydraulicPress",
        "tags": ["hydraulicpress", "playingcards", "satisfying", "science", "shorts"]
    },
    {
        "id": "science_native_04",
        "niche": "mind_blowing",
        "url": "https://www.youtube.com/shorts/7Ebq6WlI490",
        "filename": "science_04_solar_panel.mp4",
        "banner": "SOLAR PANEL EXPLODING UNDER 100 TONS! ☀️💥",
        "title": "सोलर पैनल पर जब पड़ा 100 टन का दबाव! ☀️😱 #Shorts #Science",
        "description": "Solar panel glass destruction under heavy hydraulic press! #Shorts #HydraulicPress #Destruction",
        "tags": ["hydraulicpress", "destruction", "science", "shorts", "viral"]
    }
]


def download_and_format_native(entry, target_dir="assets/creator_clips"):
    os.makedirs(target_dir, exist_ok=True)
    out_path = os.path.join(target_dir, entry["filename"])

    tmp_out = out_path + ".tmp.mp4"
    cmd = [
        sys.executable, "-m", "yt_dlp",
        "-f", "bv*[height<=1080]+ba/b[height<=1080]/best",
        "-o", tmp_out,
        "--no-playlist",
        entry["url"]
    ]

    print(f"📥 Downloading native vertical Short: {entry['title'][:40]} ({entry['url']})...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"❌ Failed download {entry['id']}: {res.stderr[-200:]}")
        return False

    matches = glob.glob(out_path + ".tmp.*")
    if not matches:
        return False
    dl_file = matches[0]

    # Convert to pure 1080x1920 9:16 Full-Screen H.264 / AAC
    # - If already vertical: scale directly to 1080:1920
    # - If horizontal: center crop directly to 1080:1920 (ZERO BLURRED BARS)
    # - High quality CRF 20, 30fps
    ff_cmd = [
        "ffmpeg", "-y",
        "-i", dl_file,
        "-t", "45",
        "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "20",
        "-c:a", "aac",
        "-b:a", "192k",
        out_path
    ]
    res_ff = subprocess.run(ff_cmd, capture_output=True, text=True)
    try:
        os.remove(dl_file)
    except Exception:
        pass

    if res_ff.returncode == 0 and os.path.exists(out_path):
        size_mb = os.path.getsize(out_path) / (1024 * 1024)
        print(f"✓ Ready Full-Screen 9:16 HD: {out_path} ({size_mb:.2f} MB)")
        return True
    return False


def main():
    print("🚀 Downloading 20 Native Full-Screen 9:16 HD Shorts directly from Official Channels...")
    success_count = 0
    clean_index = []

    for i, entry in enumerate(NATIVE_SHORTS_REGISTRY, 1):
        print(f"\n[{i}/{len(NATIVE_SHORTS_REGISTRY)}] Processing: {entry['filename']}...")
        ok = download_and_format_native(entry)
        if ok:
            success_count += 1
            clean_index.append({
                "id": entry["id"],
                "niche": entry["niche"],
                "filename": entry["filename"],
                "banner": entry["banner"],
                "title": entry["title"],
                "description": entry["description"],
                "tags": entry["tags"]
            })

    # Save index
    index_file = "assets/creator_clips/clips_index.json"
    with open(index_file, "w", encoding="utf-8") as f:
        json.dump(clean_index, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 65)
    print(f"🎉 Successfully prepared {success_count} / {len(NATIVE_SHORTS_REGISTRY)} Full-Screen Native Shorts!")
    print(f"Index saved to: {index_file}")
    print("=" * 65)


if __name__ == "__main__":
    main()
