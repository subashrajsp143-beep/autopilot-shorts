"""
Daily 10 Videos Batch Generator & Scheduler
-------------------------------------------
Generates 10 ready-to-upload viral Shorts/Reels daily in Hindi:
- 5x AI Hindi Mystery/Psychology Shorts (Neural Voice + Bold Subtitles)
- 5x Creator Highlights / MrBeast Clips (Vertical 9:16 + Top Hook Banner)

Can automatically upload them to YouTube, Instagram, and Facebook,
or copy them all to a dedicated folder on your Desktop!
"""

import os
import sys
import re
import json
import shutil
import time
from datetime import datetime
from typing import List, Dict, Any

# Fix Windows console UTF-8 output
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from hindi_script_generator import HindiScriptGenerator
from voice_generator import generate_audio
from video_maker import VideoMaker
from clipper import CreatorClipper, VIRAL_CREATOR_PRESETS
from youtube_uploader import YouTubeUploader
from meta_uploader import MetaUploader
from visual_storyboard import VisualStoryboard
from creator_storyboard import CreatorStoryboard, CREATOR_SCRIPTS_HINDI
from history_tracker import HistoryTracker
from dynamic_creator_engine import DynamicCreatorEngine


def ensure_credentials():
    """Restores client_secrets, youtube_token, and gemini_api_key if running in cloud runner."""
    cs_path = "config/client_secrets.json"
    yt_path = "config/youtube_token.json"
    dat_path = "config/credentials.dat"
    if os.path.exists(dat_path):
        import base64
        try:
            with open(dat_path, "r", encoding="utf-8") as f:
                encoded = f.read()
            payload = json.loads(base64.b85decode(encoded.encode("utf-8")).decode("utf-8"))
            os.makedirs("config", exist_ok=True)
            if not os.path.exists(cs_path) and "client_secrets" in payload:
                with open(cs_path, "w", encoding="utf-8") as f:
                    f.write(payload["client_secrets"])
            if not os.path.exists(yt_path) and "youtube_token" in payload:
                with open(yt_path, "w", encoding="utf-8") as f:
                    f.write(payload["youtube_token"])
            if "gemini_api_key" in payload and not os.environ.get("GEMINI_API_KEY"):
                os.environ["GEMINI_API_KEY"] = payload["gemini_api_key"]
            print("Credentials unpacked successfully (including Gemini API Key).")
        except Exception as e:
            print(f"Warning: Could not unpack credentials: {e}")


