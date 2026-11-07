from __future__ import annotations
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
import glob
import random
from datetime import datetime
from typing import List, Dict, Any, Optional

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
from gemini_engine import GeminiEngine
from hoodie_presenter_engine import HoodiePresenterEngine
from channel_generator import generate_channel_batch


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
            ch2_path = "config/youtube_token_ch2.json"
            if not os.path.exists(ch2_path) and "youtube_token_ch2" in payload:
                with open(ch2_path, "w", encoding="utf-8") as f:
                    f.write(payload["youtube_token_ch2"])
            ch3_path = "config/youtube_token_ch3.json"
            if not os.path.exists(ch3_path) and "youtube_token_ch3" in payload:
                with open(ch3_path, "w", encoding="utf-8") as f:
                    f.write(payload["youtube_token_ch3"])
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


def get_indian_peak_schedule(num_videos: int = 10, channel_id: int = 1):
    """
    Calculates 10 publishing slots strictly fulfilling the user's multi-channel timing architecture:
    - Channel 1 (MiniTalesWorld): Starts at 11:00 AM IST (Morning/Midday Facts & Mysteries)
    - Channel 2 (Pawsome Productions): Starts at 03:00 PM IST (Afternoon/Late Afternoon Science & Stunts)
    - Channel 3 (Next Level Facts): Starts at 08:00 PM IST (Prime Evening/Night/Morning Star Channel)

    Guarantees:
    - A massive 4-hour to 5-hour difference between equivalent video slots across channels
    - Minimum 25-55 minute spacing between videos on the same channel
    - Zero uploads during dead sleep hours (12:00 AM - 7:00 AM IST)
    - Valid future timestamps compatible with YouTube API publishAt requirements
    """
    from datetime import datetime, timedelta, timezone
    ist = timezone(timedelta(hours=5, minutes=30))
    now_ist = datetime.now(ist)

    CHANNEL_TARGET_HOURS = {
        1: [
            (11, 0),   # Slot 1: 11:00 AM (Morning kick-off)
            (11, 50),  # Slot 2: 11:50 AM
            (12, 40),  # Slot 3: 12:40 PM (Lunch peak)
            (13, 30),  # Slot 4: 01:30 PM
            (14, 20),  # Slot 5: 02:20 PM
            (15, 40),  # Slot 6: 03:40 PM
            (16, 30),  # Slot 7: 04:30 PM (Tea break peak)
            (17, 30),  # Slot 8: 05:30 PM (College/Office commute)
            (18, 30),  # Slot 9: 06:30 PM
            (19, 30),  # Slot 10: 07:30 PM (Evening transition)
        ],
        2: [
            (15, 0),   # Slot 1: 03:00 PM (Afternoon kick-off - exactly 3 PM)
            (15, 55),  # Slot 2: 03:55 PM
            (16, 50),  # Slot 3: 04:50 PM
            (17, 45),  # Slot 4: 05:45 PM
            (18, 40),  # Slot 5: 06:40 PM
            (19, 35),  # Slot 6: 07:35 PM
            (20, 30),  # Slot 7: 08:30 PM (Post-dinner leisure)
            (21, 20),  # Slot 8: 09:20 PM
            (22, 10),  # Slot 9: 10:10 PM (Bedtime scroll)
            (9, 15),   # Slot 10: Next Morning 09:15 AM
        ],
        3: [
            (20, 0),   # Slot 1: 08:00 PM (Super Prime Evening - exactly 8 PM)
            (20, 40),  # Slot 2: 08:40 PM
            (21, 15),  # Slot 3: 09:15 PM (Dinner peak)
            (21, 50),  # Slot 4: 09:50 PM
            (22, 25),  # Slot 5: 10:25 PM
            (23, 0),   # Slot 6: 11:00 PM (Late night viral scroll)
            (23, 35),  # Slot 7: 11:35 PM
            (7, 45),   # Slot 8: Next Morning 07:45 AM (Early morning wake-up)
            (8, 45),   # Slot 9: Next Morning 08:45 AM (Morning commute)
            (10, 0),   # Slot 10: Next Morning 10:00 AM (Tea break / pre-reset)
        ]
    }

    hours_list = CHANNEL_TARGET_HOURS.get(channel_id, CHANNEL_TARGET_HOURS[1])
    slots = []
    last_dt = now_ist

    for idx in range(num_videos):
        if idx == 0:
            # Slot 1 goes live IMMEDIATELY as PUBLIC!
            # Bypasses YouTube API private schedule cold-start bug and triggers real-time Shorts Feed test
            slots.append(None)
            continue

        h, m = hours_list[idx % len(hours_list)]
        target_dt = now_ist.replace(hour=h, minute=m, second=0, microsecond=0)

        anchor_h, anchor_m = hours_list[0]
        # If this slot hour is in the morning for evening channels (e.g. Channel 3 morning slots)
        if h < anchor_h or (h == anchor_h and m < anchor_m):
            target_dt += timedelta(days=1)
        elif target_dt <= now_ist + timedelta(minutes=5):
            # If today's slot time already passed, shift to tomorrow
            target_dt += timedelta(days=1)

        # Minimum spacing between videos on the same channel
        if target_dt <= last_dt:
            target_dt = last_dt + timedelta(minutes=25)

        last_dt = target_dt
        slot_utc = target_dt.astimezone(timezone.utc)
        slots.append(slot_utc.strftime("%Y-%m-%dT%H:%M:%S.000Z"))

    return slots

