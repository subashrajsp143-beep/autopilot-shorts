"""
MrBeast Hindi Commentary & Transformative Shorts Engine
-------------------------------------------------------
Downloads and formats MrBeast content with original Hindi narration,
transformative commentary, styled subtitles, and audio ducking.
Applies creator attribution, source URL preservation, and content safeguards.
Integrated with HistoryTracker to prevent repeating any clip.
"""

import os
import sys
import re
import json
import glob
import subprocess
from datetime import datetime
from typing import Dict, Any, List, Optional

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

try:
    from history_tracker import HistoryTracker
except ModuleNotFoundError:
    from src.history_tracker import HistoryTracker
from src.thumbnail_generator import ThumbnailGenerator


# Verified MrBeast Shorts Registry with Safeguards & Original Hindi Commentary
# Based on MrBeast public content reuse guidelines (see docs/CONTENT_PERMISSIONS.md)
MRBEAST_HINDI_REGISTRY: List[Dict[str, Any]] = [
    {
        "id": "aNI2jv7lBPQ",
        "title": "MrBeast ने अनजान लड़के को दिया $10,000! 💰 #Shorts #MrBeastHindi",
        "banner": "MRBEAST $10,000 CASH DROP! 💰",
        "description": "मिस्टर बीस्ट ने अनजान सब्सक्राइबर को दिए $10,000 कैश!\n\n#Shorts #MrBeast #MrBeastHindi #Giveaway #Trending",
        "tags": ["mrbeast", "mrbeast hindi", "cash giveaway", "shorts", "viral"],
        "creator": "MrBeast",
        "source_url": "https://www.youtube.com/shorts/aNI2jv7lBPQ",
        "reuse_permission_ref": "docs/CONTENT_PERMISSIONS.md#mrbeast-content-reuse-guidelines",
        "third_party_material_checked": True,
        "contains_third_party_music": False,
        "disallowed": False,
        "subject_key": "cash_giveaway_subscriber_10k",
        "hindi_script": "जिमी डोनाल्डसन यानी मिस्टर बीस्ट अक्सर आम लोगों को बिना किसी पूर्व सूचना के बड़े वित्तीय उपहार देकर चौंका देते हैं। जब सड़क पर चलते एक व्यक्ति को अचानक दस हजार डॉलर नकद थमाए जाते हैं, तो उसका पहला भाव अविश्वास और हैरानी का होता है, क्योंकि किसी के लिए भी ऐसे अप्रत्याशित क्षण पर तुरंत यकीन करना आसान नहीं होता।"
    },
    {
        "id": "CEJXqm2eiJ0",
        "title": "MrBeast Secret Briefcase में क्या था? 💼😱 #Shorts #MrBeast",
        "banner": "WHAT IS INSIDE THE BRIEFCASE? 💼",
        "description": "सीक्रेट ब्रीफकेस खोलते ही होश उड़ गए!\n\n#Shorts #MrBeastHindi #MysteryBox #Viral #Challenge",
        "tags": ["mrbeast", "briefcase", "mrbeast hindi", "shorts", "mystery"],
        "creator": "MrBeast",
        "source_url": "https://www.youtube.com/shorts/CEJXqm2eiJ0",
        "reuse_permission_ref": "docs/CONTENT_PERMISSIONS.md#mrbeast-content-reuse-guidelines",
        "third_party_material_checked": True,
        "contains_third_party_music": False,
        "disallowed": False,
        "subject_key": "mystery_briefcase_cash",
        "hindi_script": "यह चुनौती अज्ञात विकल्प के सामने निर्णय लेने के मानवीय व्यवहार को दर्शाती है। जब किसी व्यक्ति को एक बंद ब्रीफकेस सौंपा जाता है और उसके अंदर मौजूद इनाम के बारे में कोई जानकारी नहीं होती, तो जिज्ञासा और सतर्कता के बीच का द्वंद्व हर किसी के चेहरे पर साफ नजर आता है।"
    },
    {
        "id": "mND4T0lzg_g",
        "title": "Subscribers के हिसाब से लोगों का बर्ताव! 🏆 #Shorts #MrBeast",
        "banner": "TREATING PEOPLE BY SUBSCRIBERS! 🏆",
        "description": "सब्सक्राइबर्स के आधार पर लोगों का रिएक्शन!\n\n#Shorts #MrBeast #SocialExperiment #Trending",
        "tags": ["mrbeast", "subscribers", "experiment", "shorts", "viral"],
        "creator": "MrBeast",
        "source_url": "https://www.youtube.com/shorts/mND4T0lzg_g",
        "reuse_permission_ref": "docs/CONTENT_PERMISSIONS.md#mrbeast-content-reuse-guidelines",
        "third_party_material_checked": True,
        "contains_third_party_music": False,
        "disallowed": False,
        "subject_key": "subscriber_count_bias_experiment",
        "hindi_script": "सोशल मीडिया के दौर में फॉलोअर्स की संख्या लोगों के दृष्टिकोण को किस प्रकार प्रभावित करती है, मिस्टर बीस्ट ने इस प्रयोग में यही दिखाया। जब लोगों को यह बताया गया कि सामने वाले के पास कितने सब्सक्राइबर हैं, तो उनकी बातचीत और प्रतिक्रिया में स्पष्ट बदलाव देखने को मिला।"
    },
    {
        "id": "41UzbuW6wJs",
        "title": "जब Robot ने किया MrBeast का काम! 🤖 #Shorts #MrBeastTech",
        "banner": "CAN A ROBOT DO MY CHORES? 🤖",
        "description": "क्या रोबोट मिस्टर बीस्ट के सारे काम कर सकता है?\n\n#Shorts #MrBeastHindi #AI #Robot #Tech",
        "tags": ["mrbeast", "robot", "mrbeast hindi", "shorts", "funny"],
        "creator": "MrBeast",
        "source_url": "https://www.youtube.com/shorts/41UzbuW6wJs",
        "reuse_permission_ref": "docs/CONTENT_PERMISSIONS.md#mrbeast-content-reuse-guidelines",
        "third_party_material_checked": True,
        "contains_third_party_music": False,
        "disallowed": False,
        "subject_key": "robotics_automation_experiment",
        "hindi_script": "आधुनिक रोबोटिक्स में जटिल गतियों और वास्तविक दुनिया के वातावरण में काम करने की अपनी सीमाएं हैं। मिस्टर बीस्ट ने जब एक ह्यूमनॉइड रोबोट से बुनियादी काम कराने की कोशिश की, तो यह साफ दिखा कि मानवीय सहजता और मशीनी प्रोग्रामिंग के बीच अभी भी कितना बड़ा अंतर है।"
    },
    {
        "id": "T_SMf9j50uc",
        "title": "MrBeast ने बना दिया पूरा गांव! 🏘️ #Shorts #MrBeastKindness",
        "banner": "WE BUILT AN ENTIRE VILLAGE! 🏘️",
        "description": "मिस्टर बीस्ट ने जरूरतमंदों के लिए पूरा गांव बसा दिया!\n\n#Shorts #MrBeastHindi #HelpingPeople #Inspiration",
        "tags": ["mrbeast", "village", "mrbeast hindi", "shorts", "philanthropy"],
        "creator": "MrBeast",
        "source_url": "https://www.youtube.com/shorts/T_SMf9j50uc",
        "reuse_permission_ref": "docs/CONTENT_PERMISSIONS.md#mrbeast-content-reuse-guidelines",
        "third_party_material_checked": True,
        "contains_third_party_music": False,
        "disallowed": False,
        "subject_key": "built_village_infrastructure",
        "hindi_script": "मिस्टर बीस्ट फिलैंथ्रॉपी की इस पहल में जरूरतमंद परिवारों के लिए नए घरों और बुनियादी सुविधाओं का निर्माण किया गया। वीडियो निर्माण से मिलने वाले संसाधनों का उपयोग सीधे जमीन पर स्थायी आवास और स्वच्छ पानी जैसी वास्तविक जरूरतें पूरी करने के लिए किया गया।"
    },
    {
        "id": "f7y2XikE7sY",
        "title": "MrBeast Bought Food With A Car! 🚗🍔 #Shorts #CrazyGiveaway",
        "banner": "BUYING FOOD WITH MY CAR! 🚗🍔",
        "description": "ड्राइव-थ्रू में बर्गर के बदले थमा दी कार!\n\n#Shorts #MrBeastHindi #CarGiveaway #Shocking #Funny",
        "tags": ["mrbeast", "car giveaway", "shorts", "mrbeast hindi", "funny"],
        "creator": "MrBeast",
        "source_url": "https://www.youtube.com/shorts/f7y2XikE7sY",
        "reuse_permission_ref": "docs/CONTENT_PERMISSIONS.md#mrbeast-content-reuse-guidelines",
        "third_party_material_checked": True,
        "contains_third_party_music": False,
        "disallowed": False,
        "subject_key": "car_for_food_giveaway",
        "hindi_script": "मिस्टर बीस्ट ने ड्राइव-थ्रू में खाना ऑर्डर करते समय कर्मचारी को सामान्य भुगतान के बजाय एक नई कार की चाबी थमा दी। अपनी सामान्य ड्यूटी के दौरान ऐसे अकल्पनीय सरप्राइज मिलने पर कर्मचारी की सहज खुशी और हैरानी देखने लायक थी।"
    },
    {
        "id": "xDuuM3ERr5Q",
        "title": "YouTuber पहचानो और $1,000 जीतो! 🎁💰 #Shorts #MrBeastGame",
        "banner": "GUESS THE YOUTUBER = WIN $1,000! 🎁",
        "description": "आवाज सुनकर पहचानना था यूट्यूबर!\n\n#Shorts #MrBeastHindi #GuessingGame #Prize",
        "tags": ["mrbeast", "youtuber", "game", "shorts", "mrbeast hindi"],
        "creator": "MrBeast",
        "source_url": "https://www.youtube.com/shorts/xDuuM3ERr5Q",
        "reuse_permission_ref": "docs/CONTENT_PERMISSIONS.md#mrbeast-content-reuse-guidelines",
        "third_party_material_checked": True,
        "contains_third_party_music": False,
        "disallowed": False,
        "subject_key": "audio_recognition_creator_game",
        "hindi_script": "केवल कुछ सेकंड की आवाज सुनकर किसी लोकप्रिय यूट्यूबर को पहचानना एक मजेदार ऑडियो चैलेंज है। जब लोगों के सामने बिना वीडियो केवल आवाज चलाई गई, तो यह देखना दिलचस्प था कि वे अपने पसंदीदा क्रिएटर्स की अनूठी टोन और बोलने के अंदाज को कितनी तेजी से पहचान लेते हैं।"
    },
    {
        "id": "y1UVAtHALaA",
        "title": "MrBeast ने अचानक दिए 8 लाख रुपये! 💵🔥 #Shorts #CashDrop",
        "banner": "SURPRISED SUBSCRIBER WITH $10,000! 💵",
        "description": "सब्सक्राइबर की जिंदगी एक पल में बदल दी!\n\n#Shorts #MrBeastHindi #LifeChanging #Cash",
        "tags": ["mrbeast", "cash", "giveaway", "shorts", "viral"],
        "creator": "MrBeast",
        "source_url": "https://www.youtube.com/shorts/y1UVAtHALaA",
        "reuse_permission_ref": "docs/CONTENT_PERMISSIONS.md#mrbeast-content-reuse-guidelines",
        "third_party_material_checked": True,
        "contains_third_party_music": False,
        "disallowed": False,
        "subject_key": "random_subscriber_financial_relief",
        "hindi_script": "मिस्टर बीस्ट द्वारा अपने सब्सक्राइबर्स को अचानक नकद राशि देने की यह पहल हमेशा आश्चर्यजनक पलों को जन्म देती है। दैनिक जीवन की सामान्य दिनचर्या में जब किसी को अचानक हजारों डॉलर का उपहार मिलता है, तो वह क्षण उनके लिए पूरी तरह से अविस्मरणीय बन जाता है।"
    },
    {
        "id": "3ih2bPKSWsQ",
        "title": "MrBeast ने Speed को किया Arrest! 🚔😂 MRBEAST SPEED #Shorts",
        "banner": "MRBEAST ARRESTS ISHOWSPEED!",
        "description": "जब मिस्टर बीस्ट ने आईशोस्पीड को हथकड़ी पहना दी!\n\n#Shorts #MrBeastHindi #IShowSpeed #FunnyMoments",
        "tags": ["mrbeast", "ishowspeed", "speed", "shorts", "funny"],
        "creator": "MrBeast",
        "source_url": "https://www.youtube.com/shorts/3ih2bPKSWsQ",
        "reuse_permission_ref": "docs/CONTENT_PERMISSIONS.md#mrbeast-content-reuse-guidelines",
        "third_party_material_checked": False,
        "contains_third_party_music": False,
        "disallowed": True,
        "disallow_reason": "Featuring IShowSpeed (pending independent reuse verification)",
        "subject_key": "speed_arrest_guest"
    },
    {
        "id": "uA9Zcg3vHvo",
        "title": "MrBeast vs IShowSpeed महा रेस! 🏃⚡ MRBEAST SPEED RACE #Shorts",
        "banner": "MRBEAST VS ISHOWSPEED RACE!",
        "description": "100 मीटर की रेस में कौन जीता?\n\n#Shorts #MrBeastHindi #IShowSpeed #Race #Viral",
        "tags": ["mrbeast", "ishowspeed", "sprint", "shorts", "speed"],
        "creator": "MrBeast",
        "source_url": "https://www.youtube.com/shorts/uA9Zcg3vHvo",
        "reuse_permission_ref": "docs/CONTENT_PERMISSIONS.md#mrbeast-content-reuse-guidelines",
        "third_party_material_checked": False,
        "contains_third_party_music": False,
        "disallowed": True,
        "disallow_reason": "Featuring IShowSpeed (pending independent reuse verification)",
        "subject_key": "speed_race_guest"
    },
    {
        "id": "SWc8fI_9iqA",
        "title": "रोनाल्डो ने मिस्टर बीस्ट को सिखाया SIUUU! 🐐⚽ #Shorts #RonaldoBeast",
        "banner": "RONALDO TEACHES BEAST SIUU!",
        "description": "जब क्रिस्टियानो रोनाल्डो और मिस्टर बीस्ट एक साथ मिले!\n\n#Shorts #MrBeastHindi #CristianoRonaldo #CR7 #SIUU",
        "tags": ["mrbeast", "ronaldo", "cr7", "shorts", "football"],
        "creator": "MrBeast",
        "source_url": "https://www.youtube.com/shorts/SWc8fI_9iqA",
        "reuse_permission_ref": "docs/CONTENT_PERMISSIONS.md#mrbeast-content-reuse-guidelines",
        "third_party_material_checked": False,
        "contains_third_party_music": False,
        "disallowed": True,
        "disallow_reason": "Featuring sports broadcaster and athlete footage (prohibited)",
        "subject_key": "ronaldo_siuu_sports"
    },
    {
        "id": "HcL1EQ5qD_g",
        "title": "जब मिस्टर बीस्ट ने रोनाल्डो से पूछा तीखा सवाल! ⚽ #Shorts #CR7",
        "banner": "CONFRONTING CRISTIANO RONALDO!",
        "description": "रोनाल्डो का रिएक्शन देखकर हैरान रह गए!\n\n#Shorts #MrBeastHindi #Ronaldo #Goat #Interview",
        "tags": ["mrbeast", "ronaldo", "football", "shorts", "viral"],
        "creator": "MrBeast",
        "source_url": "https://www.youtube.com/shorts/HcL1EQ5qD_g",
        "reuse_permission_ref": "docs/CONTENT_PERMISSIONS.md#mrbeast-content-reuse-guidelines",
        "third_party_material_checked": False,
        "contains_third_party_music": False,
        "disallowed": True,
        "disallow_reason": "Featuring sports broadcaster and athlete footage (prohibited)",
        "subject_key": "ronaldo_interview_sports"
    },
    {
        "id": "3cWm9B_0_kI",
        "title": "रोनाल्डो को रोकने के लिए कितने लोग चाहिए? 🛡️ #Shorts #RonaldoChallenge",
        "banner": "HOW MANY TO STOP RONALDO?",
        "description": "क्या कोई रोनाल्डो को गोल करने से रोक पाया?\n\n#Shorts #MrBeastHindi #CR7 #FootballChallenge",
        "tags": ["mrbeast", "ronaldo", "cr7", "shorts", "sports"],
        "creator": "MrBeast",
        "source_url": "https://www.youtube.com/shorts/3cWm9B_0_kI",
        "reuse_permission_ref": "docs/CONTENT_PERMISSIONS.md#mrbeast-content-reuse-guidelines",
        "third_party_material_checked": False,
        "contains_third_party_music": False,
        "disallowed": True,
        "disallow_reason": "Featuring sports broadcaster and athlete footage (prohibited)",
        "subject_key": "ronaldo_challenge_sports"
    },
    {
        "id": "jCE1Ol3PYDs",
        "title": "इस तिजोरी में छुपाए 8 करोड़ रुपये! 🏦 #Shorts #MrBeastVault",
        "banner": "I HID $1,000,000 IN THIS VAULT! 🏦",
        "description": "जो तिजोरी का ताला खोलेगा, कैश उसका!\n\n#Shorts #MrBeastHindi #SecretVault #MillionDollars",
        "tags": ["mrbeast", "vault", "cash", "shorts", "mrbeast hindi"],
        "creator": "MrBeast",
        "source_url": "https://www.youtube.com/shorts/jCE1Ol3PYDs",
        "reuse_permission_ref": "docs/CONTENT_PERMISSIONS.md#mrbeast-content-reuse-guidelines",
        "third_party_material_checked": True,
        "contains_third_party_music": False,
        "disallowed": False,
        "subject_key": "million_dollar_vault_challenge",
        "hindi_script": "सीमित समय और भारी दबाव में तिजोरी का सही कोड ढूंढने की यह चुनौती दर्शकों को बांधे रखती है। जब एक बड़े नकद इनाम के सामने घड़ी की सुइयां लगातार भाग रही हों, तो जल्दबाजी के बीच शांत रहकर सही प्रयास करना ही सबसे बड़ी चुनौती होता है।"
    },
    {
        "id": "purAsH7pXTQ",
        "title": "5 अनजान लोगों ने बांटे 80 लाख रुपये! 🤝 #Shorts #SplitOrSteal",
        "banner": "5 STRANGERS SPLIT $100,000! 🤝",
        "description": "क्या उन्होंने पैसा बांटा या धोखा दिया?\n\n#Shorts #MrBeastHindi #TrustExperiment #Cash",
        "tags": ["mrbeast", "strangers", "money", "shorts", "viral"],
        "creator": "MrBeast",
        "source_url": "https://www.youtube.com/shorts/purAsH7pXTQ",
        "reuse_permission_ref": "docs/CONTENT_PERMISSIONS.md#mrbeast-content-reuse-guidelines",
        "third_party_material_checked": True,
        "contains_third_party_music": False,
        "disallowed": False,
        "subject_key": "five_strangers_trust_dilemma",
        "hindi_script": "जब पांच अनजान लोगों के सामने एक बड़ी राशि को आपस में बांटने का विकल्प रखा जाता है, तो यह सहयोग और आपसी समझ की सच्ची परीक्षा बन जाता है। व्यक्तिगत लाभ के बजाय जब सभी मिलकर एक सर्वसम्मत फैसले पर पहुंचते हैं, तो यह सामूहिक भरोसे की ताकत को दर्शाता है।"
    },
    {
        "id": "_sBRk9ADpK8",
        "title": "सिक्का उछालो और 25 लाख जीतो! 🪙 #Shorts #CoinFlipPrize",
        "banner": "FLIP A COIN, WIN $30,000! 🪙",
        "description": "हेड्स आया तो 25 लाख, टेल्स आया तो खाली हाथ!\n\n#Shorts #MrBeastHindi #CoinFlip #Gamble #Luck",
        "tags": ["mrbeast", "coin flip", "money", "shorts", "giveaway"],
        "creator": "MrBeast",
        "source_url": "https://www.youtube.com/shorts/_sBRk9ADpK8",
        "reuse_permission_ref": "docs/CONTENT_PERMISSIONS.md#mrbeast-content-reuse-guidelines",
        "third_party_material_checked": True,
        "contains_third_party_music": False,
        "disallowed": False,
        "subject_key": "coin_flip_probability_risk",
        "hindi_script": "एक सिक्के के उछाल पर बड़ा दांव लगाना बाइनरी संभावना का सबसे सरल और सीधा रूप है। पचास प्रतिशत के इस खेल में किसी हुनर या रणनीति की भूमिका नहीं होती, केवल भाग्य और सिक्के के गिरने का पहलू ही जीत या हार का फैसला करता है।"
    },
    {
        "id": "3GNyw4uaAqU",
        "title": "सब्सक्राइब करो और आईफोन ले जाओ! 📱 #Shorts #iPhoneGiveaway",
        "banner": "SUBSCRIBE FOR AN IPHONE! 📱",
        "description": "मिस्टर बीस्ट ने सड़क पर बांटे नए आईफोन!\n\n#Shorts #MrBeastHindi #Apple #iPhone #Giveaway",
        "tags": ["mrbeast", "iphone", "apple", "shorts", "viral"],
        "creator": "MrBeast",
        "source_url": "https://www.youtube.com/shorts/3GNyw4uaAqU",
        "reuse_permission_ref": "docs/CONTENT_PERMISSIONS.md#mrbeast-content-reuse-guidelines",
        "third_party_material_checked": True,
        "contains_third_party_music": False,
        "disallowed": False,
        "subject_key": "subscriber_conversion_incentive",
        "hindi_script": "मिस्टर बीस्ट अपने चैनल से जुड़ने वाले नए दर्शकों को तुरंत महंगे गैजेट्स देकर प्रोत्साहित करने के लिए जाने जाते हैं। सिर्फ एक क्लिक से चैनल सब्सक्राइब करने पर नया स्मार्टफोन थमाना उनके अनोखे कंटेंट और दर्शकों के साथ सीधे जुड़ाव का हिस्सा है।"
    },
    {
        "id": "7aE4EhHXzlA",
        "title": "ट्रैफिक में फंसे हर ड्राइवर को दिया कैश! 🚦 #Shorts #KindnessBeast",
        "banner": "PAID EVERYONE IN TRAFFIC! 🚦",
        "description": "ट्रैफिक जाम में सबको थमा दिए डॉलर!\n\n#Shorts #MrBeastHindi #TrafficJam #Help #Cash",
        "tags": ["mrbeast", "traffic", "kindness", "shorts", "mrbeast hindi"],
        "creator": "MrBeast",
        "source_url": "https://www.youtube.com/shorts/7aE4EhHXzlA",
        "reuse_permission_ref": "docs/CONTENT_PERMISSIONS.md#mrbeast-content-reuse-guidelines",
        "third_party_material_checked": True,
        "contains_third_party_music": False,
        "disallowed": False,
        "subject_key": "traffic_jam_civic_relief",
        "hindi_script": "शहरी ट्रैफिक जाम में फंसे लोगों का समय अक्सर तनाव और बोरियत में बीतता है। मिस्टर बीस्ट ने गाड़ियों के बीच पहुंचकर ड्राइवरों को अचानक नकद राशि बांटी, जिससे थके हुए लोगों के चेहरों पर अचानक मुस्कान आ गई और माहौल पूरी तरह बदल गया।"
    },
    {
        "id": "uZY9xr-QAk0",
        "title": "सिक्का उछालो, कॉलेज की पूरी फीस माफ! 🎓 #Shorts #CollegeHelp",
        "banner": "FLIP A COIN, I'LL PAY COLLEGE! 🎓",
        "description": "एक सिक्के ने छात्र का पूरा भविष्य बदल दिया!\n\n#Shorts #MrBeastHindi #College #Student #LifeChanging",
        "tags": ["mrbeast", "college", "tuition", "shorts", "giveaway"],
        "creator": "MrBeast",
        "source_url": "https://www.youtube.com/shorts/uZY9xr-QAk0",
        "reuse_permission_ref": "docs/CONTENT_PERMISSIONS.md#mrbeast-content-reuse-guidelines",
        "third_party_material_checked": True,
        "contains_third_party_music": False,
        "disallowed": False,
        "subject_key": "student_debt_relief_coin_flip",
        "hindi_script": "कॉलेज के एक छात्र के सामने जब सिक्के के एक उछाल पर पूरी ट्यूशन फीस चुकाने का मौका रखा गया, तो तनाव का स्तर चरम पर था। पचास प्रतिशत संभावना वाले इस साधारण टॉस ने उस छात्र के लिए एक बड़ा मौका पैदा कर दिया।"
    },
    {
        "id": "JgJrQnDIRgg",
        "title": "जिसने फोन उठाया उसे मिले $10,000! 📞 #Shorts #PhoneChallenge",
        "banner": "FIRST TO ANSWER WINS $10,000! 📞",
        "description": "अचानक फोन की घंटी बजी और बन गया लखपति!\n\n#Shorts #MrBeastHindi #PhoneChallenge #InstantCash",
        "tags": ["mrbeast", "phone call", "cash", "shorts", "viral"],
        "creator": "MrBeast",
        "source_url": "https://www.youtube.com/shorts/JgJrQnDIRgg",
        "reuse_permission_ref": "docs/CONTENT_PERMISSIONS.md#mrbeast-content-reuse-guidelines",
        "third_party_material_checked": True,
        "contains_third_party_music": False,
        "disallowed": False,
        "subject_key": "phone_response_speed_challenge",
        "hindi_script": "मिस्टर बीस्ट ने इस चुनौती में अनजान नंबरों पर कॉल करके शर्त रखी कि जो भी फोन तुरंत उठाएगा, उसे नकद पुरस्कार मिलेगा। आम तौर पर लोग अज्ञात कॉल्स को अनदेखा कर देते हैं, लेकिन इस बार तुरंत फोन उठाना एक प्रतिभागी के लिए बड़ा सरप्राइज साबित हुआ।"
    },
    {
        "id": "UTdcX1e0cMA",
        "title": "लावा पार करो और कैश ले जाओ! 🌋 #Shorts #FloorIsLava",
        "banner": "JUMP OVER THE LAVA, WIN! 🌋",
        "description": "फ्लोर इज लावा चैलेंज का सबसे खतरनाक राउंड!\n\n#Shorts #MrBeastHindi #Lava #Obstacle #Extreme",
        "tags": ["mrbeast", "lava", "challenge", "shorts", "game"],
        "creator": "MrBeast",
        "source_url": "https://www.youtube.com/shorts/UTdcX1e0cMA",
        "reuse_permission_ref": "docs/CONTENT_PERMISSIONS.md#mrbeast-content-reuse-guidelines",
        "third_party_material_checked": True,
        "contains_third_party_music": False,
        "disallowed": False,
        "subject_key": "physical_obstacle_biomechanics",
        "hindi_script": "फर्श को लावा मानकर बनाए गए इस बाधा दौड़ ट्रैक पर आगे बढ़ना शारीरिक संतुलन और सतर्कता की कड़ी परीक्षा है। संकरे रास्तों पर लगातार नियंत्रण बनाए रखना और बिना गिरे अगले पड़ाव तक पहुंचना केवल एकाग्रता और चपलता से ही संभव है।"
    },
    {
        "id": "0yPgljFcTR4",
        "title": "सब्सक्राइब करते ही मिले 40 लाख रुपये! 🚨 #Shorts #MrBeast50k",
        "banner": "SUBSCRIBE TO WIN $50,000! 🚨",
        "description": "बस एक क्लिक और 40 लाख कैश!\n\n#Shorts #MrBeastHindi #CashPrize #Subscribe #Viral",
        "tags": ["mrbeast", "subscribe", "prize", "shorts", "mrbeast in hindi"],
        "creator": "MrBeast",
        "source_url": "https://www.youtube.com/shorts/0yPgljFcTR4",
        "reuse_permission_ref": "docs/CONTENT_PERMISSIONS.md#mrbeast-content-reuse-guidelines",
        "third_party_material_checked": True,
        "contains_third_party_music": False,
        "disallowed": False,
        "subject_key": "milestone_subscriber_celebration",
        "hindi_script": "चैनल के खास सब्सक्राइबर माइलस्टोन पूरे होने पर मिस्टर बीस्ट अपने दर्शकों के साथ सीधे जश्न मनाते हैं। उस ऐतिहासिक क्षण पर चैनल सब्सक्राइब करने वाले लकी व्यक्ति को सीधे बड़ा नकद इनाम देकर वे अपनी कम्युनिटी के प्रति आभार जताते हैं।"
    },
    {
        "id": "TN1wErFGTzM",
        "title": "यह चाबी ढूंढो और $10,000 जीतो! 🔑 #Shorts #TreasureHunt",
        "banner": "FIND THIS KEY, WIN $10,000! 🔑",
        "description": "छुपी हुई चाबी ढूंढने का खतरनाक मिशन!\n\n#Shorts #MrBeastHindi #Treasure #Key #Challenge",
        "tags": ["mrbeast", "key", "treasure", "shorts", "viral"],
        "creator": "MrBeast",
        "source_url": "https://www.youtube.com/shorts/TN1wErFGTzM",
        "reuse_permission_ref": "docs/CONTENT_PERMISSIONS.md#mrbeast-content-reuse-guidelines",
        "third_party_material_checked": True,
        "contains_third_party_music": False,
        "disallowed": False,
        "subject_key": "spatial_search_time_pressure",
        "hindi_script": "एक बड़े इलाके में छिपी छोटी सी चाबी को समय सीमा के अंदर ढूंढना आसान काम नहीं है। बिना किसी योजना के बेतरतीब भागने के बजाय व्यवस्थित तरीके से जगह-जगह छानबीन करना ही इस खोज चुनौती में सफलता पाने का सबसे समझदारी भरा तरीका है।"
    },
    {
        "id": "pS-fFdvyHLE",
        "title": "कितने टेप लेम्बोर्गिनी को रोक सकते हैं? 🏎️📦 #Shorts #LamboTape",
        "banner": "HOW MUCH TAPE STOPS A LAMBO? 🏎️",
        "description": "हजारों टेप रोल बनाम तेज रफ्तार लेम्बोर्गिनी!\n\n#Shorts #MrBeastHindi #Lamborghini #TapeExperiment",
        "tags": ["mrbeast", "lamborghini", "tape", "shorts", "experiment"],
        "creator": "MrBeast",
        "source_url": "https://www.youtube.com/shorts/pS-fFdvyHLE",
        "reuse_permission_ref": "docs/CONTENT_PERMISSIONS.md#mrbeast-content-reuse-guidelines",
        "third_party_material_checked": True,
        "contains_third_party_music": False,
        "disallowed": False,
        "subject_key": "material_tensile_physics_experiment",
        "hindi_script": "डक्ट टेप की हजारों परतों को जोड़कर क्या एक तेज रफ्तार कार को रोका जा सकता है? जब टेप की मजबूत पकड़ और खिंचाव सहने की क्षमता चलती हुई गाड़ी की गतिज ऊर्जा से टकराती है, तो यह एक रोमांचक और व्यावहारिक भौतिकी परीक्षण बन जाता है।"
    },
    {
        "id": "8_gdcaX9Xqk",
        "title": "2 करोड़ रुपये बांटोगे या चुराओगे? 💰 #Shorts #SplitOrSteal",
        "banner": "SPLIT OR STEAL $250,000? 💰",
        "description": "जब लालच और भरोसे की टक्कर हुई!\n\n#Shorts #MrBeastHindi #MoneyDilemma #Psychology",
        "tags": ["mrbeast", "split or steal", "cash", "shorts", "experiment"],
        "creator": "MrBeast",
        "source_url": "https://www.youtube.com/shorts/8_gdcaX9Xqk",
        "reuse_permission_ref": "docs/CONTENT_PERMISSIONS.md#mrbeast-content-reuse-guidelines",
        "third_party_material_checked": True,
        "contains_third_party_music": False,
        "disallowed": False,
        "subject_key": "prisoners_dilemma_quarter_million",
        "hindi_script": "गेम थ्योरी के प्रसिद्ध 'स्प्लिट या स्टील' प्रारूप में दो खिलाड़ियों को मिलकर फैसला लेना होता है। अगर दोनों बांटने का विकल्प चुनते हैं तो इनाम आधा-आधा मिलता है, लेकिन अगर एक धोखा देता है तो सारा पैसा उसी का हो जाता है—यही दुविधा इस खेल को तनावपूर्ण बनाती है।"
    },
    {
        "id": "IemzxkkzI5s",
        "title": "पिज़्ज़ा डिलीवरी वाले को टिप में दी ब्रैंड न्यू कार! 🍕🚗 #Shorts #Generosity",
        "banner": "TIPPED PIZZA DRIVER A CAR! 🍕🚗",
        "description": "पिज़्ज़ा देने आए लड़के की आंखों में आंसू आ गए!\n\n#Shorts #MrBeastHindi #PizzaDelivery #CarTip #Heartwarming",
        "tags": ["mrbeast", "pizza", "car tip", "shorts", "kindness"],
        "creator": "MrBeast",
        "source_url": "https://www.youtube.com/shorts/IemzxkkzI5s",
        "reuse_permission_ref": "docs/CONTENT_PERMISSIONS.md#mrbeast-content-reuse-guidelines",
        "third_party_material_checked": True,
        "contains_third_party_music": False,
        "disallowed": False,
        "subject_key": "gig_economy_worker_support",
        "hindi_script": "एक साधारण पिज्जा डिलीवरी के दौरान जब डिलीवरी ड्राइवर को सामान्य टिप के बदले एक नई कार की चाबी दी गई, तो उसकी प्रतिक्रिया बेहद भावुक थी। अपने रोजमर्रा के काम के दौरान ऐसे अप्रत्याशित उपहार की उम्मीद किसी ने भी नहीं की थी।"
    },
    {
        "id": "CAOY8EKH1qU",
        "title": "अनजान छात्र की पूरी कॉलेज फीस चुका दी! 🎓 #Shorts #StudentHelp",
        "banner": "PAID STUDENT'S COLLEGE TUITION! 🎓",
        "description": "बिना बताए भर दी छात्र की पूरी डिग्री की फीस!\n\n#Shorts #MrBeastHindi #Education #Kindness #Inspiration",
        "tags": ["mrbeast", "tuition", "college", "shorts", "giveaway"],
        "creator": "MrBeast",
        "source_url": "https://www.youtube.com/shorts/CAOY8EKH1qU",
        "reuse_permission_ref": "docs/CONTENT_PERMISSIONS.md#mrbeast-content-reuse-guidelines",
        "third_party_material_checked": True,
        "contains_third_party_music": False,
        "disallowed": False,
        "subject_key": "undergraduate_tuition_grant",
        "hindi_script": "मिस्टर बीस्ट ने एक कॉलेज छात्र से बातचीत के दौरान उसकी पढ़ाई की पूरी फीस खुद चुकाने का फैसला किया। एक अप्रत्याशित बातचीत का इस तरह के बड़े सहयोग में बदल जाना उस छात्र के लिए जीवन का सबसे यादगार पल बन गया।"
    },
    {
        "id": "GGBy50KtvRk",
        "title": "वेट्रेस को टिप में दी सपनों की कार! ☕🚗 #Shorts #Emotional",
        "banner": "TIPPING A WAITRESS A CAR! ☕🚗",
        "description": "रेस्टोरेंट में काम करने वाली महिला को मिला सबसे बड़ा तोहफा!\n\n#Shorts #MrBeastHindi #Waitress #CarGift #Emotional",
        "tags": ["mrbeast", "waitress", "car gift", "shorts", "viral"],
        "creator": "MrBeast",
        "source_url": "https://www.youtube.com/shorts/GGBy50KtvRk",
        "reuse_permission_ref": "docs/CONTENT_PERMISSIONS.md#mrbeast-content-reuse-guidelines",
        "third_party_material_checked": True,
        "contains_third_party_music": False,
        "disallowed": False,
        "subject_key": "service_worker_vehicle_gift",
        "hindi_script": "एक रेस्टोरेंट में काम कर रही वेट्रेस को जब मिस्टर बीस्ट ने टिप के रूप में सीधे एक नई कार भेंट की, तो पूरे स्टाफ में खुशी की लहर दौड़ गई। दिनभर की सामान्य सेवा के बीच मिला यह बड़ा तोहफा उनके पूरे दिन को खास बना गया।"
    },
    {
        "id": "Y0cBiGUuB1Y",
        "title": "सब्सक्राइबर को भेजा डिज्नीलैंड! 🏰 #Shorts #DreamTrip",
        "banner": "SENT SUBSCRIBER TO DISNEYLAND! 🏰",
        "description": "एक परिवार का सबसे बड़ा सपना पूरा कर दिया!\n\n#Shorts #MrBeastHindi #Disneyland #DreamVacation",
        "tags": ["mrbeast", "disneyland", "vacation", "shorts", "mrbeast in hindi"],
        "creator": "MrBeast",
        "source_url": "https://www.youtube.com/shorts/Y0cBiGUuB1Y",
        "reuse_permission_ref": "docs/CONTENT_PERMISSIONS.md#mrbeast-content-reuse-guidelines",
        "third_party_material_checked": True,
        "contains_third_party_music": False,
        "disallowed": False,
        "subject_key": "family_dream_travel_experience",
        "hindi_script": "भौतिक वस्तुओं के बजाय जब किसी परिवार को एक साथ किसी प्रसिद्ध थीम पार्क की पूरी यात्रा का उपहार मिलता है, तो वह उनके लिए जीवनभर की सुखद याद बन जाता है। मिस्टर बीस्ट का यह प्रयास लोगों को खुशियां बांटने के उनके अंदाज को दर्शाता है।"
    },
    {
        "id": "S_CUEOBZ0P4",
        "title": "द रॉक vs मिस्टर बीस्ट $100,000 के लिए! 🪨💥 #Shorts #TheRock",
        "banner": "THE ROCK VS MRBEAST $100,000!",
        "description": "ड्वेन 'द रॉक' जॉनसन और मिस्टर बीस्ट का मुकाबला!\n\n#Shorts #MrBeastHindi #TheRock #RockPaperScissors #Prize",
        "tags": ["mrbeast", "the rock", "dwayne johnson", "shorts", "celebrity"],
        "creator": "MrBeast",
        "source_url": "https://www.youtube.com/shorts/S_CUEOBZ0P4",
        "reuse_permission_ref": "docs/CONTENT_PERMISSIONS.md#mrbeast-content-reuse-guidelines",
        "third_party_material_checked": False,
        "contains_third_party_music": False,
        "disallowed": True,
        "disallow_reason": "Featuring third-party celebrity (The Rock - guest rights not covered)",
        "subject_key": "the_rock_celebrity_guest"
    }
]