# Multi-variation Creator highlights library (Rotating variations for MrBeast, Speed, etc.)
CREATOR_VARIATIONS: List[List[Dict[str, Any]]] = [
    # Clip 1: MrBeast Private Island Giveaway
    [
        {
            "creator": "MrBeast",
            "title": "मिस्टर बीस्ट का 50 करोड़ का प्राइवेट आइलैंड! 🏝️ #Shorts #MrBeast",
            "banner": "MR BEAST: PRIVATE ISLAND CHALLENGE 🏝️",
            "description": "मिस्टर बीस्ट का अब तक का सबसे महंगा चैलेंज!\n\n#Shorts #MrBeast #MrBeastHindi #ViralShorts #Trending",
            "tags": ["mrbeast", "mrbeast hindi", "private island", "shorts", "viral"],
            "start_time": 0.0,
            "duration": 30.0
        },
        {
            "creator": "MrBeast",
            "title": "जब इस लड़के ने मिस्टर बीस्ट से जीता पूरा द्वीप! 😱 #Shorts #MrBeastHindi",
            "banner": "HE WON AN ENTIRE ISLAND! 🏝️😱",
            "description": "अनजान लड़के ने जीता 50 करोड़ का प्राइवेट आइलैंड!\n\n#Shorts #MrBeast #IslandChallenge #Trending #Giveaway",
            "tags": ["mrbeast", "mrbeast hindi", "challenge", "shorts", "giveaway"],
            "start_time": 2.0,
            "duration": 30.0
        },
        {
            "creator": "MrBeast",
            "title": "$1,000,000 का आइलैंड गिवअवे! 🏝️💰 #Shorts #Viral",
            "banner": "MOST EXPENSIVE GIVEAWAY EVER! 💰",
            "description": "क्या आप 24 घंटे आइलैंड पर रहकर जीत सकते हैं?\n\n#Shorts #MrBeastHindi #MillionDollar #Trending #Viral",
            "tags": ["mrbeast", "island", "viral shorts", "trending", "shorts"],
            "start_time": 4.0,
            "duration": 30.0
        },
        {
            "creator": "MrBeast",
            "title": "आइलैंड पर 24 घंटे का सबसे खतरनाक चैलेंज! 🏝️🔥 #Shorts #MrBeast",
            "banner": "24 HOURS SURVIVING ON ISLAND! 🏝️",
            "description": "मिस्टर बीस्ट का पागलपन भरा आइलैंड मुकाबला!\n\n#Shorts #MrBeast #Survival #Viral #MrBeastHindi",
            "tags": ["mrbeast in hindi", "island", "challenge", "shorts", "viral"],
            "start_time": 1.0,
            "duration": 30.0
        }
    ],
    # Clip 2: IShowSpeed Rage & Crazy Reactions
    [
        {
            "creator": "IShowSpeed",
            "title": "स्पीड का सबसे पागलपन भरा रिएक्शन! 😂🔥 #Shorts #IShowSpeed #SpeedHindi",
            "banner": "SPEED UNCONTROLLABLE RAGE! 😂",
            "description": "स्पीड का यह रिएक्शन देखकर आपकी हंसी नहीं रुकेगी!\n\n#Shorts #IShowSpeed #SpeedHindi #FunnyShorts #Trending",
            "tags": ["ishowspeed", "speed clips", "funny shorts", "hindi shorts", "shorts"],
            "start_time": 0.0,
            "duration": 29.0
        },
        {
            "creator": "IShowSpeed",
            "title": "जब स्पीड ने गुस्से में सेटअप तोड़ दिया! 💥😂 #Shorts #SpeedHindi",
            "banner": "SPEED BROKE HIS SETUP! 💥",
            "description": "लाइव स्ट्रीम पर जब स्पीड का दिमाग पूरी तरह घूम गया!\n\n#Shorts #IShowSpeed #Rage #SpeedReaction #Gaming",
            "tags": ["speed rage", "ishowspeed", "funny", "shorts", "gaming"],
            "start_time": 0.0,
            "duration": 29.0
        },
        {
            "creator": "IShowSpeed",
            "title": "स्पीड का अब तक का सबसे फनी मोमेंट! 😂⚡ #Shorts #IShowSpeed",
            "banner": "FUNNIEST SPEED MOMENT EVER! 😂",
            "description": "इंटरनेट का सबसे अनोखा और मजेदार क्रिएटर स्पीड!\n\n#Shorts #IShowSpeed #FunnyClips #ViralHindi #Shorts",
            "tags": ["ishowspeed hindi", "funny moments", "shorts", "viral", "speed"],
            "start_time": 0.0,
            "duration": 29.0
        },
        {
            "creator": "IShowSpeed",
            "title": "स्पीड के इस रिएक्शन ने इंटरनेट हिला दिया! 🤣🔥 #Shorts #Viral",
            "banner": "WHEN SPEED LOSES HIS MIND! 🤣",
            "description": "स्पीड की ऐसी कॉमेडी आपने पहले कभी नहीं देखी होगी!\n\n#Shorts #IShowSpeed #Comedy #Trending #YouTubeShorts",
            "tags": ["ishowspeed", "speed clips hindi", "viral shorts", "trending"],
            "start_time": 0.0,
            "duration": 29.0
        }
    ],
    # Clip 3: MrBeast $1,000,000 Cash Giveaway
    [
        {
            "creator": "MrBeast",
            "title": "मिस्टर बीस्ट ने दिया 10 लाख डॉलर कैश! 💰 MR BEAST CASH GIVEAWAY #Shorts #MrBeastHindi",
            "banner": "10 LAKH DOLLAR CASH DE DIYA! 💰",
            "description": "जब मिस्टर बीस्ट ने अनजान लड़के को करोड़ों रुपये दे दिए!\n\n#Shorts #MrBeast #MrBeastHindi #MoneyChallenge #Cash",
            "tags": ["mrbeast hindi", "million dollars", "mrbeast giveaway", "shorts"],
            "start_time": 0.0,
            "duration": 30.0
        },
        {
            "creator": "MrBeast",
            "title": "सूटकेस भरकर कैश दे दिया! 💼💵 #Shorts #MrBeastHindi #Challenge",
            "banner": "SUITCASE FULL OF $100 BILLS! 💼💵",
            "description": "कांच के बक्से में 8 करोड़ रुपये कैश! जो छूटेगा वो हारेगा।\n\n#Shorts #MrBeast #Money #ViralShorts #Trending",
            "tags": ["mrbeast", "cash challenge", "giveaway", "shorts", "viral"],
            "start_time": 2.0,
            "duration": 30.0
        },
        {
            "creator": "MrBeast",
            "title": "1 मिनट में 1 करोड़ रुपये जीतने का मौका! ⏱️💰 #Shorts #MoneyChallenge",
            "banner": "CAN YOU WIN $1,000,000? ⏱️💰",
            "description": "मिस्टर बीस्ट का सबसे बड़ा पैसे का खेल!\n\n#Shorts #MrBeastHindi #Cash #Trending #MoneyShorts",
            "tags": ["mrbeast in hindi", "money challenge", "shorts", "viral"],
            "start_time": 4.0,
            "duration": 30.0
        },
        {
            "creator": "MrBeast",
            "title": "जब इस लड़के की किस्मत 1 सेकंड में बदल गई! 😱💰 #Shorts #Viral",
            "banner": "HIS LIFE CHANGED IN 1 SECOND! 😱",
            "description": "मिस्टर बीस्ट ने आम लड़के को बना दिया करोड़पति!\n\n#Shorts #MrBeast #LifeChanging #Viral #Giveaway",
            "tags": ["mrbeast", "millionaire", "giveaway", "shorts", "trending"],
            "start_time": 1.0,
            "duration": 30.0
        }
    ],
    # Clip 4: IShowSpeed Meets Cristiano Ronaldo
    [
        {
            "creator": "IShowSpeed",
            "title": "स्पीड जब रोनाल्डो से पहली बार मिला! 🐐 SPEED MEETS RONALDO #Shorts #IShowSpeed #CR7",
            "banner": "SPEED MEETS RONALDO! 🐐🔥",
            "description": "स्पीड और क्रिस्टियानो रोनाल्डो का सबसे यादगार पल!\n\n#Shorts #IShowSpeed #Ronaldo #CR7 #HindiShorts",
            "tags": ["ishowspeed", "ronaldo", "cr7", "speed and ronaldo", "shorts"],
            "start_time": 0.0,
            "duration": 30.0
        },
        {
            "creator": "IShowSpeed",
            "title": "रोनाल्डो को देखकर स्पीड के आंसू निकल गए! 😭🐐 #Shorts #IShowSpeed",
            "banner": "SPEED CRIED AFTER MEETING CR7! 😭",
            "description": "जब सालों का इंतजार खत्म हुआ और स्पीड अपने भगवान से मिला!\n\n#Shorts #IShowSpeed #CR7 #EmotionalMoment #Football",
            "tags": ["speed meets ronaldo", "cr7", "ishowspeed", "shorts", "emotional"],
            "start_time": 10.0,
            "duration": 30.0
        },
        {
            "creator": "IShowSpeed",
            "title": "स्पीड और रोनाल्डो का सबसे आइकॉनिक मोमेंट! ❤️🔥 #Shorts #CR7 #IShowSpeed",
            "banner": "MOST ICONIC MOMENT EVER! ❤️🐐",
            "description": "फुटबॉल इतिहास का सबसे वायरल और प्यारा मोमेंट!\n\n#Shorts #Ronaldo #IShowSpeed #FootballViral #GOAT",
            "tags": ["ronaldo", "cr7 goat", "ishowspeed", "shorts", "viral"],
            "start_time": 16.0,
            "duration": 30.0
        },
        {
            "creator": "IShowSpeed",
            "title": "स्पीड का सपना आखिरकार पूरा हो गया! 🐐✨ #Shorts #IShowSpeed #CR7",
            "banner": "SPEED'S GREATEST DREAM CAME TRUE! 🐐✨",
            "description": "क्रिस्टियानो रोनाल्डो और स्पीड की यह मुलाकात हमेशा याद रहेगी!\n\n#Shorts #IShowSpeed #Ronaldo #DreamComeTrue #Shorts",
            "tags": ["speed", "cr7", "ronaldo meeting", "shorts", "viral"],
            "start_time": 5.0,
            "duration": 30.0
        }
    ],
    # Clip 5: MrBeast Impossible Escape Room
    [
        {
            "creator": "MrBeast",
            "title": "दुनिया का सबसे खतरनाक एस्केप रूम! 🔒🔥 MR BEAST IMPOSSIBLE ESCAPE #Shorts #MrBeastHindi",
            "banner": "DUNIYA KA SABSE KHATARNAK ESCAPE! 🔒",
            "description": "क्या ये लोग दुनिया के सबसे मुश्किल कमरे से बाहर निकल पाए?\n\n#Shorts #MrBeast #EscapeRoom #ViralShorts #Hindi",
            "tags": ["mrbeast", "escape room", "mrbeast hindi", "challenge", "shorts"],
            "start_time": 0.0,
            "duration": 30.0
        },
        {
            "creator": "MrBeast",
            "title": "100 घंटे में इस कमरे से बाहर निकल कर दिखाओ! ⏱️🔒 #Shorts #MrBeast",
            "banner": "CAN THEY ESCAPE IN TIME? 🔒⚠️",
            "description": "चारों तरफ जाल और सिर्फ 100 घंटे का समय!\n\n#Shorts #MrBeastHindi #EscapeChallenge #Viral #Survival",
            "tags": ["mrbeast in hindi", "escape room", "survival", "shorts", "trending"],
            "start_time": 2.0,
            "duration": 30.0
        },
        {
            "creator": "MrBeast",
            "title": "मिस्टर बीस्ट का इम्पॉसिबल ट्रैप चैलेंज! 😱🔥 #Shorts #EscapeRoom #MrBeast",
            "banner": "IMPOSSIBLE TRAP CHALLENGE! 😱",
            "description": "जिसने भी यह दरवाजा खोला, उसके होश उड़ गए!\n\n#Shorts #MrBeast #ImpossibleEscape #ViralShorts #Challenge",
            "tags": ["mrbeast", "trap challenge", "shorts", "viral", "escape room"],
            "start_time": 4.0,
            "duration": 30.0
        },
        {
            "creator": "MrBeast",
            "title": "जो बाहर निकलेगा उसे मिलेंगे 5 लाख डॉलर! 💰🔒 #Shorts #MrBeastHindi",
            "banner": "ESCAPE AND WIN $500,000! 💰🔒",
            "description": "जिंदगी का सबसे कठिन और महंगा एस्केप गेम!\n\n#Shorts #MrBeast #CashPrize #Viral #Trending",
            "tags": ["mrbeast giveaway", "escape room", "shorts", "mrbeast hindi"],
            "start_time": 1.0,
            "duration": 30.0
        }
    ]
]


