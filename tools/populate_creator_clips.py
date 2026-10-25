"""
Populate and Standardize Pre-Cached Creator Clips
------------------------------------------------
Creates 23 high-retention viral creator clips across 5 niches:
- mrbeast (5)
- ishowspeed (5)
- football (5)
- world_records (4)
- mind_blowing (4)

Compresses each clip to ~2-3.5 MB so they easily commit to git,
giving GitHub Actions runners instant, bulletproof local clips!
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

TARGET_CLIPS = [
    # --- MRBEAST ---
    {
        "id": "mrbeast_01",
        "niche": "mrbeast",
        "filename": "mrbeast_01_circle_survival.mp4",
        "existing_src": "assets/downloads/fresh_mrbeast_20261022_154928_zxYjTTXc-J8.mp4",
        "search_query": "MrBeast last to leave circle wins $500,000",
        "banner": "LAST TO LEAVE WINS $500,000! 💰",
        "title": "जो आखिरी में निकलेगा उसे मिलेंगे 5 करोड़! 💰😱 #Shorts #MrBeast #Viral",
        "description": "MrBeast Insane $500,000 Challenge! Watch till the end! #Shorts #MrBeast #Viral #Trending",
        "tags": ["mrbeast", "shorts", "viral", "challenge", "trending"]
    },
    {
        "id": "mrbeast_02",
        "niche": "mrbeast",
        "filename": "mrbeast_02_luxury_yacht.mp4",
        "existing_src": "assets/downloads/fresh_mrbeast_20261021_140215_48h57PspBec.mp4",
        "search_query": "MrBeast $1,000,000 luxury yacht challenge",
        "banner": "$1,000,000 LUXURY YACHT! 🛥️",
        "title": "10 करोड़ की लग्जरी यॉट का सबसे बड़ा चैलेंज! 🛥️🔥 #Shorts #MrBeast #Viral",
        "description": "MrBeast $1,000,000 Luxury Yacht challenge! #Shorts #MrBeast #Viral #Trending",
        "tags": ["mrbeast", "shorts", "viral", "luxury", "yacht"]
    },
    {
        "id": "mrbeast_03",
        "niche": "mrbeast",
        "filename": "mrbeast_03_extreme_challenge.mp4",
        "existing_src": "assets/downloads/fresh_mrbeast_20261017_130743_zajUgQLviwk.mp4",
        "search_query": "MrBeast crazy extreme challenge moments",
        "banner": "MRBEAST CRAZIEST EXPERIMENT! 💥",
        "title": "मिस्टर बीस्ट का सबसे खतरनाक एक्सपेरिमेंट! 😱🔥 #Shorts #MrBeast #Viral",
        "description": "MrBeast craziest experiment ever done! #Shorts #MrBeast #Viral #Trending",
        "tags": ["mrbeast", "shorts", "viral", "experiment", "trending"]
    },
    {
        "id": "mrbeast_04",
        "niche": "mrbeast",
        "filename": "mrbeast_04_squid_game.mp4",
        "existing_src": "assets/downloads/test_short.webm",
        "search_query": "MrBeast real life squid game viral moments",
        "banner": "REAL LIFE SQUID GAME $456,000! 🦑",
        "title": "असली जिंदगी का स्क्विड गेम $456,000! 🦑😱 #Shorts #MrBeast #Viral",
        "description": "MrBeast Real Life Squid Game with 456 players! #Shorts #MrBeast #Viral #SquidGame",
        "tags": ["mrbeast", "squidgame", "shorts", "viral", "trending"]
    },
    {
        "id": "mrbeast_05",
        "niche": "mrbeast",
        "filename": "mrbeast_05_bunker_survival.mp4",
        "existing_src": "assets/downloads/fresh_mrbeast_20261017_131928_cnArVXTOvc0.mp4",
        "search_query": "MrBeast 100 days underground bunker survival",
        "banner": "100 DAYS UNDERGROUND BUNKER! 🛡️",
        "title": "100 दिन तक जमीन के नीचे बंकर में जीवित रहा! 🛡️😱 #Shorts #MrBeast #Viral",
        "description": "Surviving 100 days underground in a bunker! #Shorts #MrBeast #Viral #Survival",
        "tags": ["mrbeast", "survival", "shorts", "viral", "trending"]
    },

    # --- ISHOWSPEED ---
    {
        "id": "speed_01",
        "niche": "ishowspeed",
        "filename": "speed_01_ronaldo_scream.mp4",
        "existing_src": "assets/creator_clips/speed_01_ronaldo_scream.mp4",
        "search_query": "IShowSpeed ronaldo scream celebration funny",
        "banner": "SPEED MEETS RONALDO REACTION! 🐐⚡",
        "title": "जब स्पीड आखिरकार रोनाल्डो से मिला! 😭🔥 #Shorts #IShowSpeed #Ronaldo",
        "description": "IShowSpeed meeting his idol Cristiano Ronaldo! #Shorts #IShowSpeed #Ronaldo #Viral",
        "tags": ["ishowspeed", "speed", "ronaldo", "shorts", "viral"]
    },
    {
        "id": "speed_02",
        "niche": "ishowspeed",
        "filename": "speed_02_fifa_rage.mp4",
        "existing_src": "assets/downloads/speed_test.mp4",
        "search_query": "IShowSpeed playing FIFA funny rage scream",
        "banner": "SPEED CRAZIEST RAGE MOMENT! 🎮💥",
        "title": "स्पीड का सबसे खतरनाक गेमिंग रेज देखकर दंग रह जाओगे! 😂🔥 #Shorts #IShowSpeed #Viral",
        "description": "IShowSpeed funniest rage moment during stream! #Shorts #IShowSpeed #Gaming #Funny",
        "tags": ["ishowspeed", "speed", "funny", "rage", "shorts"]
    },
    {
        "id": "speed_03",
        "niche": "ishowspeed",
        "filename": "speed_03_funny_screams.mp4",
        "existing_src": "assets/downloads/fresh_ishowspeed_20261017_131959_wtndQw9GXdQ.mp4",
        "search_query": "IShowSpeed funny screams and barking compilation",
        "banner": "SPEED'S FUNNIEST SCREAMS! 😭⚡",
        "title": "स्पीड की ऐसी चीखें देखकर हंसी नहीं रुकेगी! 😂💀 #Shorts #IShowSpeed #Funny",
        "description": "Funniest IShowSpeed screams compilation! #Shorts #IShowSpeed #Funny #Trending",
        "tags": ["ishowspeed", "speed", "funny", "comedy", "shorts"]
    },
    {
        "id": "speed_04",
        "niche": "ishowspeed",
        "filename": "speed_04_stream_crazy.mp4",
        "existing_src": None,
        "search_query": "IShowSpeed crazy stream moments funny shorts",
        "banner": "SPEED GOES COMPLETELY CRAZY! 😂🔥",
        "title": "लाइव स्ट्रीम पर स्पीड ने कर दिया यह पागलपन! 😱😂 #Shorts #IShowSpeed #Viral",
        "description": "Speed went crazy on live stream! #Shorts #IShowSpeed #Viral #Trending",
        "tags": ["ishowspeed", "stream", "funny", "shorts", "viral"]
    },
    {
        "id": "speed_05",
        "niche": "ishowspeed",
        "filename": "speed_05_bark_moment.mp4",
        "existing_src": "assets/downloads/fresh_ishowspeed_20261021_140321_SykgD0PGMAI.mp4",
        "search_query": "IShowSpeed iconic bark reaction funny shorts",
        "banner": "SPEED ICONIC BARKING MOMENT! 🐕⚡",
        "title": "स्पीड का सबसे आइकॉनिक रिएक्शन जो वायरल हो गया! 😂🔥 #Shorts #IShowSpeed",
        "description": "IShowSpeed iconic barking moment reaction! #Shorts #IShowSpeed #Comedy #Viral",
        "tags": ["ishowspeed", "bark", "comedy", "shorts", "viral"]
    },

    # --- FOOTBALL ---
    {
        "id": "football_01",
        "niche": "football",
        "filename": "football_01_ronaldo_header.mp4",
        "existing_src": "assets/downloads/fresh_football_20261017_132030_at_jeLqBTJk.mp4",
        "search_query": "Cristiano Ronaldo high jump header impossible goal",
        "banner": "CR7 FLIES IN THE AIR! ✈️🐐",
        "title": "जब रोनाल्डो ने हवा में उड़कर दागा करिश्माई गोल! 🐐🔥 #Shorts #Ronaldo #Football",
        "description": "Cristiano Ronaldo gravity defying high jump header goal! #Shorts #Ronaldo #CR7 #Football",
        "tags": ["ronaldo", "cr7", "football", "goal", "shorts"]
    },
    {
        "id": "football_02",
        "niche": "football",
        "filename": "football_02_neymar_skills.mp4",
        "existing_src": "assets/downloads/fresh_football_20261021_140355_OWOjRdmpM6I.mp4",
        "search_query": "Neymar Jr samba skills ankle breaker shorts",
        "banner": "NEYMAR UNSTOPPABLE SKILLS! 🇧🇷⚡",
        "title": "नेमार का ऐसा ब्राजीलियन जादू जो कोई नहीं रोक सकता! 🇧🇷🔥 #Shorts #Neymar #Football",
        "description": "Neymar Jr best samba dribbling skills in football! #Shorts #Neymar #Skills #Football",
        "tags": ["neymar", "football", "skills", "shorts", "viral"]
    },
    {
        "id": "football_03",
        "niche": "football",
        "filename": "football_03_messi_magic.mp4",
        "existing_src": None,
        "search_query": "Lionel Messi best dribbles commentary viral shorts",
        "banner": "MESSI ANKLE BREAKER MOMENTS! 👑🔥",
        "title": "मेसी का यह जादुई ड्रिबल देखकर डिफेंडर गिर पड़े! 👑⚽ #Shorts #Messi #Football",
        "description": "Lionel Messi impossible ankle breaking dribble! #Shorts #Messi #GOAT #Football",
        "tags": ["messi", "football", "goat", "dribble", "shorts"]
    },
    {
        "id": "football_04",
        "niche": "football",
        "filename": "football_04_impossible_saves.mp4",
        "existing_src": None,
        "search_query": "Impossible goalkeeper saves football shorts",
        "banner": "IMPOSSIBLE GOALKEEPER SAVES! 🧤🔥",
        "title": "गोलकीपर का ऐसा करिश्माई बचाव जो बिल्कुल नामुमकिन था! 🧤⚽ #Shorts #Football",
        "description": "Most incredible and impossible goalkeeper saves in football! #Shorts #Goalkeeper #Football",
        "tags": ["goalkeeper", "football", "saves", "shorts", "viral"]
    },
    {
        "id": "football_05",
        "niche": "football",
        "filename": "football_05_ronaldinho_magic.mp4",
        "existing_src": None,
        "search_query": "Ronaldinho magic skills and smile football shorts",
        "banner": "RONALDINHO PURE FOOTBALL MAGIC! 🎩✨",
        "title": "रोनाल्डिन्हो का वो जादू जो दोबारा कभी देखने को नहीं मिलेगा! 🎩⚽ #Shorts #Football",
        "description": "Ronaldinho magical football skills that shocked the world! #Shorts #Ronaldinho #Magic",
        "tags": ["ronaldinho", "football", "magic", "shorts", "viral"]
    },

    # --- WORLD RECORDS ---
    {
        "id": "records_01",
        "niche": "world_records",
        "filename": "records_01_domino_chain.mp4",
        "existing_src": "assets/downloads/fresh_world_records_20261021_140443_vbjko3M0JT4.mp4",
        "search_query": "World largest Domino chain reaction Guinness shorts",
        "banner": "LARGEST DOMINO CHAIN REACTION! 🧱💥",
        "title": "लाखों डोमिनोज़ का सबसे खूबसूरत वर्ल्ड रिकॉर्ड! 🧱✨ #Shorts #WorldRecord #Satisfying",
        "description": "World largest domino chain reaction record! #Shorts #WorldRecord #Domino #Trending",
        "tags": ["domino", "worldrecord", "satisfying", "shorts", "viral"]
    },
    {
        "id": "records_02",
        "niche": "world_records",
        "filename": "records_02_insane_stunts.mp4",
        "existing_src": "assets/downloads/fresh_world_records_20261017_132059_KSWYF3racCQ.mp4",
        "search_query": "Insane Guinness World Records compilation shorts",
        "banner": "INSANE GUINNESS WORLD RECORDS! 🏆😱",
        "title": "इंसान ने बनाया ऐसा वर्ल्ड रिकॉर्ड जो तोड़ना नामुमकिन है! 🏆🔥 #Shorts #WorldRecord",
        "description": "Unbelievable Guinness World Records ever recorded! #Shorts #WorldRecord #Guinness",
        "tags": ["guinness", "worldrecord", "stunt", "shorts", "viral"]
    },
    {
        "id": "records_03",
        "niche": "world_records",
        "filename": "records_03_parkour_stunts.mp4",
        "existing_src": None,
        "search_query": "Death defying parkour stunts compilation shorts",
        "banner": "DEATH-DEFYING PARKOUR STUNTS! 🏙️⚠️",
        "title": "50 मंजिला इमारत पर बिना रस्सी के ऐसा खतरनाक स्टंट! 😱🏙️ #Shorts #Parkour #Viral",
        "description": "Crazy parkour stunts that will make your heart skip a beat! #Shorts #Parkour #Stunt",
        "tags": ["parkour", "stunt", "extreme", "shorts", "viral"]
    },
    {
        "id": "records_04",
        "niche": "world_records",
        "filename": "records_04_speed_cube.mp4",
        "existing_src": None,
        "search_query": "Fastest Rubik cube solver world record shorts",
        "banner": "FASTEST HUMAN REACTION EVER! ⚡👀",
        "title": "दुनिया के सबसे तेज इंसान की सुपरह्यूमन स्पीड! ⚡😱 #Shorts #WorldRecord #Speed",
        "description": "Fastest human reaction and solving speed world record! #Shorts #WorldRecord #HumanSpeed",
        "tags": ["speed", "worldrecord", "human", "shorts", "viral"]
    },

    # --- MIND BLOWING / EXPERIMENTS ---
    {
        "id": "science_01",
        "niche": "mind_blowing",
        "filename": "science_01_hydraulic_diamond.mp4",
        "existing_src": "assets/downloads/fresh_mind_blowing_20261021_140545_CFmmCp3X7vA.mp4",
        "search_query": "Hydraulic press vs real diamond experiment shorts",
        "banner": "HYDRAULIC PRESS VS DIAMOND! 💎💥",
        "title": "जब 100 टन के हाइड्रोलिक प्रेस के नीचे असली हीरा रखा गया! 💎😱 #Shorts #Science #Viral",
        "description": "Satisfying hydraulic press crushing vs real diamond! #Shorts #Science #HydraulicPress",
        "tags": ["hydraulicpress", "science", "diamond", "shorts", "viral"]
    },
    {
        "id": "science_02",
        "niche": "mind_blowing",
        "filename": "science_02_satisfying_crushing.mp4",
        "existing_src": "assets/downloads/fresh_mind_blowing_20261017_132126_akU5vXCWGQg.mp4",
        "search_query": "Most satisfying hydraulic press crushing moments shorts",
        "banner": "MOST SATISFYING CRUSHING EVER! 🔨🔥",
        "title": "100 टन के प्रेस ने इस चीज को सेकंडों में चकनाचूर कर दिया! 🔨💥 #Shorts #Satisfying #Viral",
        "description": "Ultra satisfying hydraulic press destruction! #Shorts #Satisfying #Crushing",
        "tags": ["satisfying", "crushing", "hydraulicpress", "shorts", "viral"]
    },
    {
        "id": "science_03",
        "niche": "mind_blowing",
        "filename": "science_03_physics_magic.mp4",
        "existing_src": None,
        "search_query": "Crazy physics experiments that look like real magic shorts",
        "banner": "PHYSICS OR REAL MAGIC? 🧪✨",
        "title": "साइंस का यह जादुई एक्सपेरिमेंट देखकर होश उड़ जाएंगे! 🧪🔥 #Shorts #Science #Magic",
        "description": "Incredible physics experiments that look like real magic! #Shorts #Physics #Science",
        "tags": ["physics", "science", "magic", "shorts", "viral"]
    },
    {
        "id": "science_04",
        "niche": "mind_blowing",
        "filename": "science_04_magnetic_putty.mp4",
        "existing_src": None,
        "search_query": "Magnetic putty swallowing metal ball satisfying shorts",
        "banner": "MAGNETIC MONSTER SWALLOWING METAL! 🧲😱",
        "title": "जब इस जादुई मैग्नेट ने लोहे को सेकंडों में निगल लिया! 🧲✨ #Shorts #Satisfying #Science",
        "description": "Magnetic putty swallowing giant neodymium magnet! #Shorts #Magnetic #Satisfying",
        "tags": ["magnetic", "satisfying", "science", "shorts", "viral"]
    }
]


def standardize_clip(src_path: str, out_path: str, max_duration: float = 28.0) -> bool:
    """Re-encodes clip into high-quality, lightweight 720p H.264/AAC (~2-3MB)."""
    cmd = [
        "ffmpeg", "-y",
        "-ss", "0",
        "-i", src_path,
        "-t", str(max_duration),
        "-vf", "scale=-2:720",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "26",
        "-c:a", "aac",
        "-b:a", "128k",
        out_path
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0 and os.path.exists(out_path) and os.path.getsize(out_path) > 100000:
        return True
    return False


def download_fresh_short(query: str, out_path: str, max_duration: float = 28.0) -> bool:
    """Downloads a short from YouTube using search query and encodes to 720p H.264."""
    tmp_tmpl = out_path + ".tmp.%(ext)s"
    cmd_dl = [
        sys.executable, "-m", "yt_dlp",
        "-f", "bv*[height<=720]+ba/b[height<=720]/best",
        "--no-playlist",
        "-o", tmp_tmpl,
        f"ytsearch1:{query}"
    ]
    print(f"📥 Downloading: {query}...")
    res = subprocess.run(cmd_dl, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"DL failed: {res.stderr[-200:]}")
        return False

    matches = glob.glob(out_path + ".tmp.*")
    if not matches:
        return False
    dl_file = matches[0]

    ok = standardize_clip(dl_file, out_path, max_duration)
    try:
        os.remove(dl_file)
    except Exception:
        pass
    return ok


def main():
    os.makedirs("assets/creator_clips", exist_ok=True)
    index_entries = []

    print(f"🚀 Populating {len(TARGET_CLIPS)} Viral Creator Clips in assets/creator_clips/...")

    for i, item in enumerate(TARGET_CLIPS, 1):
        out_path = os.path.join("assets/creator_clips", item["filename"])
        print(f"\n[{i}/{len(TARGET_CLIPS)}] Processing '{item['id']}' ({item['niche']}): {item['filename']}...")

        # 1. Check if already exists and is valid
        if os.path.exists(out_path) and os.path.getsize(out_path) > 300000:
            print(f"✓ Already exists: {out_path} ({os.path.getsize(out_path)/(1024*1024):.2f} MB)")
            index_entries.append({
                "id": item["id"],
                "niche": item["niche"],
                "filename": item["filename"],
                "banner": item["banner"],
                "title": item["title"],
                "description": item["description"],
                "tags": item["tags"]
            })
            continue

        # 2. Try existing source file
        src = item.get("existing_src")
        success = False
        if src and os.path.exists(src) and os.path.getsize(src) > 300000:
            print(f"Converting from existing source: {src}...")
            success = standardize_clip(src, out_path, max_duration=28.0)

        # 3. If not, download fresh
        if not success:
            query = item["search_query"]
            success = download_fresh_short(query, out_path, max_duration=28.0)

        if success and os.path.exists(out_path):
            size_mb = os.path.getsize(out_path) / (1024 * 1024)
            print(f"✓ Saved {out_path} ({size_mb:.2f} MB)")
            index_entries.append({
                "id": item["id"],
                "niche": item["niche"],
                "filename": item["filename"],
                "banner": item["banner"],
                "title": item["title"],
                "description": item["description"],
                "tags": item["tags"]
            })
        else:
            print(f"❌ Failed to prepare clip: {item['id']}")

    # Write index
    index_path = "assets/creator_clips/clips_index.json"
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(index_entries, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 60)
    print(f"🎉 Successfully prepared {len(index_entries)} / {len(TARGET_CLIPS)} viral creator clips!")
    print(f"Index saved to: {index_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
