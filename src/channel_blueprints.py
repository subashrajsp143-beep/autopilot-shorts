"""
Channel Blueprints & Dynamic Daily Rotation Matrix
---------------------------------------------------
Defines distinct, rotating content blueprints for all 3 channels:
- Channel 3: Sports, Football (Ronaldo/Messi) & IShowSpeed Viral Moments (Hindi Commentary)
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
# CHANNEL 3: Next Level Facts (Star Channel - 54k+ Views)
# Rotating pools across Football, Speed, and Cricket moments
# ==============================================================================
CHANNEL_3_POOL: List[Dict[str, Any]] = [
    # Pool A: Ronaldo & Speed
    {
        "clip": "assets/creator_clips/football_01_ronaldo_bicycle.mp4",
        "title": "जब Ronaldo ने बनाया IMPOSSIBLE Goal! 😱 CR7 BICYCLE #Shorts",
        "banner": "RONALDO IMPOSSIBLE BICYCLE KICK! 🚲🐐",
        "description": "फुटबॉल इतिहास का सबसे नामुमकिन गोल! हवा में 8 फीट ऊपर उछलकर रोनाल्डो ने सबको हैरान कर दिया।\n\n#Shorts #Ronaldo #BicycleKick #FootballViral #CR7",
        "tags": ["ronaldo", "cr7 bicycle kick", "football shorts", "viral shorts", "cr7 goat"],
        "hindi_script": "रोनाल्डो का यह बाइसिकल किक गोल देखकर विरोधी टीम के फैंस भी खड़े होकर तालियां बजाने लगे! जब हवा में करीब आठ फीट ऊपर उछलकर रोनाल्डो ने यह नामुमकिन गोल दागा, तो साइंस भी हैरान रह गई!"
    },
    {
        "clip": "assets/creator_clips/speed_01_dude_perfect.mp4",
        "title": "Speed का सबसे CRAZY शॉट! 😱 ISHOWSPEED BASKETBALL #Shorts",
        "banner": "SPEED IMPOSSIBLE BASKETBALL SHOT! 🏀🔥",
        "description": "स्पीड और ड्यूट परफेक्ट का सबसे ऐतिहासिक और फनी मोमेंट!\n\n#Shorts #IShowSpeed #DudePerfect #TrickShot #Viral",
        "tags": ["ishowspeed", "speed trick shot", "dude perfect", "shorts", "viral"],
        "hindi_script": "स्पीड ने जब पहली बार यह नामुमकिन बास्केटबॉल शॉट मारा, तो वहां मौजूद कोई भी अपनी आंखों पर यकीन नहीं कर पाया! स्पीड की खुशी और रिएक्शन देखकर आपका दिन बन जाएगा!"
    },
    {
        "clip": "assets/creator_clips/football_02_ronaldo_freekick.mp4",
        "title": "Ronaldo का 40 गज का Free-Kick! 🚀⚽ CR7 KNUCKLEBALL #Shorts",
        "banner": "RONALDO 40-YARD KNUCKLEBALL! 🚀⚽",
        "description": "रोनाल्डो का नकल-बॉल फ्रीकिक जो हवा में सांप की तरह मुड़ गया!\n\n#Shorts #Ronaldo #FreeKick #Knuckleball #CR7",
        "tags": ["ronaldo freekick", "cr7 knuckleball", "football goals", "shorts", "viral"],
        "hindi_script": "रोनाल्डो का यह 40 गज का फ्रीकिक देखकर गोलकीपर सिर्फ देखता ही रह गया! 100 किलोमीटर प्रति घंटे से ज्यादा की रफ्तार से गेंद हवा में लहराती हुई सीधे गोल में जा घुसी!"
    },
    {
        "clip": "assets/creator_clips/speed_02_backflips.mp4",
        "title": "Speed का सबसे पागलपन भरा स्टंट! 😂🔥 ISHOWSPEED BACKFLIP #Shorts",
        "banner": "SPEED CRAZY BACKFLIP STUNT! 😂🔥",
        "description": "स्पीड ने लाइव स्ट्रीम पर लगाया ऐसा बैकफ्लिप कि पूरा इंटरनेट हंस पड़ा!\n\n#Shorts #Speed #Backflip #FunnyStream #IShowSpeed",
        "tags": ["speed backflip", "ishowspeed funny", "stream moments", "shorts", "viral"],
        "hindi_script": "स्पीड ने जब लाइव स्ट्रीम पर बैकफ्लिप लगाने की कोशिश की तो जो हुआ उसने इंटरनेट को हिला कर रख दिया! स्पीड की यही दीवानगी उसे दुनिया का सबसे वायरल स्ट्रीमर बनाती है!"
    },
    {
        "clip": "assets/creator_clips/football_03_ronaldo_juventus.mp4",
        "title": "जब Ronaldo ने Gravity को किया फेल! ✈️🐐 CR7 SUPER JUMP #Shorts",
        "banner": "RONALDO FLIES IN THE AIR! ✈️🐐",
        "description": "रोनाल्डो ने ग्रैविटी को किया फेल! 2.56 मीटर की ऊंचाई पर डेढ़ सेकंड तक हवा में रुके रहे।\n\n#Shorts #Ronaldo #GravityDefying #CR7 #FootballViral",
        "tags": ["ronaldo jump", "cr7 header", "gravity defying", "shorts", "viral"],
        "hindi_script": "जब रोनाल्डो ने यह हेडर गोल दागा, तो वे हवा में करीब डेढ़ सेकंड तक लटके रहे! इस छलांग की ऊंचाई एक बास्केटबॉल हूप से भी ऊंची थी। इसीलिए रोनाल्डो को एलियन कहा जाता है!"
    },
    {
        "clip": "assets/creator_clips/speed_03_silence_challenge.mp4",
        "title": "Speed 1 मिनट भी शांत नहीं रह पाया! 😭⚡ ISHOWSPEED FUNNY #Shorts",
        "banner": "CAN SPEED STAY SILENT FOR 1 MINUTE? 😭⚡",
        "description": "स्पीड का सबसे पागलपन भरा चैलेंज जिसमें वह 10 सेकंड भी शांत नहीं रह पाया!\n\n#Shorts #Speed #SilenceChallenge #IShowSpeedRage #Viral",
        "tags": ["speed silence", "ishowspeed rage", "speed funny moments", "shorts", "viral"],
        "hindi_script": "स्पीड को एक कमरे में सिर्फ एक मिनट शांत रहने की चुनौती दी गई! लेकिन स्पीड से दस सेकंड भी चुप नहीं रहा गया और उसने जो चीख मारी, उसने सबका सिर हिला दिया!"
    },
    {
        "clip": "assets/creator_clips/football_04_impossible_clearance.mp4",
        "title": "Football का सबसे हैरतअंगेज Save! 😱🧤 IMPOSSIBLE DEFENCE #Shorts",
        "banner": "IMPOSSIBLE GOAL-LINE CLEARANCE! 🧤🔥",
        "description": "फुटबॉल का सबसे हैरतअंगेज सेव! जब 99% निश्चित गोल को डिफेंडर ने हवा में उड़कर रोक लिया।\n\n#Shorts #GoalLineClearance #BestSaves #Football #Viral",
        "tags": ["impossible saves", "goal line clearance", "football defence", "shorts", "viral"],
        "hindi_script": "जब गेंद गोल लाइन पार करने ही वाली थी, तभी इस डिफेंडर ने हवा में उड़कर ऐसा अविश्वसनीय सेव किया कि पूरा स्टेडियम हैरान रह गया! इसे कहते हैं आखिरी सांस तक लड़ना!"
    },
    {
        "clip": "assets/creator_clips/speed_04_iphone_duo.mp4",
        "title": "Speed का नया iPhone Unboxing मोमेंट! 😂📱 ISHOWSPEED FUNNY #Shorts",
        "banner": "SPEED UNBOXING IPHONE GONE WRONG! 😂📱",
        "description": "स्पीड का आईफोन अनबॉक्सिंग जो पूरी तरह फनी आपदा बन गया!\n\n#Shorts #IShowSpeed #iPhone #FunnyUnboxing #Viral",
        "tags": ["speed iphone", "ishowspeed funny", "unboxing gone wrong", "shorts", "viral"],
        "hindi_script": "स्पीड ने जैसे ही यह नया आईफोन खोला, उसकी एक्साइटमेंट इतनी बढ़ गई कि उसने फोन को ही हवा में उछाल दिया! स्पीड के इन फनी मोमेंट्स का कोई मुकाबला नहीं है!"
    },
    {
        "clip": "assets/creator_clips/football_01_ronaldo_bicycle.mp4",
        "title": "Zidane Shocked Reaction To Ronaldo Goal! 🤯🐐 CR7 GOAT #Shorts",
        "banner": "ZIDANE REACTION TO RONALDO GOAL! 🤯🐐",
        "description": "जब कोच जिदान ने रोनाल्डो का गोल देखकर अपना सिर पकड़ लिया!\n\n#Shorts #Ronaldo #Zidane #ChampionsLeague #CR7",
        "tags": ["ronaldo zidane", "cr7 goat", "champions league", "shorts", "viral"],
        "hindi_script": "रोनाल्डो का यह गोल देखकर खुद महान कोच जिनेदिन जिदान ने अपना सिर पकड़ लिया! उन्हें यकीन ही नहीं हुआ कि कोई इंसान फुटबॉल मैदान पर ऐसा करिश्मा भी कर सकता है!"
    },
    {
        "clip": "assets/creator_clips/speed_02_backflips.mp4",
        "title": "Speed का 10M Celebration पागलपन! 🦁🔥 ISHOWSPEED 10 MILLION #Shorts",
        "banner": "SPEED 10M CELEBRATION CRAZINESS! 🦁🔥",
        "description": "स्पीड का सबसे एनर्जेटिक और अनफिल्टर्ड मोमेंट!\n\n#Shorts #IShowSpeed #Celebration #ViralStream #Shorts",
        "tags": ["speed celebration", "ishowspeed 10m", "viral streamer", "shorts", "cr7"],
        "hindi_script": "स्पीड का यह सेलिब्रेशन देखकर आप भी अपनी हंसी नहीं रोक पाएंगे! बिना किसी स्क्रिप्ट के स्पीड की यह असली एनर्जी ही उसे दुनिया का सबसे बड़ा स्ट्रीमर बनाती है!"
    },

    # Pool B: Day 2 Variations
    {
        "clip": "assets/creator_clips/football_02_ronaldo_freekick.mp4",
        "title": "जब रोनाल्डो ने हवा में उड़ती हुई बॉल को रोक दिया! ⚽🔥 #Shorts #CR7Magic",
        "banner": "RONALDO'S GREATEST FREEKICK ANGLE! ⚽🔥",
        "description": "रोनाल्डो का ऐसा जादू जो कोई दूसरा खिलाड़ी कभी दोहरा नहीं पाया!\n\n#Shorts #CR7 #FreeKick #FootballSkills",
        "tags": ["ronaldo", "cr7 skills", "football", "shorts", "viral"],
        "hindi_script": "फुटबॉल के मैदान पर रोनाल्डो जब भी फ्रीकिक लेने खड़े होते हैं, तो विरोधी गोलकीपर की धड़कनें तेज हो जाती हैं! हवा में गेंद ऐसे घूमती है जैसे कोई रिमोट से कंट्रोल कर रहा हो!"
    },
    {
        "clip": "assets/creator_clips/speed_03_silence_challenge.mp4",
        "title": "स्पीड की सबसे फनी चीख जिसने माइक्रोफोन ही उड़ा दिया! 😭⚡ #Shorts #IShowSpeed",
        "banner": "SPEED'S FUNNIEST SCREAM EVER! 😭⚡",
        "description": "स्पीड का अनकंट्रोल्ड रिएक्शन जिसने पूरे कमरे को हिला दिया!\n\n#Shorts #Speed #FunnyMoments #IShowSpeed",
        "tags": ["speed scream", "ishowspeed rage", "shorts", "viral"],
        "hindi_script": "स्पीड जब भी ज्यादा एक्साइटेड होता है, तो उसका रिएक्शन ऐसा होता है जिसे देखकर कोई भी अपनी हंसी नहीं रोक सकता! इंटरनेट पर स्पीड जैसा दूसरा कोई नहीं है!"
    },
    {
        "clip": "assets/creator_clips/football_03_ronaldo_juventus.mp4",
        "title": "जब साइंस ने नापी रोनाल्डो की छलांग, तो वैज्ञानिक हैरान रह गए! ✈️🐐 #Shorts #CR7Physics",
        "banner": "SCIENCE PROVES RONALDO IS ALIEN! ✈️🐐",
        "description": "रोनाल्डो की जंप का ऐसा विश्लेषण जिसने सबको दंग कर दिया!\n\n#Shorts #RonaldoJump #ScienceFacts #CR7",
        "tags": ["ronaldo jump", "cr7 science", "physics", "shorts", "viral"],
        "hindi_script": "वैज्ञानिकों के अनुसार रोनाल्डो जब कूदते हैं तो उनके पैरों पर पांच जी का दबाव पड़ता है, जो एक लड़ाकू विमान के पायलट के बराबर है! इसी ताकत की वजह से रोनाल्डो ग्रैविटी को हरा देते हैं!"
    },
    {
        "clip": "assets/creator_clips/speed_01_dude_perfect.mp4",
        "title": "स्पीड ने ड्यूड परफेक्ट को जब खुली चुनौती दी! 😱🔥 #Shorts #DudePerfect",
        "banner": "SPEED CHALLENGES DUDE PERFECT! 😱🔥",
        "description": "स्पीड का सबसे रोमांचक ट्रिक शॉट मुकाबला!\n\n#Shorts #Speed #DudePerfect #TrickShot",
        "tags": ["speed dude perfect", "trick shot", "shorts", "viral"],
        "hindi_script": "जब स्पीड ने ड्यूड परफेक्ट की टीम को उन्हीं के खेल में चुनौती दी, तो किसी को उम्मीद नहीं थी कि स्पीड इतना सटीक शॉट लगा देगा! इसे कहते हैं छुपा रुस्तम!"
    },
    {
        "clip": "assets/creator_clips/football_04_impossible_clearance.mp4",
        "title": "फुटबॉल इतिहास का वो सेव जो हार को जीत में बदल गया! 😱🧤 #Shorts #BestClearance",
        "banner": "SAVE OF THE CENTURY! 🧤🔥",
        "description": "जब पूरी टीम ने उम्मीद छोड़ दी थी, तब इस खिलाड़ी ने नामुमकिन कर दिखाया!\n\n#Shorts #Football #BestSave #MiracleGoal",
        "tags": ["football save", "miracle", "shorts", "viral"],
        "hindi_script": "यह सेव सिर्फ एक गेंद को रोकना नहीं था, बल्कि अपनी टीम के लिए दिल और जान से लड़ने का सबूत था! फुटबॉल की खूबसूरती इसी जज्बे में छुपी है!"
    }
]


# ==============================================================================
# CHANNEL 2: Pawsome Productions
# Rotating pools across Satisfying Science, 100-Ton Press & Guinness Records
# ==============================================================================
CHANNEL_2_POOL: List[Dict[str, Any]] = [
    # Pool A: Day 1
    {
        "clip": "assets/creator_clips/science_01_helmet_press.mp4",
        "title": "100 टन हाइड्रोलिक प्रेस बनाम मजबूत हेलमेट! 😱🔨 #Shorts #HydraulicPress #Satisfying",
        "banner": "100-TON PRESS VS CRASH HELMET! 🔨💥",
        "description": "क्या एक मजबूत हेलमेट 100 टन के हाइड्रोलिक प्रेस का दबाव झेल पाएगा?\n\n#Shorts #HydraulicPress #Crushing #Satisfying #Viral",
        "tags": ["hydraulic press", "helmet crushing", "satisfying videos", "shorts", "viral"],
        "hindi_script": "जब इस 100 टन के शक्तिशाली हाइड्रोलिक प्रेस के नीचे इस मजबूत हेलमेट को रखा गया, तो देखिए कैसे सेकंडों में यह चूर-चूर हो गया! हाइड्रोलिक प्रेस की ताकत का कोई मुकाबला नहीं है!"
    },
    {
        "clip": "assets/creator_clips/records_01_table_tennis.mp4",
        "title": "टेबल टेनिस का ऐसा नामुमकिन शॉट जिसे देखकर आंखें खुली रह जाएं! 😱🏓 #Shorts #WorldRecord",
        "banner": "IMPOSSIBLE PING PONG TRICKSHOT! 🏓🔥",
        "description": "गिनीज वर्ल्ड रिकॉर्ड लेवल का सबसे हैरान कर देने वाला टेबल टेनिस ट्रिक शॉट!\n\n#Shorts #PingPong #TrickShot #WorldRecord #Viral",
        "tags": ["ping pong trick shot", "table tennis", "world record", "shorts", "viral"],
        "hindi_script": "टेबल टेनिस का यह शॉट देखकर आप भी अपनी आंखों पर यकीन नहीं करेंगे! इतनी दूरी और सटीकता से यह शॉट लगाना इंसानी क्षमता से परे लगता है। इसे कहते हैं असली परफेक्शन!"
    },
    {
        "clip": "assets/creator_clips/science_03_cards_press.mp4",
        "title": "हाइड्रोलिक प्रेस बनाम ताश के पत्तों की गड्डी! 💥🃏 #Shorts #HydraulicPress",
        "banner": "HYDRAULIC PRESS VS PLAYING CARDS! 🃏💥",
        "description": "जब 100 टन के प्रेस ने 52 ताश के पत्तों को दबाया तो क्या हुआ?\n\n#Shorts #HydraulicPress #CardsCrushing #SatisfyingShorts",
        "tags": ["hydraulic press", "playing cards", "satisfying", "shorts", "viral"],
        "hindi_script": "ताश के पत्तों की गड्डी पर जब 100 टन का दबाव डाला गया, तो पत्ते ऐसे फूटे जैसे कोई छोटा धमाका हुआ हो! यह वीडियो देखने में बेहद सुकून देने वाला और संतोषजनक है!"
    },
    {
        "clip": "assets/creator_clips/records_02_levitation_handstand.mp4",
        "title": "गुरुत्वाकर्षण को चुनौती देने वाला नामुमकिन हैंडस्टैंड स्टंट! 🤯🤸 #Shorts #HumanStunts",
        "banner": "GRAVITY DEFYING HANDSTAND! 🤸⚡",
        "description": "इस लड़के ने फिजिक्स के नियमों को पूरी तरह गलत साबित कर दिया!\n\n#Shorts #Handstand #Calisthenics #BodyPower #Viral",
        "tags": ["calisthenics", "gravity defying", "handstand stunt", "shorts", "viral"],
        "hindi_script": "इस लड़के के शरीर का संतुलन देखकर वैज्ञानिक भी हैरान हैं! हवा में सिर्फ उंगलियों के बल पर पूरे शरीर को साध लेना, यह साबित करता है कि इंसान अभ्यास से कुछ भी कर सकता है!"
    },
    {
        "clip": "assets/creator_clips/science_04_solar_panel.mp4",
        "title": "हाइड्रोलिक प्रेस बनाम सोलर पैनल का भयानक क्रंच! ☀️💥 #Shorts #HydraulicPress",
        "banner": "HYDRAULIC PRESS VS SOLAR PANEL! ☀️💥",
        "description": "जब सोलर पैनल पर पड़ा 100 टन का हाइड्रोलिक वजन!\n\n#Shorts #SolarPanel #HydraulicPress #ScienceExperiments",
        "tags": ["solar panel crush", "hydraulic press", "science shorts", "shorts", "viral"],
        "hindi_script": "जब इस सिलिकॉन सोलर पैनल पर हाइड्रोलिक प्रेस का दबाव पड़ा, तो कांच के हजारों टुकड़े चमकते हुए बिखर गए! यह क्रंच देखने में बेहद संतोषजनक और अद्भुत है!"
    },
    {
        "clip": "assets/creator_clips/records_03_juggling_sword.mp4",
        "title": "आंखों पर पट्टी बांधकर तलवारों से करतब! 😱🗡️ #Shorts #GuinnessRecord",
        "banner": "EXTREME BLINDFOLD SWORD STUNT! 🗡️⚠️",
        "description": "मौत को छूकर वापस आने वाला सबसे खतरनाक स्टंट!\n\n#Shorts #SwordStunt #DangerousRecords #WorldRecord #Viral",
        "tags": ["sword stunt", "guinness record", "extreme stunt", "shorts", "viral"],
        "hindi_script": "जरा सी भी चूक और सीधे जान का खतरा! आंखों पर काली पट्टी बांधकर इन धारदार तलवारों को हवा में उछालना मौत से खेलने जैसा है। इस स्टंटबाज के साहस को सलाम है!"
    },
    {
        "clip": "assets/creator_clips/science_02_prettiest_crunch.mp4",
        "title": "इंटरनेट का सबसे खूबसूरत और संतोषजनक क्रंच! 😍✨ #Shorts #OddlySatisfying",
        "banner": "MOST SATISFYING CRUNCH EVER! 😍✨",
        "description": "इसे देखकर आपका सारा स्ट्रेस चुटकियों में गायब हो जाएगा!\n\n#Shorts #Satisfying #StressRelief #HydraulicPress #Viral",
        "tags": ["oddly satisfying", "crunch", "stress relief", "shorts", "viral"],
        "hindi_script": "अगर आप दिनभर की थकान से परेशान हैं, तो इस वीडियो को पूरे ध्यान से देखिए! यह क्रंच इतना संतोषजनक है कि आपका सारा तनाव सेकंडों में दूर हो जाएगा!"
    },
    {
        "clip": "assets/creator_clips/records_04_human_catapult.mp4",
        "title": "इंसान को गुलेल की तरह हवा में 100 फीट ऊपर फेंक दिया! 😱🚀 #Shorts #HumanCatapult",
        "banner": "100FT HUMAN CATAPULT LAUNCH! 🚀😱",
        "description": "दुनिया का सबसे रोंगटे खड़े कर देने वाला एक्सट्रीम एडवेंचर स्टंट!\n\n#Shorts #HumanCatapult #ExtremeStunts #Adrenaline #Viral",
        "tags": ["human catapult", "extreme sports", "insane stunt", "shorts", "viral"],
        "hindi_script": "जब इस विशालकाय कैटापुल्ट ने इस इंसान को 100 फीट ऊपर हवा में उछाला, तो जमीन पर खड़े लोगों की सांसें थम गईं! कमजोर दिल वाले इस स्टंट को बिल्कुल न देखें!"
    },
    {
        "clip": "assets/creator_clips/science_01_helmet_press.mp4",
        "title": "क्या हेलमेट 50,000 किलो का वजन रोक पाया? 😱🔨 #Shorts #SafetyTest",
        "banner": "CAN A HELMET SURVIVE 50,000 KG? 🔨⚠️",
        "description": "बाइक हेलमेट की असली मजबूती का सबसे कड़ा टेस्ट!\n\n#Shorts #HelmetTest #HydraulicPress #SafetyFirst #Viral",
        "tags": ["helmet test", "hydraulic press test", "satisfying science", "shorts", "viral"],
        "hindi_script": "आपकी सुरक्षा करने वाला हेलमेट असल में कितना मजबूत होता है? इस 100 टन प्रेस टेस्ट ने दिखा दिया कि अच्छी क्वालिटी का हेलमेट किस हद तक आपकी जान बचा सकता है!"
    },
    {
        "clip": "assets/creator_clips/records_02_levitation_handstand.mp4",
        "title": "इस लड़के ने जमीन से हाथ उठाकर सबको चौंका दिया! 😱🤸 #Shorts #ImpossibleBalance",
        "banner": "ONE-ARM IMPOSSIBLE BALANCE! 🤸🔥",
        "description": "ताकत और एकाग्रता का सबसे बेमिसाल नमूना!\n\n#Shorts #CalisthenicsPower #HumanFeats #ViralShorts",
        "tags": ["impossible balance", "one arm handstand", "fitness motivation", "shorts", "viral"],
        "hindi_script": "कड़ी मेहनत और अटूट एकाग्रता से इंसान क्या नहीं कर सकता! इस एक हाथ के बैलेंस ने दुनिया भर के फिटनेस एक्सपर्ट्स को हैरान कर दिया है!"
    },

    # Pool B: Day 2 Variations
    {
        "clip": "assets/creator_clips/science_02_prettiest_crunch.mp4",
        "title": "दिन का सबसे संतोषजनक स्लो-मोशन क्रंच! 💆✨ #Shorts #SatisfyingVideo",
        "banner": "SLOW MOTION SATISFYING CRUNCH! 💆✨",
        "description": "इस वीडियो को हेडफोन लगाकर सुनें, गजब का सुकून मिलेगा!\n\n#Shorts #SlowMo #Crunch #ASMR #Satisfying",
        "tags": ["slow motion", "satisfying crunch", "asmr", "shorts", "viral"],
        "hindi_script": "धीमी गति में इस वस्तु का टूटना देखना दिमाग को एक अनोखा सुकून देता है। विज्ञान कहता है कि ऐसे संतोषजनक वीडियो देखने से दिमाग का तनाव कम होता है!"
    },
    {
        "clip": "assets/creator_clips/records_01_table_tennis.mp4",
        "title": "100 में से 99 लोग यह पिंग पॉन्ग शॉट मिस कर देंगे! 🏓🔥 #Shorts #NextLevel",
        "banner": "CAN YOU MAKE THIS PING PONG SHOT? 🏓🔥",
        "description": "इतनी छोटी गेंद पर इतना सटीक नियंत्रण, अविश्वसनीय!\n\n#Shorts #Trickshot #PingPong #NextLevel",
        "tags": ["trickshot", "ping pong", "impossible", "shorts", "viral"],
        "hindi_script": "अगर आपको लगता है कि आप टेबल टेनिस में अच्छे हैं, तो इस शॉट को देखिए! हवा के दबाव और स्पिन को मापकर यह शॉट लगाना किसी जादू से कम नहीं है!"
    },
    {
        "clip": "assets/creator_clips/science_03_cards_press.mp4",
        "title": "जब 52 ताश के पत्तों पर 100 टन का वजन पड़ा! 🃏💥 #Shorts #CardPress",
        "banner": "52 CARDS VS 100-TON PRESS! 🃏💥",
        "description": "ताश के पत्तों का सबसे अनोखा हाइड्रोलिक एक्सपेरिमेंट!\n\n#Shorts #HydraulicPress #PlayingCards #Satisfying",
        "tags": ["cards", "hydraulic press", "science", "shorts", "viral"],
        "hindi_script": "कागज के पत्तों में इतनी ताकत हो सकती है कि वे कुछ पलों के लिए लोहे के प्रेस को भी रोक लें, यह देखकर हर कोई हैरान रह जाता है!"
    },
    {
        "clip": "assets/creator_clips/records_04_human_catapult.mp4",
        "title": "जब स्टंटबाज ने खुद को हवा में 10 मंजिला इमारत जितना ऊपर उड़ाया! 🚀😱 #Shorts",
        "banner": "EXTREME 10-STORY HUMAN LAUNCH! 🚀😱",
        "description": "रोंगटे खड़े कर देने वाला एड्रेनालाईन रश!\n\n#Shorts #ExtremeSports #HumanCatapult #Adrenaline",
        "tags": ["extreme sports", "catapult", "stunt", "shorts", "viral"],
        "hindi_script": "जब इंसान हवा में पंखों की तरह उड़ता है, तो दिल की धड़कनें तेज हो जाती हैं। सुरक्षा के कड़े इंतजामों के बीच यह स्टंट दुनिया का सबसे खतरनाक एडवेंचर है!"
    },
    {
        "clip": "assets/creator_clips/science_04_solar_panel.mp4",
        "title": "क्या सोलर पैनल हाइड्रोलिक प्रेस को रोक पाया? ☀️💥 #Shorts #TechExperiment",
        "banner": "SOLAR PANEL VS 100-TON HYDRAULIC! ☀️💥",
        "description": "सोलर सेल की मजबूती का सबसे रोमांचक टेस्ट!\n\n#Shorts #SolarEnergy #HydraulicPress #TechTest",
        "tags": ["solar panel", "hydraulic press", "tech test", "shorts", "viral"],
        "hindi_script": "सोलर पैनल के भीतर लगे सिलिकॉन वेफर्स जब दबाव में चटकते हैं, तो उनका पैटर्न देखना विज्ञान का एक अद्भुत नजारा पेश करता है!"
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
        # Channel 3: Super Viral Mix - 50% MrBeast Official Hindi Dubs + 50% Football/Speed
        beast_pool = [dict(x, engine="mrbeast_hindi", type="MrBeast Official Hindi Dub Short") for x in MRBEAST_HINDI_REGISTRY]
        action_pool = [dict(x, engine="action", type="Football & Speed Viral Short") for x in CHANNEL_3_POOL]

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

            a_item = dict(action_items[i])
            selected.append(a_item)

    elif channel_id == 1:
        # Channel 1: FactTechz 29 Rotating Scripts
        total_scripts = len(HINDI_VIRAL_SCRIPTS)
        start_idx = (day_offset * count) % total_scripts

        # Scene mapping
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
                title = f"{title.split('#')[0].strip()} Part {day_offset + 1} #Shorts"

            item = {
                "niche": niche,
                "scenes": scenes,
                "title": title,
                "banner": f"{niche.upper()} SECRETS! 🧠✨",
                "description": raw_script.get("description", "Watch till the end! #Shorts #HindiFacts"),
                "tags": raw_script.get("tags", ["shorts", "facts", "hindi"]),
                "hindi_script": raw_script.get("text", "")
            }
            if item not in selected:
                selected.append(item)
            if len(selected) >= count:
                break

    elif channel_id == 2:
        # Channel 2: Science & Guinness Records
        total_pool = len(CHANNEL_2_POOL)
        start_idx = (day_offset * count) % total_pool
        for i in range(total_pool):
            candidate = CHANNEL_2_POOL[(start_idx + i) % total_pool]
            title = candidate["title"]
            if tracker.is_title_used(title):
                candidate = dict(candidate)
                candidate["title"] = f"{title.split('#')[0].strip()} Part {day_offset + 1} #{title.split('#')[-1] if '#' in title else 'Shorts'}"
            if candidate not in selected:
                selected.append(dict(candidate))
            if len(selected) >= count:
                break

    # Assign 1-indexed slots
    for idx, item in enumerate(selected, 1):
        item["slot"] = idx

    return selected


# Legacy exports for backwards compatibility
CHANNEL_3_BLUEPRINTS = get_channel_blueprints(3, count=10, day_offset=0)
CHANNEL_1_BLUEPRINTS = get_channel_blueprints(1, count=10, day_offset=0)
CHANNEL_2_BLUEPRINTS = get_channel_blueprints(2, count=10, day_offset=0)