def get_todays_creator_presets() -> List[Dict[str, Any]]:
    """
    Returns 5 distinct creator presets for today, rotating variations daily based on calendar date.
    Guarantees different titles, banners, tags, and visual cuts every single day!
    """
    from datetime import date
    base_date = date(2026, 10, 15)
    days_passed = max(0, (date.today() - base_date).days)

    clip_files = [
        "assets/creator_clips/clip_01_mrbeast_island.mp4",
        "assets/creator_clips/clip_02_speed_reaction.mp4",
        "assets/creator_clips/clip_03_mrbeast_cash.mp4",
        "assets/creator_clips/clip_04_speed_ronaldo.mp4",
        "assets/creator_clips/clip_05_mrbeast_escape.mp4"
    ]

    presets = []
    for j in range(5):
        variations = CREATOR_VARIATIONS[j]
        var_idx = (days_passed + j) % len(variations)
        preset = dict(variations[var_idx])
        preset["clip_path"] = clip_files[j]
        presets.append(preset)

    return presets


def get_staggered_schedule(num_videos: int = 10, interval_minutes: int = 90):
    """
    Calculates strictly staggered publishing slots spaced every 90 minutes.
    Guarantees videos are strictly chronological and never out of order.
    """
    from datetime import datetime, timedelta, timezone
    now_utc = datetime.now(timezone.utc)

    # Base time is 02:30 UTC (08:00 AM IST)
    base_time = now_utc.replace(hour=2, minute=30, second=0, microsecond=0)

    # If already past 08:15 AM IST, base time moves to current time
    if now_utc > base_time + timedelta(minutes=15):
        base_time = now_utc

    schedules = []
    for i in range(num_videos):
        if i == 0:
            schedules.append(None)  # Video 1 goes live immediately
        else:
            slot = base_time + timedelta(minutes=i * interval_minutes)
            if slot <= now_utc + timedelta(minutes=5):
                slot = now_utc + timedelta(minutes=i * interval_minutes)
            schedules.append(slot.strftime("%Y-%m-%dT%H:%M:%S.000Z"))

    return schedules


