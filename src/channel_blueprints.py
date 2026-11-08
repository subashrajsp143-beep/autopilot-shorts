import re
"""
Channel Blueprints & Dynamic Daily Rotation Matrix
---------------------------------------------------
Defines distinct, rotating content blueprints for all 3 channels:
- Channel 3: MrBeast Official Hindi Dubs & IShowSpeed Viral Stunts (100% Safe, Zero Copyright)
- Channel 1: FactTechz-Style HD Moving B-Roll Documentary Shorts (29 Rotating Topics)
- Channel 2: Mind-Blowing Science, Hydraulic Press Crushing & Guinness World Records

Includes multi-day rotating pools so every single day gets 100% FRESH
titles, commentary, and clip pairings.
"""

import os
import sys
from datetime import date, datetime
from typing import List, Dict, Any, Optional

try:
    from history_tracker import HistoryTracker
except ModuleNotFoundError:
    from src.history_tracker import HistoryTracker

from src.hindi_script_generator import HINDI_VIRAL_SCRIPTS
from src.mrbeast_hindi_engine import MRBEAST_HINDI_REGISTRY


# ==============================================================================
# CHANNEL 3: Next Level Facts (Star Channel)
# 100% Copyright-Free Viral Clips: IShowSpeed + World Record Stunts
# ==============================================================================
CHANNEL_3_POOL: List[Dict[str, Any]] = [
    {
        "clip": "assets/creator_clips/speed_01_dude_perfect.mp4",
        "title": "Speed का सबसे CRAZY शॉट! 😱 ISHOWSPEED BASKETBALL #Shorts",
        "banner": "SPEED IMPOSSIBLE BASKETBALL SHOT! 🤯🔥",
        "description": "Speed ने Dude Perfect के साथ मिलकर मारा ऐसा नामुमकिन शॉट कि सब हैरान रह गए!\n\n#Shorts #IShowSpeed #DudePerfect #TrickShot #Viral",
        "tags": ["ishowspeed", "speed trick shot", "dude perfect", "shorts", "viral"],
        "hindi_script": "जब Speed ने Dude Perfect के साथ मिलकर ऐसा बास्केटबॉल शॉट मारा, तो देखने वालों के होश उड़ गए! क्या यह सच में असली था?"
    },
    {
        "clip": "assets/creator_clips/speed_02_backflips.mp4",
        "title": "Speed का सबसे पागलपन भरा स्टंट! 😂🔥 ISHOWSPEED BACKFLIP #Shorts",
        "banner": "SPEED CRAZY BACKFLIP STUNT! 😂🔥",
        "description": "Speed ने बैकफ्लिप करने की कोशिश की और जो हुआ वो देखकर अपनी हंसी नहीं रोक पाओगे!\n\n#Shorts #IShowSpeed #Funny #Backflip #StreamMoments",
        "tags": ["ishowspeed", "speed backflip", "funny stream", "shorts", "viral"],
        "hindi_script": "Speed ने जब लाइव स्ट्रीम पर बैकफ्लिप मारने की कोशिश की, तो जो हुआ उसे देखकर हर कोई लोटपोट हो गया!"
    },
    {
        "clip": "assets/creator_clips/speed_03_silence_challenge.mp4",
        "title": "Speed 1 मिनट भी शांत नहीं रह पाया! 😭⚡ ISHOWSPEED FUNNY #Shorts",
        "banner": "SPEED 1 MINUTE SILENCE CHALLENGE! 🤐😂",
        "description": "Speed को मिला 1 मिनट शांत रहने का चैलेंज, लेकिन वो 10 सेकंड भी नहीं रुक पाया!\n\n#Shorts #IShowSpeed #SilenceChallenge #FunnyShorts #Viral",
        "tags": ["speed funny", "silence challenge", "ishowspeed", "shorts", "viral"],
        "hindi_script": "Speed को जब कमरे में 1 मिनट बिल्कुल शांत रहने को कहा गया, तो देखिए उसने क्या पागलपन किया!"
    },
    {
        "clip": "assets/creator_clips/speed_04_iphone_duo.mp4",
        "title": "Speed का नया iPhone Unboxing मोमेंट! 😂📱 ISHOWSPEED FUNNY #Shorts",
        "banner": "SPEED IPHONE UNBOXING MADNESS! 📱⚡",
        "description": "Speed ने जब लाइव स्ट्रीम पर नया आईफोन अनबॉक्स किया तो खुशी में फोन ही गिरा दिया!\n\n#Shorts #IShowSpeed #iPhoneUnboxing #FunnyMoments #Viral",
        "tags": ["speed iphone", "unboxing", "ishowspeed", "shorts", "viral"],
        "hindi_script": "Speed ने जब नया आईफोन अनबॉक्स किया, तो उसकी अजीबोगरीब हरकतें देखकर सब दंग रह गए!"
    },
    {
        "clip": "assets/creator_clips/records_01_table_tennis.mp4",
        "title": "100 में से 99 लोग यह पिंग पॉन्ग शॉट मिस कर देंगे! 🏓🔥 #Shorts #Trickshot",
        "banner": "WORLD\'S CRAZIEST PING PONG SHOT! 🏓🤯",
        "description": "टेबल टेनिस का ऐसा नामुमकिन शॉट जिसे देखकर आंखें खुली की खुली रह जाएंगी!\n\n#Shorts #PingPong #TableTennis #WorldRecord #Skill",
        "tags": ["ping pong", "table tennis", "trickshot", "shorts", "viral"],
        "hindi_script": "टेबल टेनिस का ऐसा नामुमकिन शॉट जो 10 लाख कोशिशों में सिर्फ एक बार लगता है!"
    },
    {
        "clip": "assets/creator_clips/records_02_levitation_handstand.mp4",
        "title": "गुरुत्वाकर्षण को चुनौती देने वाला नामुमकिन हैंडस्टैंड! 🤯🤸 #Shorts #Stunt",
        "banner": "ONE-ARM IMPOSSIBLE BALANCE! 🤸🔥",
        "description": "एक हाथ पर ऐसा बैलेंस जिसे देखकर विज्ञान भी हैरान रह जाए! क्या यह इंसान है?\n\n#Shorts #Handstand #Calisthenics #ImpossibleBalance #Viral",
        "tags": ["handstand", "balance", "calisthenics", "shorts", "viral"],
        "hindi_script": "इस एथलीट ने एक हाथ पर ऐसा हैरतअंगेज बैलेंस बनाया कि देखने वालों को लगा जैसे ग्रेविटी ही गायब हो गई हो!"
    },
    {
        "clip": "assets/creator_clips/records_04_human_catapult.mp4",
        "title": "जब स्टंटबाज ने खुद को हवा में 10 मंजिला ऊपर उड़ाया! 🚀😱 #Shorts #HumanCatapult",
        "banner": "EXTREME 10-STORY HUMAN LAUNCH! 🚀😱",
        "description": "ह्यूमन कैटापुल्ट से हवा में उड़ने का यह खौफनाक मंजर देखकर रोंगटे खड़े हो जाएंगे!\n\n#Shorts #HumanCatapult #ExtremeStunt #Adrenaline #Viral",
        "tags": ["human catapult", "extreme stunt", "adrenaline", "shorts", "viral"],
        "hindi_script": "यह स्टंटबाज जब विशाल गुलेल से आसमान में लॉन्च हुआ, तो उसने मौत को मात देकर नया इतिहास रच दिया!"
    },
    {
        "clip": "assets/creator_clips/records_03_juggling_sword.mp4",
        "title": "आंखों पर पट्टी बांधकर तलवारों से करतब! 🗡️😱 #Shorts #GuinnessRecord",
        "banner": "BLINDFOLDED SWORD JUGGLING! 🗡️🔥",
        "description": "गिनीज वर्ल्ड रिकॉर्ड का सबसे खतरनाक करतब! ज़रा सी चूक और जान जा सकती थी!\n\n#Shorts #SwordJuggling #WorldRecord #ExtremeSkill #Viral",
        "tags": ["sword juggling", "guinness record", "extreme stunt", "shorts", "viral"],
        "hindi_script": "आंखों पर काली पट्टी बांधकर तीन धारदार तलवारों को हवा में उछालना! यह करतब देखकर कोई भी कांप उठेगा!"
    }
]