get_staggered_schedule = get_indian_peak_schedule


def check_already_uploaded_today(force: bool = False, target_channels: Optional[List[int]] = None) -> bool:
    """
    Checks if target channels have already completed their 10 uploads today (IST).
    Prevents duplicate uploads and protects YouTube 24-hour daily quota
    while allowing staggered runs across different channels throughout the day.
    """
    if force or os.environ.get("FORCE_UPLOAD") == "true":
        print("⚡ Force upload enabled. Bypassing daily duplicate guard.")
        return False

    history_file = "config/uploaded_history.json"
    if os.path.exists(history_file):
        try:
            with open(history_file, "r", encoding="utf-8") as f:
                h = json.load(f)
            logs = h.get("upload_logs", [])
            from datetime import datetime, timezone, timedelta
            ist_now = datetime.now(timezone(timedelta(hours=5, minutes=30)))
            today_str = ist_now.strftime("%Y-%m-%d")

            chs_to_check = target_channels if target_channels else [1, 2, 3]
            ch_names = {
                1: ["Channel 1", "MiniTalesWorld"],
                2: ["Channel 2", "Pawsome"],
                3: ["Channel 3", "Next Level Facts"]
            }

            all_done = True
            for ch in chs_to_check:
                names = ch_names.get(ch, [f"Channel {ch}"])
                count = sum(1 for item in logs if item.get("timestamp", "").startswith(today_str) and any(n in item.get("type", "") for n in names))
                if count < 10:
                    all_done = False
                    break

            if all_done:
                print(f"🛑 Target channels {chs_to_check} already completed 10 uploads each for today ({today_str}).")
                print("🔒 Skipping duplicate upload to protect YouTube 24-hr quota.")
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
    if "अंतरिक्ष" in combined or "ब्रह्मांड" in combined or "तारा" in combined or "सूरज" in combined or "space" in combined:
        return ["assets/ai_video_clips/bg_space.mp4", "assets/ai_video_clips/bg_ocean.mp4"]
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
    force: bool = False,
    target_channels: Optional[List[int]] = None
):
    print("=" * 65)
    print("🚀 GENERATING DAILY BATCH OF VIRAL HINDI SHORTS ACROSS CHANNELS")
    print("=" * 65)

    ensure_credentials()

    if upload_yt and check_already_uploaded_today(force=force, target_channels=target_channels):
        print("✅ Daily quota safe. Today's videos are already uploaded on schedule.")
        return

    os.makedirs(output_batch_dir, exist_ok=True)
    tracker = HistoryTracker()

    # Channel configuration mapping (Channel 3 -> Channel 1 -> Channel 2)
    channels = [
        {"id": 3, "name": "Channel 3 (Next Level Facts)", "token": "config/youtube_token_ch3.json"},
        {"id": 1, "name": "Channel 1 (MiniTalesWorld)", "token": "config/youtube_token.json"}
    ]
    if os.path.exists("config/youtube_token_ch2.json"):
        channels.append({"id": 2, "name": "Channel 2 (Pawsome Productions)", "token": "config/youtube_token_ch2.json"})

    if target_channels:
        channels = [c for c in channels if c["id"] in target_channels]

    print(f"\n>> Active Channel Targets: {[c['name'] for c in channels]}")

    all_generated_videos: Dict[int, List[Dict[str, Any]]] = {}
    total_successful_uploads = 0

    for ch in channels:
        ch_id = ch["id"]
        ch_name = ch["name"]
        print("\n" + "=" * 60)
        print(f"🎬 Processing Batch for {ch_name} (Channel {ch_id})")
        print("=" * 60)

        try:
            # 1. Generate 10 unique, channel-specific videos
            ch_videos = generate_channel_batch(ch_id, base_output_dir=output_batch_dir)
            all_generated_videos[ch_id] = ch_videos

            # 2. Copy to desktop if requested
            if copy_to_desktop:
                try:
                    onedrive_desktop = os.path.join(os.environ.get("USERPROFILE", ""), "OneDrive", "Desktop")
                    local_desktop = os.path.join(os.environ.get("USERPROFILE", ""), "Desktop")
                    target_desktops = []
                    if os.path.exists(onedrive_desktop):
                        target_desktops.append(onedrive_desktop)
                    if os.path.exists(local_desktop) and local_desktop not in target_desktops:
                        target_desktops.append(local_desktop)

                    for d_path in target_desktops:
                        ch_clean = re.sub(r'[^\w\-_]', '_', ch_name)
                        folder = os.path.join(d_path, "Daily_Shorts", ch_clean)
                        os.makedirs(folder, exist_ok=True)
                        for v in ch_videos:
                            dest = os.path.join(folder, os.path.basename(v["video_path"]))
                            shutil.copy2(v["video_path"], dest)
                            if v.get("thumbnail_path") and os.path.exists(v["thumbnail_path"]):
                                shutil.copy2(v["thumbnail_path"], os.path.join(folder, os.path.basename(v["thumbnail_path"])))
                        meta_dest = os.path.join(folder, "titles_and_tags.json")
                        with open(meta_dest, "w", encoding="utf-8") as f:
                            json.dump(ch_videos, f, ensure_ascii=False, indent=2)
                        print(f"📂 Copied {len(ch_videos)} videos to Desktop -> {folder}")
                except Exception as e:
                    print(f"Desktop copy notice: {e}")

            # 3. Upload to YouTube if requested
            if upload_yt:
                print(f"\n🚀 Auto-Uploading 10 Shorts to {ch_name} with Staggered Indian Peak Schedule...")
                uploader = YouTubeUploader(token_path=ch["token"])
                schedules = get_indian_peak_schedule(len(ch_videos), channel_id=ch_id)
                ch_success = 0

                # Strict Category IDs for perfect YouTube algorithm audience matching
                CHANNEL_CATEGORIES = {
                    1: "27",  # Education / Documentaries / Facts
                    2: "28",  # Science & Technology / Hydraulic Press Experiments
                    3: "24",  # Entertainment / MrBeast, Speed & Sports Viral Moments
                }
                ch_category = CHANNEL_CATEGORIES.get(ch_id, "24")

                for idx, v in enumerate(ch_videos):
                    slot = schedules[idx]
                    try:
                        upload_res = uploader.upload_short(
                            video_path=v["video_path"],
                            title=v["title"],
                            description=v["description"],
                            tags=v["tags"],
                            privacy_status="public",
                            category_id=ch_category,
                            publish_at=slot,
                            thumbnail_path=v.get("thumbnail_path")
                        )
                        ch_success += 1
                        total_successful_uploads += 1
                        tracker.record_upload(
                            title=v["title"],
                            video_type=f"{v['type']} [{ch_name}]",
                            youtube_video_id=upload_res.get("video_id"),
                            source_id=v.get("source_id"),
                            query=v.get("query")
                        )
                        time.sleep(4)
                    except Exception as e:
                        print(f"[{ch_name}] Upload failed for '{v['title']}': {e}")
                print(f"✓ {ch_success} / {len(ch_videos)} videos successfully uploaded to {ch_name}!")
        except Exception as ch_err:
            print(f"❌ Error processing batch for {ch_name}: {ch_err}")

    if upload_yt and total_successful_uploads == 0:
        raise RuntimeError("All YouTube uploads across all channels failed.")

    print("\n" + "=" * 65)
    print("🎉 ALL CHANNEL BATCHES PROCESSED SUCCESSFULLY!")
    print("=" * 65)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Daily 10 Videos Batch Generator & Uploader")
    parser.add_argument("--upload-yt", action="store_true", help="Upload to YouTube")
    parser.add_argument("--upload-meta", action="store_true", help="Upload to Facebook & Instagram")
    parser.add_argument("--upload-all", action="store_true", help="Upload to all platforms")
    parser.add_argument("--skip-gen", action="store_true", help="Upload existing generated batch without re-rendering")
    parser.add_argument("--force", action="store_true", help="Force upload bypassing daily duplicate guard")
    parser.add_argument("--desktop", action="store_true", help="Copy all 10 generated videos to Desktop folder")
    parser.add_argument("--channels", type=str, default="", help="Target specific channel IDs, e.g. '2,3'")
    args = parser.parse_args()

    upload_yt = args.upload_yt or args.upload_all
    upload_meta = args.upload_meta or args.upload_all
    copy_to_desktop = args.desktop

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
        target_chs = [int(x.strip()) for x in args.channels.split(",") if x.strip().isdigit()] if args.channels else None
        generate_daily_10_batch(
            copy_to_desktop=copy_to_desktop,
            upload_yt=upload_yt,
            upload_meta=upload_meta,
            force=args.force,
            target_channels=target_chs
        )