def check_already_uploaded_today(force: bool = False) -> bool:
    """
    Checks if a successful batch upload has already occurred today (IST).
    Prevents duplicate uploads and protects YouTube 24-hour daily quota
    if multiple cron triggers or manual triggers run on the same day.
    """
    if force or os.environ.get("FORCE_UPLOAD") == "true":
        print("⚡ Force upload enabled. Bypassing daily duplicate guard.")
        return False

    if os.environ.get("GITHUB_ACTIONS") != "true":
        return False

    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        return False
    repo = os.environ.get("GITHUB_REPOSITORY", "subashrajsp143-beep/autopilot-shorts")
    current_run_id = int(os.environ.get("GITHUB_RUN_ID", 0))

    import urllib.request
    from datetime import datetime, timezone, timedelta
    try:
        url = f"https://api.github.com/repos/{repo}/actions/runs?status=success&per_page=5"
        req = urllib.request.Request(
            url,
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github+json",
                "User-Agent": "AutopilotGuard"
            }
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            runs = data.get("workflow_runs", [])
            ist_now = datetime.now(timezone(timedelta(hours=5, minutes=30)))
            today_str = ist_now.strftime("%Y-%m-%d")

            for r in runs:
                if r["id"] == current_run_id:
                    continue
                created_utc = datetime.fromisoformat(r["created_at"].replace("Z", "+00:00"))
                created_ist = created_utc.astimezone(timezone(timedelta(hours=5, minutes=30)))
                if created_ist.strftime("%Y-%m-%d") == today_str:
                    print(f"⚠️ A successful batch run already finished today ({created_ist.strftime('%H:%M:%S IST')}).")
                    print("🛡️ Skipping duplicate upload to protect YouTube 24-hr quota and avoid duplicate videos.")
                    return True
    except Exception as e:
        print(f"Daily guard note: {e}")
    return False