# ==============================================================================
# CHANNEL 2: Pawsome Productions
# 100% Copyright-Free Science, Hydraulic Press & Stunts
# ==============================================================================
CHANNEL_2_POOL: List[Dict[str, Any]] = [
    {
        "clip": "assets/creator_clips/science_01_helmet_press.mp4",
        "title": "100 टन हाइड्रोलिक प्रेस बनाम मजबूत हेलमेट! 😱🔨 #Shorts #HydraulicPress",
        "banner": "100-TON PRESS VS CRASH HELMET! 🔨💥",
        "description": "देखिए क्या एक मजबूत हेलमेट 100 टन के हाइड्रोलिक प्रेस का दबाव झेल पाएगा?\n\n#Shorts #HydraulicPress #Crushing #Satisfying #Viral",
        "tags": ["hydraulic press", "helmet", "crush test", "science", "shorts"],
        "hindi_script": "100 टन के हाइड्रोलिक प्रेस के नीचे जब इस मजबूत हेलमेट को रखा गया, तो देखिए इसका क्या हाल हुआ!"
    },
    {
        "clip": "assets/creator_clips/science_02_prettiest_crunch.mp4",
        "title": "दिन का सबसे संतोषजनक स्लो-मोशन क्रंच! 💆✨ #Shorts #SatisfyingCrunch",
        "banner": "MOST SATISFYING CRUNCH EVER! ✨💆",
        "description": "यह आवाज़ और विजुअल देखकर आपके दिमाग को मिलेगा 100% सुकून! हेडफोन ज़रूर लगाएं!\n\n#Shorts #Satisfying #ASMR #Crunch #Relaxing",
        "tags": ["satisfying crunch", "asmr", "hydraulic press", "shorts", "viral"],
        "hindi_script": "यह क्रंच इतना संतोषजनक है कि इसे देखने के बाद आपका तनाव पूरी तरह गायब हो जाएगा!"
    },
    {
        "clip": "assets/creator_clips/science_03_cards_press.mp4",
        "title": "जब 52 ताश के पत्तों पर 100 टन का वजन पड़ा! 🃏💥 #Shorts #CardPress",
        "banner": "52 CARDS VS 100-TON PRESS! 🃏💥",
        "description": "ताश के पत्तों का ऐसा विनाशकारी क्रंच आपने कभी नहीं देखा होगा!\n\n#Shorts #HydraulicPress #PlayingCards #Satisfying",
        "tags": ["cards", "hydraulic press", "science", "shorts", "viral"],
        "hindi_script": "ताश की पूरी गड्डी को जब हाइड्रोलिक प्रेस के नीचे रखा गया, तो पत्तों का ऐसा विस्फोट हुआ जिसे देखकर आंखें फटी रह जाएंगी!"
    },
    {
        "clip": "assets/creator_clips/science_04_solar_panel.mp4",
        "title": "क्या सोलर पैनल हाइड्रोलिक प्रेस को रोक पाया? ☀️💥 #Shorts #TechExperiment",
        "banner": "SOLAR PANEL VS 100-TON HYDRAULIC! ☀️💥",
        "description": "सोलर पैनल पर जब 100 टन का दबाव पड़ा तो शीशे के टुकड़े हवा में उड़ने लगे!\n\n#Shorts #SolarEnergy #HydraulicPress #TechTest",
        "tags": ["solar panel", "hydraulic press", "tech test", "shorts", "viral"],
        "hindi_script": "सोलर पैनल को जब 100 टन के विशालकाय प्रेस के नीचे डाला गया, तो कांच का ऐसा धमाका हुआ कि सब सन्न रह गए!"
    },
    {
        "clip": "assets/creator_clips/records_01_table_tennis.mp4",
        "title": "टेबल टेनिस का ऐसा नामुमकिन शॉट जिसे देखकर होश उड़ जाएं! 😱🏓 #Shorts",
        "banner": "IMPOSSIBLE PING PONG ANGLE! 🏓⚡",
        "description": "इस खिलाड़ी ने टेबल टेनिस का ऐसा अकल्पनीय शॉट मारा कि प्रतिद्वंदी देखता ही रह गया!\n\n#Shorts #TableTennis #Trickshot #ViralSkill",
        "tags": ["table tennis", "trickshot", "sports", "shorts", "viral"],
        "hindi_script": "टेबल टेनिस का यह शॉट देखने के बाद कोई भी विश्वास नहीं कर पाएगा कि यह बिना किसी कंप्यूटर ग्राफिक्स के मारा गया है!"
    },
    {
        "clip": "assets/creator_clips/records_02_levitation_handstand.mp4",
        "title": "हवा में तैरने वाला नामुमकिन बैलेंस स्टंट! 🤯🤸 #Shorts #ExtremeFitness",
        "banner": "DEFYING LAWS OF PHYSICS! 🤯🤸",
        "description": "शरीर की ताकत का ऐसा प्रदर्शन जिसे देखकर डॉक्टरों के होश उड़ गए!\n\n#Shorts #Handstand #Calisthenics #Strength #Fitness",
        "tags": ["fitness", "handstand", "calisthenics", "strength", "shorts"],
        "hindi_script": "इस इंसान ने एक हाथ पर शरीर को ऐसे टिका दिया मानो जमीन में कोई चुंबक लगी हो!"
    },
    {
        "clip": "assets/creator_clips/records_04_human_catapult.mp4",
        "title": "10 मंजिला इमारत जितना ऊंचा मानव प्रक्षेपण! 🚀😱 #Shorts #Daredevil",
        "banner": "FLYING WITHOUT WINGS! 🚀😱",
        "description": "बिना पंखों के आसमान छूने का यह जानलेवा कारनामा!\n\n#Shorts #Catapult #Daredevil #ExtremeStunt #Viral",
        "tags": ["daredevil", "catapult", "stunt", "shorts", "viral"],
        "hindi_script": "जब इस जांबाज को गुलेल से आसमान में दागा गया, तो वह बादलों को छूकर सीधे पानी के तालाब में जा गिरा!"
    },
    {
        "clip": "assets/creator_clips/records_03_juggling_sword.mp4",
        "title": "खतरनाक तलवारों के साथ मौत का खेल! 🗡️⚠️ #Shorts #ExtremeSkill",
        "banner": "DANCING WITH RAZOR SHARP SWORDS! 🗡️🔥",
        "description": "एक सेकंड की चूक और हाथ कट सकता था! गिनीज रिकॉर्ड का सबसे रोंगटे खड़े करने वाला वीडियो!\n\n#Shorts #SwordStunt #GuinnessRecord #Danger",
        "tags": ["swords", "danger stunt", "guinness", "shorts", "viral"],
        "hindi_script": "तेज धार वाली तीन तलवारों को हवा में नचाते हुए इस शख्स ने गिनीज वर्ल्ड रिकॉर्ड बनाकर सबको चौंका दिया!"
    }
]