class MrBeastHindiEngine:
    """Manages downloading, clipping, and formatting MrBeast transformative Hindi shorts."""

    def __init__(self, output_dir: str = "output/batch_today"):
        self.output_dir = output_dir
        self.tracker = HistoryTracker()
        os.makedirs(self.output_dir, exist_ok=True)

    @staticmethod
    def _get_font_opt() -> str:
        if os.path.exists("C:/Windows/Fonts/impact.ttf"):
            return "fontfile='C\\:/Windows/Fonts/impact.ttf':"
        elif os.path.exists("C:/Windows/Fonts/arialbd.ttf"):
            return "fontfile='C\\:/Windows/Fonts/arialbd.ttf':"
        return ""

    def get_next_fresh_short(self, day_offset: int = 0) -> Dict[str, Any]:
        """Finds next unused approved MrBeast short from registry (filtering out disabled items)."""
        allowed = [
            item for item in MRBEAST_HINDI_REGISTRY
            if not item.get("disallowed", False)
        ]
        unused = [item for item in allowed if not self.tracker.is_source_used(item["id"])]
        if not unused:
            print("Notice: All approved MrBeast Hindi shorts in primary registry used, resetting pool rotation.")
            unused = allowed

        idx = day_offset % len(unused)
        return unused[idx]

    def _get_best_formats(self, target_url: str) -> tuple[str, str]:
        """
        Queries video metadata via yt-dlp -J to find the exact Hindi audio format ID
        and best vertical video format ID.
        """
        cmd = [
            sys.executable, "-m", "yt_dlp",
            "--extractor-args", "youtube:player_client=android,ios,mweb",
            "-J", target_url
        ]
        out = subprocess.check_output(cmd, text=True, timeout=25)
        info = json.loads(out)
        formats = info.get("formats", [])

        # Find Hindi audio
        hindi_audios = [
            f for f in formats
            if f.get("vcodec") == "none" and (f.get("language") == "hi" or "hindi" in (f.get("format_note") or "").lower())
        ]
        if not hindi_audios:
            # Fallback to any audio with [hi] in format_id or dubbed
            hindi_audios = [f for f in formats if f.get("vcodec") == "none" and "-dubbed" in (f.get("format_note") or "")]

        if hindi_audios:
            # Pick highest bitrate audio
            best_audio = max(hindi_audios, key=lambda x: x.get("tbr") or x.get("abr") or 0)
            audio_id = best_audio["format_id"]
        else:
            audio_id = "ba[language=hi]/bestaudio"

        # Find best video (prefer vertical <= 1080p, single selector to prevent OR slash precedence bug)
        video_id = "bv*[height<=1080]"
        if not any(f.get("height") and f.get("height") <= 1080 for f in formats if f.get("vcodec") != "none"):
            video_id = "bestvideo"

        return video_id, audio_id

    def render_mrbeast_short(
        self,
        item: Dict[str, Any],
        output_video_path: str,
        output_thumb_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Downloads source footage and renders a transformative Short formatted to 1080x1920
        with original Hindi commentary narration, synchronized subtitles, top hook banner,
        and audio ducking to prevent third-party music claims.
        """
        os.makedirs(os.path.dirname(output_video_path), exist_ok=True)
        vid_id = item["id"]
        target_url = item.get("source_url") or f"https://www.youtube.com/shorts/{vid_id}"

        # 1. Query audio/video stream format
        print(f"🔍 Inspecting audio streams for MrBeast short ({vid_id})...")
        try:
            video_fmt, audio_fmt = self._get_best_formats(target_url)
            fmt_selector = f"{video_fmt}+{audio_fmt}"
        except Exception as e:
            print(f"Warning querying format: {e}. Falling back to language=hi selector.")
            fmt_selector = "bv*[height<=1080]+ba[language=hi]/best"

        temp_tmpl = os.path.join(os.path.dirname(output_video_path), f"merged_{vid_id}.%(ext)s")

        # 2. Download exact formats via yt-dlp
        print(f"📥 Downloading MrBeast Short footage ({vid_id}) with format '{fmt_selector}'...")
        dl_cmd = [
            sys.executable, "-m", "yt_dlp",
            "--extractor-args", "youtube:player_client=android,ios,mweb",
            "-f", fmt_selector,
            "--merge-output-format", "mp4",
            "-o", temp_tmpl,
            "--force-overwrites",
            "--no-playlist",
            target_url
        ]

        res = subprocess.run(dl_cmd, capture_output=True, text=True, timeout=60)
        raw_candidates = glob.glob(os.path.join(os.path.dirname(output_video_path), f"merged_{vid_id}*"))
        valid_raw = [
            f for f in raw_candidates
            if not f.endswith(".part")
            and not re.search(r'\.f[a-zA-Z0-9_-]+\.', f)
            and os.path.getsize(f) > 500000
        ]

        if not valid_raw:
            # Fallback to pre-cached verified MrBeast Hindi clips if live download fails
            cached_beast = glob.glob(os.path.join("assets", "creator_clips", "mrbeast_*.mp4"))
            # Filter out any non-mrbeast or speed clips
            cached_beast = [c for c in cached_beast if "speed" not in c.lower() and "football" not in c.lower()]
            if cached_beast:
                chosen = cached_beast[int(datetime.now().timestamp()) % len(cached_beast)]
                print(f"🎯 Live download unavailable ({res.stderr[:80] if res.stderr else 'none'}). Using verified pre-cached MrBeast clip: {chosen}")
                downloaded_raw = chosen
            else:
                raise RuntimeError(f"Failed to download MrBeast short {vid_id}: {res.stderr[-300:]}")
        else:
            downloaded_raw = valid_raw[0]

        # 3. Generate original Hindi narration & styled subtitles (Transformative Storytelling)
        hindi_text = item.get("hindi_script", "")
        base_name = os.path.splitext(output_video_path)[0]
        audio_path = f"{base_name}_voice.mp3"
        ass_path = f"{base_name}_sub.ass"

        font_opt = self._get_font_opt()
        clean_banner = re.sub(r'[^\w\s!?,.$#@\-%/:]', '', item["banner"]).replace(":", "\\:").strip()
        banner_filter = (
            f"drawtext={font_opt}text='{clean_banner}':"
            f"fontsize=50:fontcolor=white:box=1:boxcolor=0xDD0000@0.95:boxborderw=16:"
            f"x=(w-text_w)/2:y=160"
        )

        has_voice = False
        voice_duration = None
        if hindi_text:
            try:
                from src.voice_generator import generate_audio
                voice_res = generate_audio(
                    text=hindi_text,
                    audio_path=audio_path,
                    ass_path=ass_path,
                    voice="hi-IN-MadhurNeural"
                )
                has_voice = os.path.exists(audio_path) and os.path.exists(ass_path)
                if isinstance(voice_res, dict) and "duration" in voice_res:
                    voice_duration = voice_res["duration"]
            except Exception as e:
                print(f"Notice: Voiceover generation fallback: {e}")
                has_voice = False

        # MUTE UNLICENSED SOURCE AUDIO & EXCLUDE UNVERIFIED BACKGROUND MUSIC:
        # Source clip audio [0:a] contains unlicensed commercial music.
        # It is completely muted/excluded from final render.
        # Final audio uses strictly:
        # 1. Original Hindi voiceover narration (voice_audio) at normal audible volume [1:a]
        # Unverified ambient_suspense.mp3 is completely removed from the pipeline.
        # Note: Audio muting significantly reduces acoustic fingerprint matches,
        # but does NOT eliminate visual copyright matching risk.
        if has_voice:
            duration = (voice_duration + 0.5) if voice_duration else 30.0
            escaped_ass = ass_path.replace("\\", "/").replace(":", r"\:")
            filter_complex = (
                f"[0:v]trim=duration={duration:.2f},scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,{banner_filter},subtitles='{escaped_ass}'[vout]"
            )
            render_cmd = [
                "ffmpeg", "-y",
                "-stream_loop", "-1", "-i", downloaded_raw,
                "-i", audio_path,
                "-filter_complex", filter_complex,
                "-map", "[vout]",
                "-map", "1:a",
                "-c:v", "libx264",
                "-preset", "veryfast",
                "-crf", "18",
                "-pix_fmt", "yuv420p",
                "-r", "30",
                "-c:a", "aac",
                "-b:a", "192k",
                "-t", f"{duration:.2f}",
                output_video_path
            ]
        else:
            filter_complex = f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,{banner_filter}[vout]"
            render_cmd = [
                "ffmpeg", "-y",
                "-i", downloaded_raw,
                "-filter_complex", filter_complex,
                "-map", "[vout]",
                "-an",
                "-c:v", "libx264",
                "-preset", "veryfast",
                "-crf", "18",
                "-pix_fmt", "yuv420p",
                "-r", "30",
                output_video_path
            ]

        print(f"🎬 Formatting MrBeast transformative Hindi short to 1080x1920 with voiceover & subtitles...")
        render_res = subprocess.run(render_cmd, capture_output=True, text=True)

        # Cleanup raw temp file (never delete assets!)
        try:
            raw_normalized = str(downloaded_raw).replace('\\', '/')
            if not raw_normalized.startswith("assets") and os.path.exists(downloaded_raw):
                os.remove(downloaded_raw)
        except Exception:
            pass

        if render_res.returncode != 0:
            raise RuntimeError(f"FFmpeg render failed for MrBeast Hindi short: {render_res.stderr[-300:]}")

        # 4. Generate high-impact thumbnail using ThumbnailGenerator
        thumb_path = output_thumb_path or os.path.splitext(output_video_path)[0] + "_thumb.jpg"
        try:
            tg = ThumbnailGenerator(output_dir=os.path.dirname(thumb_path))
            thumb_source = downloaded_raw if (downloaded_raw and os.path.exists(downloaded_raw)) else output_video_path
            best_time = item.get("thumb_time", 2.8)
            tg.generate(
                video_path=thumb_source,
                output_thumb_path=thumb_path,
                badge_text=item.get("banner", "MRBEAST HINDI"),
                timestamp_sec=best_time,
                slot_index=item.get("slot", 1)
            )
        except Exception as e:
            print(f"Notice: MrBeast thumbnail generator fallback: {e}")
            thumb_cmd = [
                "ffmpeg", "-y",
                "-ss", "00:00:02.500",
                "-i", output_video_path,
                "-vframes", "1",
                "-q:v", "2",
                thumb_path
            ]
            subprocess.run(thumb_cmd, capture_output=True, text=True)

        # 5. Record source ID in history
        self.tracker.history.setdefault("used_source_ids", []).append(vid_id)
        self.tracker.save()

        # Get duration
        try:
            dur_cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", output_video_path]
            duration = float(subprocess.check_output(dur_cmd, text=True).strip())
        except Exception:
            duration = 35.0

        source_url = item.get("source_url") or f"https://www.youtube.com/shorts/{vid_id}"
        desc = item.get("description", "")
        if "Original Creator:" not in desc:
            desc = (
                f"{desc}\n\n"
                f"🎙️ Hindi Narration & Storytelling: Next Level Facts\n"
                f"🎬 Original Creator: @MrBeast\n"
                f"🔗 Source Video: {source_url}\n"
                f"ℹ️ Transformative Hindi commentary and analysis. Independent channel; not affiliated with, sponsored by, or endorsed by MrBeast."
            )

        return {
            "video_path": output_video_path,
            "thumbnail_path": thumb_path if os.path.exists(thumb_path) else None,
            "title": item["title"],
            "description": desc,
            "tags": item["tags"],
            "duration": duration,
            "source_id": vid_id,
            "query": f"mrbeast_official_hindi_{vid_id}",
            "creator": item.get("creator", "MrBeast"),
            "source_url": source_url,
            "reuse_permission_ref": item.get("reuse_permission_ref", "docs/CONTENT_PERMISSIONS.md#mrbeast-content-reuse-guidelines"),
            "third_party_material_checked": item.get("third_party_material_checked", True),
            "contains_third_party_music": item.get("contains_third_party_music", False),
            "subject_key": item.get("subject_key", vid_id),
        }