def get_cinematic_scenes_for_script(script: Dict[str, Any]) -> List[str]:
    """
    Selects matching HD moving video B-roll clips for a dynamic multi-scene documentary montage.
    100% real moving footage, zero static images.
    """
    title = script.get("title", "").lower()
    text = script.get("text", "").lower()
    niche = script.get("niche", "")
    combined = f"{title} {text} {niche}".lower()

    if "मंदिर" in combined or "जगन्नाथ" in combined or "temple" in combined:
        return ["assets/ai_video_clips/bg_temple.mp4", "assets/ai_video_clips/bg_space.mp4"]
    if "पिरामिड" in combined or "मिस्र" in combined or "pyramid" in combined:
        return ["assets/ai_video_clips/bg_pyramid.mp4", "assets/ai_video_clips/bg_space.mp4"]
    if "बरमूडा" in combined or "ट्रायंगल" in combined or "जहाज" in combined:
        return ["assets/ai_video_clips/bg_bermuda.mp4", "assets/ai_video_clips/bg_ocean.mp4"]
    if "मेगालोडन" in combined or "शार्क" in combined or "ब्लूप" in combined or "गहराई" in combined:
        return ["assets/ai_video_clips/bg_deepsea.mp4", "assets/ai_video_clips/bg_ocean.mp4"]
    if "समुद्र" in combined or "ocean" in combined:
        return ["assets/ai_video_clips/bg_ocean.mp4", "assets/ai_video_clips/bg_deepsea.mp4"]
    if "झूठ" in combined or "पुलिस" in combined or "आंख" in combined or "ट्रिक" in combined:
        return ["assets/ai_video_clips/bg_darkpsych.mp4", "assets/ai_video_clips/bg_psychology.mp4"]
    if "मनोविज्ञान" in combined or "psychology" in combined or "पर्सनालिटी" in combined:
        return ["assets/ai_video_clips/bg_psychology.mp4", "assets/ai_video_clips/bg_darkpsych.mp4"]
    if "अमीर" in combined or "करोड़पति" in combined or "बैंक" in combined or "लोन" in combined:
        return ["assets/ai_video_clips/bg_wealth.mp4", "assets/ai_video_clips/bg_money.mp4"]
    if "पैसा" in combined or "इन्वेस्ट" in combined or "कमाई" in combined or "money" in combined:
        return ["assets/ai_video_clips/bg_money.mp4", "assets/ai_video_clips/bg_wealth.mp4"]
    if "नींद" in combined or "सोने" in combined or "रात" in combined:
        return ["assets/ai_video_clips/bg_sleepbrain.mp4", "assets/ai_video_clips/bg_brain.mp4"]
    if "दिमाग" in combined or "मेमोरी" in combined or "brain" in combined:
        return ["assets/ai_video_clips/bg_brain.mp4", "assets/ai_video_clips/bg_sleepbrain.mp4"]

    NICHE_SCENE_MAP = {
        "Dark Psychology": ["assets/ai_video_clips/bg_darkpsych.mp4", "assets/ai_video_clips/bg_psychology.mp4"],
        "Ancient Mysteries": ["assets/ai_video_clips/bg_temple.mp4", "assets/ai_video_clips/bg_pyramid.mp4"],
        "Ocean Mysteries": ["assets/ai_video_clips/bg_deepsea.mp4", "assets/ai_video_clips/bg_ocean.mp4"],
        "Money Mindset": ["assets/ai_video_clips/bg_wealth.mp4", "assets/ai_video_clips/bg_money.mp4"],
        "Brain Power": ["assets/ai_video_clips/bg_brain.mp4", "assets/ai_video_clips/bg_sleepbrain.mp4"],
        "Space Wonders": ["assets/ai_video_clips/bg_space.mp4", "assets/ai_video_clips/bg_ocean.mp4"]
    }
    return NICHE_SCENE_MAP.get(niche, ["assets/ai_video_clips/bg_space.mp4", "assets/ai_video_clips/bg_ocean.mp4"])