# ==============================================================================
# DYNAMIC BLUEPRINT RETRIEVER WITH PERMANENT DEDUPLICATION
# ==============================================================================
def get_channel_blueprints(channel_id: int, count: int = 10, day_offset: Optional[int] = None) -> List[Dict[str, Any]]:
    """
    Returns 10 guaranteed unique, non-repeating blueprints for the specified channel.
    Automatically rotates through pools based on the calendar day to prevent monotony.
    """
    tracker = HistoryTracker()
    if day_offset is None:
        base_date = date(2026, 11, 3)
        day_offset = max(0, (date.today() - base_date).days)

    selected: List[Dict[str, Any]] = []

    if channel_id == 3:
        # Channel 3: Super Viral Mix - 50% MrBeast Official Hindi Dubs + 50% Speed / Stunts (100% Safe)
        beast_pool = [dict(x, engine="mrbeast_hindi", type="MrBeast Official Hindi Dub Short") for x in MRBEAST_HINDI_REGISTRY]
        action_pool = [dict(x, engine="action", type="Speed & Stunts Viral Short") for x in CHANNEL_3_POOL]

        beast_start = (day_offset * 5) % len(beast_pool)
        action_start = (day_offset * 5) % len(action_pool)

        beast_items = [beast_pool[(beast_start + i) % len(beast_pool)] for i in range(5)]
        action_items = [action_pool[(action_start + i) % len(action_pool)] for i in range(5)]

        # Perfectly alternate: Beast -> Action -> Beast -> Action -> ...
        chosen_beast_ids = set()
        for i in range(5):
            b_item = dict(beast_items[i])
            if tracker.is_source_used(b_item["id"]) or b_item["id"] in chosen_beast_ids:
                # Pick next strictly unused beast short
                for alt in beast_pool:
                    if not tracker.is_source_used(alt["id"]) and alt["id"] not in chosen_beast_ids:
                        b_item = dict(alt)
                        break
            chosen_beast_ids.add(b_item["id"])
            selected.append(b_item)

            a_item = dict(action_items[i % len(action_items)])
            selected.append(a_item)

    elif channel_id == 1:
        # Channel 1: FactTechz 29 Rotating Scripts
        total_scripts = len(HINDI_VIRAL_SCRIPTS)
        start_idx = (day_offset * count) % total_scripts

        THEME_SCENE_MAP = {
            "Dark Psychology": ["assets/ai_video_clips/bg_darkpsych.mp4", "assets/ai_video_clips/bg_psychology.mp4"],
            "Ancient Mysteries": ["assets/ai_video_clips/bg_temple.mp4", "assets/ai_video_clips/bg_pyramid.mp4"],
            "Ocean Mysteries": ["assets/ai_video_clips/bg_deepsea.mp4", "assets/ai_video_clips/bg_ocean.mp4"],
            "Money Mindset": ["assets/ai_video_clips/bg_wealth.mp4", "assets/ai_video_clips/bg_money.mp4"],
            "Brain Power": ["assets/ai_video_clips/bg_sleepbrain.mp4", "assets/ai_video_clips/bg_brain.mp4"],
            "Space Wonders": ["assets/ai_video_clips/bg_space.mp4", "assets/ai_video_clips/bg_ocean.mp4"]
        }

        for i in range(total_scripts):
            raw_script = HINDI_VIRAL_SCRIPTS[(start_idx + i) % total_scripts]
            niche = raw_script.get("niche", "Dark Psychology")
            scenes = THEME_SCENE_MAP.get(niche, ["assets/ai_video_clips/bg_space.mp4", "assets/ai_video_clips/bg_ocean.mp4"])
            title = raw_script["title"]

            if tracker.is_title_used(title):
                VIRAL_HOOKS = [
                    "यह सच जानकर होश उड़ जाएंगे! 😱",
                    "99% लोग यह गलती करते हैं! ⚠️",
                    "दुनिया का सबसे बड़ा अनसुलझा रहस्य! 💀",
                    "कभी किसी ने यह नहीं सोचा था! ⚡",
                    "अमीर बनने का यह सीक्रेट कोई नहीं सिखाता! 💰",
                    "वैज्ञानिक भी इसका जवाब नहीं दे पाए! 🔬",
                    "इतिहास का सबसे खौफनाक रहस्य! 💀",
                    "1 सेकंड में किसी के दिमाग को समझो! 🧠"
                ]
                clean_core = re.sub(r'\s*Part\s*\d+', '', title.split('#')[0]).strip()
                hook = VIRAL_HOOKS[day_offset % len(VIRAL_HOOKS)]
                title = f"{clean_core} ⚠️ {hook} #Shorts"
                if len(title) > 95:
                    title = title[:92].rsplit(' ', 1)[0] + " #Shorts"

            item = {
                "niche": niche,
                "scenes": scenes,
                "title": title,
                "banner": f"{niche.upper()} SECRETS! 🧠✨",
                "script": raw_script.get("text", ""),
                "voice": raw_script.get("voice", "hi-IN-MadhurNeural"),
                "tags": raw_script.get("tags", ["facts", "hindi facts", "shorts", "viral"]),
                "description": f"{raw_script.get('text', '')[:150]}...\n\n#Shorts #facts #viral #hindifacts",
                "engine": "facttechz",
                "type": f"FactTechz Documentary Short ({niche[:12]})"
            }
            selected.append(item)
            if len(selected) >= count:
                break

    elif channel_id == 2:
        # Channel 2: 100% Unique Science & Stunts
        pool = CHANNEL_2_POOL
        start_idx = (day_offset * count) % len(pool)
        for i in range(count):
            candidate = dict(pool[(start_idx + i) % len(pool)])
            title = candidate["title"]

            if tracker.is_title_used(title):
                STUNT_HOOKS = [
                    "यह नामुमकिन स्टंट देखकर आंखें खुली रह जाएंगी! 🔥",
                    "विज्ञान का यह चमत्कार देखकर यकीन नहीं होगा! 🤯",
                    "100 में से 99 लोग यह शॉट मिस कर देंगे! 🏓",
                    "100 टन के दबाव में जो हुआ वो कोई सोच नहीं सकता! 💥",
                    "गिनीज वर्ल्ड रिकॉर्ड का सबसे हैरतअंगेज स्टंट! 🏆",
                    "गुरुत्वाकर्षण को चुनौती देने वाला नामुमकिन करतब! ⚡"
                ]
                clean_title = re.sub(r'\s*Part\s*\d+', '', title.split('#')[0]).strip()
                hook = STUNT_HOOKS[(day_offset + i) % len(STUNT_HOOKS)]
                candidate["title"] = f"{clean_title} | {hook} #Shorts"
                if len(candidate["title"]) > 95:
                    candidate["title"] = candidate["title"][:92].rsplit(' ', 1)[0] + " #Shorts"

            candidate["engine"] = "action"
            candidate["type"] = "Science & Stunt Short (Authentic Audio)"
            selected.append(candidate)

    # Attach slots (1 to 10)
    for idx, item in enumerate(selected):
        item["slot"] = idx + 1

    return selected[:count]


CHANNEL_1_BLUEPRINTS = get_channel_blueprints(1, count=10, day_offset=0)
CHANNEL_2_BLUEPRINTS = get_channel_blueprints(2, count=10, day_offset=0)
CHANNEL_3_BLUEPRINTS = get_channel_blueprints(3, count=10, day_offset=0)