def generate_daily_10_batch(
    output_batch_dir: str = "output/batch_today",
    copy_to_desktop: bool = False,
    upload_yt: bool = False,
    upload_meta: bool = False,
    force: bool = False
):
    print("=" * 65)
    print("🚀 GENERATING DAILY BATCH OF 10 VIRAL SHORTS (HINDI & CREATORS)")
    print("=" * 65)

    ensure_credentials()

    if upload_yt and check_already_uploaded_today(force=force):
        print("✅ Daily quota safe. Today's 10 videos are already uploaded on schedule.")
        return

    os.makedirs(output_batch_dir, exist_ok=True)
    generated_videos: List[Dict[str, Any]] = []

    # -------------------------------------------------------------
    # PART 1: 5 HIGH-RETENTION FACT & MYSTERY SHORTS (REAL VIDEO MULTI-SCENE MONTAGE)
    # -------------------------------------------------------------
    print("\n>>> [STAGE 1] Generating 5 High-Retention Fact & Mystery Shorts (Multi-Scene Montage)...")
    hindi_gen = HindiScriptGenerator()
    todays_scripts = hindi_gen.get_todays_5_scripts()
    video_maker = VideoMaker(assets_dir="assets", output_dir=output_batch_dir)

    from datetime import date
    base_date = date(2026, 10, 15)
    days_passed = max(0, (date.today() - base_date).days)

    for i, script in enumerate(todays_scripts):
        idx = i + 1
        print(f"\n[{idx}/10] Creating FactTechz-Style Mystery Short: {script['title'][:40]}...")

        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            audio_path = os.path.join(output_batch_dir, f"hindi_audio_{idx}_{timestamp}.mp3")
            ass_path = os.path.join(output_batch_dir, f"hindi_sub_{idx}_{timestamp}.ass")
            video_filename = f"video_{idx:02d}_hindi_ai.mp4"

            # Generate Hindi neural voiceover and styled ASS subtitles
            voice_res = generate_audio(
                text=script["text"],
                audio_path=audio_path,
                ass_path=ass_path,
                voice="hi-IN-MadhurNeural"
            )

            # Assign 2 matching HD moving video scenes for dynamic cut montage
            scenes = get_cinematic_scenes_for_script(script)
            valid_scenes = [s for s in scenes if os.path.exists(s)]
            if not valid_scenes:
                valid_scenes = ["assets/ai_video_clips/bg_space.mp4"]

            # Render 9:16 vertical video with multi-scene real video montage
            video_path = video_maker.render_video(
                audio_path=audio_path,
                ass_path=ass_path,
                output_filename=video_filename,
                duration=voice_res["duration"],
                bg_video_paths=valid_scenes,
                presenter_video_path=None
            )

            generated_videos.append({
                "index": idx,
                "type": "Fact & Mystery Short (Multi-Scene Montage)",
                "title": script["title"],
                "description": script["description"],
                "tags": script["tags"],
                "video_path": video_path,
                "duration": f"{voice_res['duration']:.1f}s",
                "source_id": f"script_{idx}_{script.get('niche', 'fact')}",
                "query": script.get("niche", "fact")
            })
            print(f"✓ Video {idx} ready (Multi-Scene FactTechz Style): {video_filename}")
        except Exception as e:
            print(f"❌ Failed to generate video {idx}: {e}")

    # -------------------------------------------------------------
    # PART 2: 5 REAL CREATOR & VIRAL MOMENT SHORTS (100% REAL FRESH FOOTAGE)
    # -------------------------------------------------------------
    print("\n>>> [STAGE 2] Generating 5 Real Creator Shorts (MrBeast, Speed, Viral Moments)...")
    dynamic_engine = DynamicCreatorEngine(
        downloads_dir="assets/downloads",
        output_dir=output_batch_dir
    )

    creator_niches = [
        "mrbeast",
        "ishowspeed",
        "football",
        "world_records",
        "mind_blowing"
    ]

    for j, niche in enumerate(creator_niches):
        idx = 5 + j + 1
        print(f"\n[{idx}/10] Discovering & Clipping Fresh '{niche.upper()}' Viral Footage...")

        video_filename = f"video_{idx:02d}_creator_clip.mp4"

        try:
            # 1. Dynamically download fresh, non-repeating footage from YouTube
            fresh_clip_data = dynamic_engine.download_fresh_clip(
                niche=niche,
                day_offset=days_passed + j
            )

            if not fresh_clip_data or not os.path.exists(fresh_clip_data["clip_path"]):
                raise RuntimeError(f"Could not find or download fresh footage for niche '{niche}'")

            raw_video = fresh_clip_data["clip_path"]
            banner_text = fresh_clip_data["banner"]
            clip_title = fresh_clip_data["title"]
            clip_desc = fresh_clip_data["description"]
            clip_tags = fresh_clip_data["tags"]
            source_id = fresh_clip_data["source_id"]
            query_used = fresh_clip_data["query"]

            # 2. Format into 9:16 vertical short with studio blurred background & top hook banner
            video_path = dynamic_engine.format_to_vertical_short(
                video_path=raw_video,
                banner_text=banner_text,
                output_filename=video_filename,
                duration=29.0
            )

            generated_videos.append({
                "index": idx,
                "type": f"Real Creator Short ({niche})",
                "title": clip_title,
                "description": clip_desc,
                "tags": clip_tags,
                "video_path": video_path,
                "duration": "29.0s",
                "source_id": source_id,
                "query": query_used
            })
            print(f"✓ Video {idx} ready (100% Fresh Moving Footage): {video_filename}")

        except Exception as e:
            print(f"❌ Failed creator short {idx}: {e}")
            continue

    # -------------------------------------------------------------
    # PART 3: SAVE METADATA & SCHEDULE
    # -------------------------------------------------------------
    metadata_path = os.path.join(output_batch_dir, "daily_metadata.json")
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(generated_videos, f, ensure_ascii=False, indent=2)

    # Copy to Desktop if requested
    desktop_folder = None
    if copy_to_desktop:
        try:
            desktop_path = os.path.join(os.environ["USERPROFILE"], "Desktop")
            desktop_folder = os.path.join(desktop_path, "Daily_10_Shorts")
            os.makedirs(desktop_folder, exist_ok=True)
            for v in generated_videos:
                dest = os.path.join(desktop_folder, os.path.basename(v["video_path"]))
                shutil.copy2(v["video_path"], dest)
            # Copy metadata json too
            shutil.copy2(metadata_path, os.path.join(desktop_folder, "titles_and_tags.json"))
            print(f"\n📂 All 10 videos copied to Desktop -> {desktop_folder}")
        except Exception as e:
            print(f"Warning: Could not copy to desktop: {e}")

    # Optional Auto-Upload
    if upload_yt:
        print("\n>> Uploading all 10 videos with Smart Staggered Schedule (Every 1.5 Hours)...")
        yt_uploader = YouTubeUploader()
        tracker = HistoryTracker()
        schedules = get_staggered_schedule(len(generated_videos), interval_minutes=90)
        successful_uploads = 0
        for idx, v in enumerate(generated_videos):
            slot = schedules[idx]
            try:
                upload_res = yt_uploader.upload_short(
                    video_path=v["video_path"],
                    title=v["title"],
                    description=v["description"],
                    tags=v["tags"],
                    privacy_status="public",
                    publish_at=slot
                )
                successful_uploads += 1
                tracker.record_upload(
                    title=v["title"],
                    video_type=v["type"],
                    youtube_video_id=upload_res.get("video_id"),
                    source_id=v.get("source_id"),
                    query=v.get("query")
                )
                time.sleep(4)  # pause between uploads
            except Exception as e:
                print(f"YouTube upload failed for {v['title']}: {e}")

        if generated_videos and successful_uploads == 0:
            raise RuntimeError("All YouTube uploads failed (likely daily quota or upload limit exceeded).")

    if upload_meta:
        print("\n>> Uploading to Facebook/Instagram...")
        meta_uploader = MetaUploader()
        for v in generated_videos:
            try:
                meta_uploader.upload_facebook_reel(
                    video_path=v["video_path"],
                    caption=f"{v['title']}\n\n{v['description']}"
                )
            except Exception as e:
                print(f"Meta upload failed for {v['title']}: {e}")

    print("\n" + "=" * 65)
    print("🎉 ALL 10 VIDEOS GENERATED SUCCESSFULLY!")
    if desktop_folder:
        print(f"📁 Check your Desktop folder: 'Daily_10_Shorts'")
    print("=" * 65)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Daily 10 Videos Batch Generator & Uploader")
    parser.add_argument("--upload-yt", action="store_true", help="Upload to YouTube")
    parser.add_argument("--upload-meta", action="store_true", help="Upload to Facebook & Instagram")
    parser.add_argument("--upload-all", action="store_true", help="Upload to all platforms")
    parser.add_argument("--skip-gen", action="store_true", help="Upload existing generated batch without re-rendering")
    parser.add_argument("--force", action="store_true", help="Force upload bypassing daily duplicate guard")
    args = parser.parse_args()

    upload_yt = args.upload_yt or args.upload_all
    upload_meta = args.upload_meta or args.upload_all

    if args.skip_gen:
        # Load existing batch metadata
        metadata_path = "output/batch_today/daily_metadata.json"
        if os.path.exists(metadata_path):
            with open(metadata_path, "r", encoding="utf-8") as f:
                videos = json.load(f)
            print(f"Loaded {len(videos)} existing batch videos.")
            if upload_yt:
                print(">> Uploading to YouTube...")
                uploader = YouTubeUploader()
                for v in videos[1:]:  # skip video 1 which is already uploaded
                    uploader.upload_short(v["video_path"], v["title"], v["description"], v["tags"])
                    time.sleep(4)
        else:
            print("No existing batch found. Run without --skip-gen first.")
    else:
        generate_daily_10_batch(
            copy_to_desktop=False,
            upload_yt=upload_yt,
            upload_meta=upload_meta,
            force=args.force
        )
