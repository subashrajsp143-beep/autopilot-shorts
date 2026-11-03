"""
Channel Blueprints & Content Matrix
-----------------------------------
Defines distinct, non-overlapping content blueprints for all 3 channels:
- Channel 3: Sports, Football (Ronaldo/Messi) & IShowSpeed Viral Moments (Hindi Commentary)
- Channel 1: FactTechz-Style Cinematic Documentary Shorts (Dark Psychology, Ancient Mysteries, Deep Sea)
- Channel 2: Mind-Blowing Science, Hydraulic Press Crushing & Guinness World Records (Hindi Commentary)
"""

from typing import List, Dict, Any

# ==============================================================================
# CHANNEL 3: Next Level Facts (Star Channel - 54k+ Views)
# Target: Football, Speed, Sports Thrillers with High-Energy Hindi Commentary
# ==============================================================================
CHANNEL_3_BLUEPRINTS: List[Dict[str, Any]] = [
    {
        "slot": 1,
        "clip": "assets/creator_clips/football_01_ronaldo_bicycle.mp4",
        "title": "रोनाल्डो का यह बाइसिकल किक गोल देखकर विरोधी फैंस भी रो पड़े! 😱🐐 #Shorts #CR7 #Football",
        "banner": "RONALDO IMPOSSIBLE BICYCLE KICK! 🚲🐐",
        "description": "फुटबॉल इतिहास का सबसे नामुमकिन गोल! हवा में 8 फीट ऊपर उछलकर रोनाल्डो ने सबको हैरान कर दिया।\n\n#Shorts #Ronaldo #BicycleKick #FootballViral #CR7",
        "tags": ["ronaldo", "cr7 bicycle kick", "football shorts", "viral shorts", "cr7 goat"],
        "hindi_script": "रोनाल्डो का यह बाइसिकल किक गोल देखकर विरोधी टीम के फैंस भी खड़े होकर तालियां बजाने लगे! जब हवा में करीब आठ फीट ऊपर उछलकर रोनाल्डो ने यह नामुमकिन गोल दागा, तो साइंस भी हैरान रह गई!"
    },
    {
        "slot": 2,
        "clip": "assets/creator_clips/speed_01_dude_perfect.mp4",
        "title": "स्पीड ने जब पहली बार मारा नामुमकिन बास्केटबॉल शॉट! 😱🏀 #Shorts #IShowSpeed",
        "banner": "SPEED IMPOSSIBLE BASKETBALL SHOT! 🏀🔥",
        "description": "स्पीड और ड्यूट परफेक्ट का सबसे ऐतिहासिक और फनी मोमेंट!\n\n#Shorts #IShowSpeed #DudePerfect #TrickShot #Viral",
        "tags": ["ishowspeed", "speed trick shot", "dude perfect", "shorts", "viral"],
        "hindi_script": "स्पीड ने जब पहली बार यह नामुमकिन बास्केटबॉल शॉट मारा, तो वहां मौजूद कोई भी अपनी आंखों पर यकीन नहीं कर पाया! स्पीड की खुशी और रिएक्शन देखकर आपका दिन बन जाएगा!"
    },
    {
        "slot": 3,
        "clip": "assets/creator_clips/football_02_ronaldo_freekick.mp4",
        "title": "रोनाल्डो का वो 40 गज का फ्रीकिक जिसने फिजिक्स के नियम तोड़ दिए! 🚀⚽ #Shorts #Ronaldo",
        "banner": "RONALDO 40-YARD KNUCKLEBALL! 🚀⚽",
        "description": "रोनाल्डो का नकल-बॉल फ्रीकिक जो हवा में सांप की तरह मुड़ गया!\n\n#Shorts #Ronaldo #FreeKick #Knuckleball #CR7",
        "tags": ["ronaldo freekick", "cr7 knuckleball", "football goals", "shorts", "viral"],
        "hindi_script": "रोनाल्डो का यह 40 गज का फ्रीकिक देखकर गोलकीपर सिर्फ देखता ही रह गया! 100 किलोमीटर प्रति घंटे से ज्यादा की रफ्तार से गेंद हवा में लहराती हुई सीधे गोल में जा घुसी!"
    },
    {
        "slot": 4,
        "clip": "assets/creator_clips/speed_02_backflips.mp4",
        "title": "स्पीड का सबसे खतरनाक बैकफ्लिप स्टंट! 😂🔥 #Shorts #IShowSpeed #CrazyMoments",
        "banner": "SPEED CRAZY BACKFLIP STUNT! 😂🔥",
        "description": "स्पीड ने लाइव स्ट्रीम पर लगाया ऐसा बैकफ्लिप कि पूरा इंटरनेट हंस पड़ा!\n\n#Shorts #Speed #Backflip #FunnyStream #IShowSpeed",
        "tags": ["speed backflip", "ishowspeed funny", "stream moments", "shorts", "viral"],
        "hindi_script": "स्पीड ने जब लाइव स्ट्रीम पर बैकफ्लिप लगाने की कोशिश की तो जो हुआ उसने इंटरनेट को हिला कर रख दिया! स्पीड की यही दीवानगी उसे दुनिया का सबसे वायरल स्ट्रीमर बनाती है!"
    },
    {
        "slot": 5,
        "clip": "assets/creator_clips/football_03_ronaldo_juventus.mp4",
        "title": "रोनाल्डो की हवा में 2.56 मीटर ऊंची छलांग! ✈️🐐 #Shorts #CR7Header #Football",
        "banner": "RONALDO FLIES IN THE AIR! ✈️🐐",
        "description": "रोनाल्डो ने ग्रैविटी को किया फेल! 2.56 मीटर की ऊंचाई पर डेढ़ सेकंड तक हवा में रुके रहे।\n\n#Shorts #Ronaldo #GravityDefying #CR7 #FootballViral",
        "tags": ["ronaldo jump", "cr7 header", "gravity defying", "shorts", "viral"],
        "hindi_script": "जब रोनाल्डो ने यह हेडर गोल दागा, तो वे हवा में करीब डेढ़ सेकंड तक लटके रहे! इस छलांग की ऊंचाई एक बास्केटबॉल हूप से भी ऊंची थी। इसीलिए रोनाल्डो को एलियन कहा जाता है!"
    },
    {
        "slot": 6,
        "clip": "assets/creator_clips/speed_03_silence_challenge.mp4",
        "title": "स्पीड को जब कमरे में 1 मिनट शांत रहने को कहा गया! 😭⚡ #Shorts #IShowSpeed",
        "banner": "CAN SPEED STAY SILENT FOR 1 MINUTE? 😭⚡",
        "description": "स्पीड का सबसे पागलपन भरा चैलेंज जिसमें वह 10 सेकंड भी शांत नहीं रह पाया!\n\n#Shorts #Speed #SilenceChallenge #IShowSpeedRage #Viral",
        "tags": ["speed silence", "ishowspeed rage", "speed funny moments", "shorts", "viral"],
        "hindi_script": "स्पीड को एक कमरे में सिर्फ एक मिनट शांत रहने की चुनौती दी गई! लेकिन स्पीड से दस सेकंड भी चुप नहीं रहा गया और उसने जो चीख मारी, उसने सबका सिर हिला दिया!"
    },
    {
        "slot": 7,
        "clip": "assets/creator_clips/football_04_impossible_clearance.mp4",
        "title": "गोल लाइन पर डिफेंडर का ऐसा करिश्मा जिसे देखकर सब दंग रह गए! 😱🧤 #Shorts #FootballSaves",
        "banner": "IMPOSSIBLE GOAL-LINE CLEARANCE! 🧤🔥",
        "description": "फुटबॉल का सबसे हैरतअंगेज सेव! जब 99% निश्चित गोल को डिफेंडर ने हवा में उड़कर रोक लिया।\n\n#Shorts #GoalLineClearance #BestSaves #Football #Viral",
        "tags": ["impossible saves", "goal line clearance", "football defence", "shorts", "viral"],
        "hindi_script": "जब गेंद गोल लाइन पार करने ही वाली थी, तभी इस डिफेंडर ने हवा में उड़कर ऐसा अविश्वसनीय सेव किया कि पूरा स्टेडियम हैरान रह गया! इसे कहते हैं आखिरी सांस तक लड़ना!"
    },
    {
        "slot": 8,
        "clip": "assets/creator_clips/speed_04_iphone_duo.mp4",
        "title": "स्पीड ने जब लाइव स्ट्रीम पर नया आईफोन अनबॉक्स किया! 😂📱 #Shorts #IShowSpeed",
        "banner": "SPEED UNBOXING IPHONE GONE WRONG! 😂📱",
        "description": "स्पीड का आईफोन अनबॉक्सिंग जो पूरी तरह फनी आपदा बन गया!\n\n#Shorts #IShowSpeed #iPhone #FunnyUnboxing #Viral",
        "tags": ["speed iphone", "ishowspeed funny", "unboxing gone wrong", "shorts", "viral"],
        "hindi_script": "स्पीड ने जैसे ही यह नया आईफोन खोला, उसकी एक्साइटमेंट इतनी बढ़ गई कि उसने फोन को ही हवा में उछाल दिया! स्पीड के इन फनी मोमेंट्स का कोई मुकाबला नहीं है!"
    },
    {
        "slot": 9,
        "clip": "assets/creator_clips/football_01_ronaldo_bicycle.mp4",
        "title": "रोनाल्डो के इस गोल पर रियल मैड्रिड के कोच का रिएक्शन देखें! 🤯🐐 #Shorts #CR7",
        "banner": "ZIDANE REACTION TO RONALDO GOAL! 🤯🐐",
        "description": "जब कोच जिदान ने रोनाल्डो का गोल देखकर अपना सिर पकड़ लिया!\n\n#Shorts #Ronaldo #Zidane #ChampionsLeague #CR7",
        "tags": ["ronaldo zidane", "cr7 goat", "champions league", "shorts", "viral"],
        "hindi_script": "रोनाल्डो का यह गोल देखकर खुद महान कोच जिनेदिन जिदान ने अपना सिर पकड़ लिया! उन्हें यकीन ही नहीं हुआ कि कोई इंसान फुटबॉल मैदान पर ऐसा करिश्मा भी कर सकता है!"
    },
    {
        "slot": 10,
        "clip": "assets/creator_clips/speed_02_backflips.mp4",
        "title": "स्पीड का 10 मिलियन सब्सक्राइबर्स सेलिब्रेशन! 🦁🔥 #Shorts #IShowSpeed #10Million",
        "banner": "SPEED 10M CELEBRATION CRAZINESS! 🦁🔥",
        "description": "स्पीड का सबसे एनर्जेटिक और अनफिल्टर्ड मोमेंट!\n\n#Shorts #IShowSpeed #Celebration #ViralStream #Shorts",
        "tags": ["speed celebration", "ishowspeed 10m", "viral streamer", "shorts", "cr7"],
        "hindi_script": "स्पीड का यह सेलिब्रेशन देखकर आप भी अपनी हंसी नहीं रोक पाएंगे! बिना किसी स्क्रिप्ट के स्पीड की यह असली एनर्जी ही उसे दुनिया का सबसे बड़ा स्ट्रीमर बनाती है!"
    }
]

# ==============================================================================
# CHANNEL 1: MiniTalesWorld (Original Fact & Mystery Channel)
# Target: FactTechz-Style HD Moving B-Roll Hindi Documentary Shorts
# ==============================================================================
CHANNEL_1_BLUEPRINTS: List[Dict[str, Any]] = [
    {
        "slot": 1,
        "niche": "Dark Psychology",
        "scenes": ["assets/ai_video_clips/bg_darkpsych.mp4", "assets/ai_video_clips/bg_psychology.mp4"],
        "title": "3 साइकोलॉजिकल ट्रिक्स जो सबको आपका दीवाना बना देंगी! 😱 #Shorts #PsychologyFacts",
        "banner": "DARK PSYCHOLOGY TRICKS! 🧠⚠️",
        "description": "ये 3 मनोवैज्ञानिक नियम आपकी पर्सनालिटी को पूरी तरह बदल देंगे।\n#Shorts #HindiFacts #PsychologyInHindi #LifeHacks",
        "tags": ["psychology tricks", "dark psychology", "hindi facts", "body language", "shorts", "viral"],
        "hindi_script": "नंबर एक। जब भी किसी से बात करें तो उनकी आंखों में शांत होकर देखें। बात खत्म होने के बाद 2 सेकंड रुकें। यह पॉज आपके शब्दों को ताकतवर बना देता है। नंबर दो। अगर कोई आपका मजाक उड़ाए, तो गुस्सा होने की बजाय मुस्कुरा कर पूछें: क्या आप ठीक हैं? नंबर तीन। कभी अपनी अगली चाल पहले मत बताएं, काम को चुपचाप होने दें।"
    },
    {
        "slot": 2,
        "niche": "Ancient Mysteries",
        "scenes": ["assets/ai_video_clips/bg_pyramid.mp4", "assets/ai_video_clips/bg_space.mp4"],
        "title": "मिस्र के पिरामिडों का यह खौफनाक सच कोई नहीं बताता! 🏛️ #Shorts #AncientMysteries",
        "banner": "EGYPT PYRAMIDS SECRET! 🏛️⏳",
        "description": "पिरामिडों का ऐसा रहस्य जिसे आज तक आधुनिक विज्ञान भी नहीं सुलझा पाया।\n#Shorts #Pyramids #Mystery #HistoryFacts #Hindi",
        "tags": ["egypt pyramids", "ancient mysteries", "rahasya", "hindi facts", "shorts", "viral"],
        "hindi_script": "मिस्र के ग्रेट पिरामिड में 23 लाख से ज्यादा भारी पत्थर लगे हैं। हैरानी की बात यह है कि हर पत्थर का वजन दो से सत्तर टन तक है! उस जमाने में जब पहिया या क्रेन भी नहीं थी, तब इतने भारी पत्थर 450 फीट ऊपर कैसे चढ़ाए गए? आज की सबसे आधुनिक मशीनें भी ऐसा निर्माण नहीं कर सकतीं!"
    },
    {
        "slot": 3,
        "niche": "Ocean Mysteries",
        "scenes": ["assets/ai_video_clips/bg_bermuda.mp4", "assets/ai_video_clips/bg_ocean.mp4"],
        "title": "बरमूडा ट्रायंगल में गायब होने वाले जहाजों का असली सच! 🌊⚓ #Shorts #BermudaTriangle",
        "banner": "BERMUDA TRIANGLE REAL TRUTH! 🌊⚓",
        "description": "बरमूडा ट्रायंगल के भीतर ऐसा क्या है जो जहाजों और विमानों को निगल जाता है?\n#Shorts #Bermuda #OceanMystery #StrangeFacts",
        "tags": ["bermuda triangle", "ocean mysteries", "lost ships", "shorts", "hindi facts"],
        "hindi_script": "अटलांटिक महासागर का एक ऐसा रहस्यमय इलाका, जहां घुसते ही जहाजों के कंपास काम करना बंद कर देते हैं! पिछले 100 सालों में यहां 50 से ज्यादा जहाज और 20 विमान हमेशा के लिए गायब हो चुके हैं, जिनका मलबा आज तक किसी को नहीं मिला!"
    },
    {
        "slot": 4,
        "niche": "Ocean Mysteries",
        "scenes": ["assets/ai_video_clips/bg_deepsea.mp4", "assets/ai_video_clips/bg_ocean.mp4"],
        "title": "मरियाना ट्रेंच की 36,000 फीट गहराई में क्या छुपा है? 🌊👾 #Shorts #MarianaTrench",
        "banner": "DEEP SEA MONSTERS SECRETS! 🌊👾",
        "description": "समुद्र की सबसे गहरी जगह जहां सूरज की रोशनी कभी नहीं पहुंचती।\n#Shorts #DeepSea #MarianaTrench #OceanCreatures",
        "tags": ["mariana trench", "deep sea", "megalodon", "shorts", "hindi facts"],
        "hindi_script": "समुद्र का सबसे गहरा स्थान मरियाना ट्रेंच करीब 36,000 फीट गहरा है। यहां इतना भयानक दबाव है जैसे आपके ऊपर पचास बोइंग हवाई जहाज रख दिए जाएं! वैज्ञानिक मानते हैं कि इस अंधेरी गहराई में ऐसे विशालकाय जीव मौजूद हैं, जिन्हें इंसानों ने कभी नहीं देखा!"
    },
    {
        "slot": 5,
        "niche": "Money Mindset",
        "scenes": ["assets/ai_video_clips/bg_wealth.mp4", "assets/ai_video_clips/bg_money.mp4"],
        "title": "अमीर लोग अपने पैसे को 10 गुना कैसे बढ़ाते हैं? 💰📈 #Shorts #RichMindset",
        "banner": "SECRET WEALTH FORMULA! 💰📈",
        "description": "अमीरों के वे गुप्त नियम जो स्कूल और कॉलेज में कभी नहीं सिखाए जाते।\n#Shorts #MoneyRules #WealthSecrets #Investing",
        "tags": ["money mindset", "rich habits", "wealth rules", "shorts", "hindi motivational"],
        "hindi_script": "गरीब इंसान पैसे के लिए काम करता है, लेकिन अमीर इंसान अपने पैसे से काम करवाता है। जब आम लोग दिखावे के महंगे फोन और कपड़े खरीदते हैं, अमीर लोग उन पैसों को रियल एस्टेट और शेयर में लगाते हैं जो सोते समय भी पैसा बनाकर देते हैं!"
    },
    {
        "slot": 6,
        "niche": "Dark Psychology",
        "scenes": ["assets/ai_video_clips/bg_psychology.mp4", "assets/ai_video_clips/bg_darkpsych.mp4"],
        "title": "झूठ पकड़ने का यह खुफिया तरीका पुलिस भी इस्तेमाल करती है! 🕵️ #Shorts #Psychology",
        "banner": "LIE DETECTOR SECRET TRICK! 🕵️🔍",
        "description": "किसी का भी झूठ सिर्फ 5 सेकंड में पकड़ने का सबसे आसान वैज्ञानिक तरीका।\n#Shorts #LieDetection #MindHacks #Psychology",
        "tags": ["lie detector", "body language", "psychology", "shorts", "hindi facts"],
        "hindi_script": "अगर आपको शक है कि कोई आपसे झूठ बोल रहा है, तो उनकी आंखों पर ध्यान दें। जब इंसान सच याद करता है, तो आंखें बाईं तरफ ऊपर जाती हैं। लेकिन जब कोई झूठ गढ़ता है, तो आंखें दाईं ओर जाती हैं क्योंकि दिमाग नई कहानी बना रहा होता है!"
    },
    {
        "slot": 7,
        "niche": "Brain Power",
        "scenes": ["assets/ai_video_clips/bg_sleepbrain.mp4", "assets/ai_video_clips/bg_brain.mp4"],
        "title": "8 घंटे की गहरी नींद सिर्फ 10 मिनट में लेने का सीक्रेट! 😴⚡ #Shorts #SleepHack",
        "banner": "MILITARY SLEEP SECRET METHOD! 😴⚡",
        "description": "अमेरिकी सेना का वह तरीका जिससे सैनिक 2 मिनट में गहरी नींद में सो जाते हैं।\n#Shorts #SleepHacks #BrainScience #HealthTips",
        "tags": ["sleep hack", "military sleep method", "brain power", "shorts", "hindi facts"],
        "hindi_script": "अमेरिकी सेना अपने लड़ाकू पायलटों को यह स्लीप मेथड सिखाती है। पहले अपने चेहरे की सभी मांसपेशियों को ढीला छोड़ें, फिर कंधों को नीचे गिराएं और गहरी सांस लें। दिमाग में सिर्फ शांत बहते पानी की कल्पना करें। सिर्फ दो मिनट में गहरी नींद आ जाएगी!"
    },
    {
        "slot": 8,
        "niche": "Space Wonders",
        "scenes": ["assets/ai_video_clips/bg_space.mp4", "assets/ai_video_clips/bg_ocean.mp4"],
        "title": "ब्रह्मांड का सबसे खौफनाक ब्लैक होल जो रोशनी को भी निगल जाता है! 🌌🕳️ #Shorts #SpaceFacts",
        "banner": "MONSTER BLACK HOLE SECRET! 🌌🕳️",
        "description": "ब्लैक होल का ऐसा भयानक सच जो समय और स्पेस को मोड़ देता है।\n#Shorts #BlackHole #SpaceMystery #Astronomy",
        "tags": ["black hole", "space mystery", "universe facts", "shorts", "hindi"],
        "hindi_script": "ब्लैक होल अंतरिक्ष का एक ऐसा राक्षस है जिसका गुरुत्वाकर्षण इतना शक्तिशाली होता है कि रोशनी भी इससे बच नहीं सकती! अगर आप किसी ब्लैक होल के करीब जाएं, तो आपके लिए समय धीमा हो जाएगा, और आप भविष्य में पहुंच जाएंगे!"
    },
    {
        "slot": 9,
        "niche": "Ancient Mysteries",
        "scenes": ["assets/ai_video_clips/bg_temple.mp4", "assets/ai_video_clips/bg_space.mp4"],
        "title": "पुरी जगन्नाथ मंदिर के 5 चमत्कार जिन्हें विज्ञान भी नहीं समझा पाया! 🚩🛕 #Shorts #JagannathTemple",
        "banner": "JAGANNATH TEMPLE MIRACLES! 🚩🛕",
        "description": "जगन्नाथ मंदिर का ध्वज हमेशा हवा की उल्टी दिशा में क्यों फहराता है?\n#Shorts #JagannathPuri #TempleMiracle #SanatanFacts",
        "tags": ["jagannath temple", "puri miracles", "temple secrets", "shorts", "hindi facts"],
        "hindi_script": "पुरी जगन्नाथ मंदिर का ध्वज हमेशा हवा की उल्टी दिशा में लहराता है! मंदिर के शिखर के ऊपर से आज तक कोई पक्षी या हवाई जहाज नहीं उड़ पाया। और चाहे लाखों भक्त आ जाएं, मंदिर का प्रसाद कभी कम नहीं पड़ता!"
    },
    {
        "slot": 10,
        "niche": "Dark Psychology",
        "scenes": ["assets/ai_video_clips/bg_darkpsych.mp4", "assets/ai_video_clips/bg_wealth.mp4"],
        "title": "लोग आपकी इज्जत क्यों नहीं करते? यह 1 गलती तुरंत सुधारें! ⚠️ #Shorts #SelfRespect",
        "banner": "HOW TO INCREASE YOUR VALUE! ⚠️💎",
        "description": "हर जगह अपनी कद्र और इज्जत 10 गुना बढ़ाने का अचूक नियम।\n#Shorts #SelfRespect #PersonalityTips #Psychology",
        "tags": ["self respect", "personality tips", "psychology", "shorts", "hindi motivational"],
        "hindi_script": "अगर आप हर किसी के लिए हमेशा उपलब्ध रहते हैं, तो लोग आपकी कद्र करना बंद कर देंगे। जिस चीज की सप्लाई ज्यादा होती है, उसकी कीमत गिर जाती है। कभी-कभी ना कहना सीखिए। जो आसानी से नहीं मिलता, दुनिया उसी की कद्र करती है!"
    }
]

# ==============================================================================
# CHANNEL 2: Pawsome Productions
# Target: Satisfying Science Experiments, 100-Ton Hydraulic Press & Guinness World Records
# ==============================================================================
CHANNEL_2_BLUEPRINTS: List[Dict[str, Any]] = [
    {
        "slot": 1,
        "clip": "assets/creator_clips/science_01_helmet_press.mp4",
        "title": "100 टन हाइड्रोलिक प्रेस बनाम मजबूत हेलमेट! 😱🔨 #Shorts #HydraulicPress #Satisfying",
        "banner": "100-TON PRESS VS CRASH HELMET! 🔨💥",
        "description": "क्या एक मजबूत हेलमेट 100 टन के हाइड्रोलिक प्रेस का दबाव झेल पाएगा?\n\n#Shorts #HydraulicPress #Crushing #Satisfying #Viral",
        "tags": ["hydraulic press", "helmet crushing", "satisfying videos", "shorts", "viral"],
        "hindi_script": "जब इस 100 टन के शक्तिशाली हाइड्रोलिक प्रेस के नीचे इस मजबूत हेलमेट को रखा गया, तो देखिए कैसे सेकंडों में यह चूर-चूर हो गया! हाइड्रोलिक प्रेस की ताकत का कोई मुकाबला नहीं है!"
    },
    {
        "slot": 2,
        "clip": "assets/creator_clips/records_01_table_tennis.mp4",
        "title": "टेबल टेनिस का ऐसा नामुमकिन शॉट जिसे देखकर आंखें खुली रह जाएं! 😱🏓 #Shorts #WorldRecord",
        "banner": "IMPOSSIBLE PING PONG TRICKSHOT! 🏓🔥",
        "description": "गिनीज वर्ल्ड रिकॉर्ड लेवल का सबसे हैरान कर देने वाला टेबल टेनिस ट्रिक शॉट!\n\n#Shorts #PingPong #TrickShot #WorldRecord #Viral",
        "tags": ["ping pong trick shot", "table tennis", "world record", "shorts", "viral"],
        "hindi_script": "टेबल टेनिस का यह शॉट देखकर आप भी अपनी आंखों पर यकीन नहीं करेंगे! इतनी दूरी और सटीकता से यह शॉट लगाना इंसानी क्षमता से परे लगता है। इसे कहते हैं असली परफेक्शन!"
    },
    {
        "slot": 3,
        "clip": "assets/creator_clips/science_03_cards_press.mp4",
        "title": "हाइड्रोलिक प्रेस बनाम ताश के पत्तों की गड्डी! 💥🃏 #Shorts #HydraulicPress",
        "banner": "HYDRAULIC PRESS VS PLAYING CARDS! 🃏💥",
        "description": "जब 100 टन के प्रेस ने 52 ताश के पत्तों को दबाया तो क्या हुआ?\n\n#Shorts #HydraulicPress #CardsCrushing #SatisfyingShorts",
        "tags": ["hydraulic press", "playing cards", "satisfying", "shorts", "viral"],
        "hindi_script": "ताश के पत्तों की गड्डी पर जब 100 टन का दबाव डाला गया, तो पत्ते ऐसे फूटे जैसे कोई छोटा धमाका हुआ हो! यह वीडियो देखने में बेहद सुकून देने वाला और संतोषजनक है!"
    },
    {
        "slot": 4,
        "clip": "assets/creator_clips/records_02_levitation_handstand.mp4",
        "title": "गुरुत्वाकर्षण को चुनौती देने वाला नामुमकिन हैंडस्टैंड स्टंट! 🤯🤸 #Shorts #HumanStunts",
        "banner": "GRAVITY DEFYING HANDSTAND! 🤸⚡",
        "description": "इस लड़के ने फिजिक्स के नियमों को पूरी तरह गलत साबित कर दिया!\n\n#Shorts #Handstand #Calisthenics #BodyPower #Viral",
        "tags": ["calisthenics", "gravity defying", "handstand stunt", "shorts", "viral"],
        "hindi_script": "इस लड़के के शरीर का संतुलन देखकर वैज्ञानिक भी हैरान हैं! हवा में सिर्फ उंगलियों के बल पर पूरे शरीर को साध लेना, यह साबित करता है कि इंसान अभ्यास से कुछ भी कर सकता है!"
    },
    {
        "slot": 5,
        "clip": "assets/creator_clips/science_04_solar_panel.mp4",
        "title": "हाइड्रोलिक प्रेस बनाम सोलर पैनल का भयानक क्रंच! ☀️💥 #Shorts #HydraulicPress",
        "banner": "HYDRAULIC PRESS VS SOLAR PANEL! ☀️💥",
        "description": "जब सोलर पैनल पर पड़ा 100 टन का हाइड्रोलिक वजन!\n\n#Shorts #SolarPanel #HydraulicPress #ScienceExperiments",
        "tags": ["solar panel crush", "hydraulic press", "science shorts", "shorts", "viral"],
        "hindi_script": "जब इस सिलिकॉन सोलर पैनल पर हाइड्रोलिक प्रेस का दबाव पड़ा, तो कांच के हजारों टुकड़े चमकते हुए बिखर गए! यह क्रंच देखने में बेहद संतोषजनक और अद्भुत है!"
    },
    {
        "slot": 6,
        "clip": "assets/creator_clips/records_03_juggling_sword.mp4",
        "title": "आंखों पर पट्टी बांधकर तलवारों से करतब! 😱🗡️ #Shorts #GuinnessRecord",
        "banner": "EXTREME BLINDFOLD SWORD STUNT! 🗡️⚠️",
        "description": "मौत को छूकर वापस आने वाला सबसे खतरनाक स्टंट!\n\n#Shorts #SwordStunt #DangerousRecords #WorldRecord #Viral",
        "tags": ["sword stunt", "guinness record", "extreme stunt", "shorts", "viral"],
        "hindi_script": "जरा सी भी चूक और सीधे जान का खतरा! आंखों पर काली पट्टी बांधकर इन धारदार तलवारों को हवा में उछालना मौत से खेलने जैसा है। इस स्टंटबाज के साहस को सलाम है!"
    },
    {
        "slot": 7,
        "clip": "assets/creator_clips/science_02_prettiest_crunch.mp4",
        "title": "इंटरनेट का सबसे खूबसूरत और संतोषजनक क्रंच! 😍✨ #Shorts #OddlySatisfying",
        "banner": "MOST SATISFYING CRUNCH EVER! 😍✨",
        "description": "इसे देखकर आपका सारा स्ट्रेस चुटकियों में गायब हो जाएगा!\n\n#Shorts #Satisfying #StressRelief #HydraulicPress #Viral",
        "tags": ["oddly satisfying", "crunch", "stress relief", "shorts", "viral"],
        "hindi_script": "अगर आप दिनभर की थकान से परेशान हैं, तो इस वीडियो को पूरे ध्यान से देखिए! यह क्रंच इतना संतोषजनक है कि आपका सारा तनाव सेकंडों में दूर हो जाएगा!"
    },
    {
        "slot": 8,
        "clip": "assets/creator_clips/records_04_human_catapult.mp4",
        "title": "इंसान को गुलेल की तरह हवा में 100 फीट ऊपर फेंक दिया! 😱🚀 #Shorts #HumanCatapult",
        "banner": "100FT HUMAN CATAPULT LAUNCH! 🚀😱",
        "description": "दुनिया का सबसे रोंगटे खड़े कर देने वाला एक्सट्रीम एडवेंचर स्टंट!\n\n#Shorts #HumanCatapult #ExtremeStunts #Adrenaline #Viral",
        "tags": ["human catapult", "extreme sports", "insane stunt", "shorts", "viral"],
        "hindi_script": "जब इस विशालकाय कैटापुल्ट ने इस इंसान को 100 फीट ऊपर हवा में उछाला, तो जमीन पर खड़े लोगों की सांसें थम गईं! कमजोर दिल वाले इस स्टंट को बिल्कुल न देखें!"
    },
    {
        "slot": 9,
        "clip": "assets/creator_clips/science_01_helmet_press.mp4",
        "title": "क्या हेलमेट 50,000 किलो का वजन रोक पाया? 😱🔨 #Shorts #SafetyTest",
        "banner": "CAN A HELMET SURVIVE 50,000 KG? 🔨⚠️",
        "description": "बाइक हेलमेट की असली मजबूती का सबसे कड़ा टेस्ट!\n\n#Shorts #HelmetTest #HydraulicPress #SafetyFirst #Viral",
        "tags": ["helmet test", "hydraulic press test", "satisfying science", "shorts", "viral"],
        "hindi_script": "आपकी सुरक्षा करने वाला हेलमेट असल में कितना मजबूत होता है? इस 100 टन प्रेस टेस्ट ने दिखा दिया कि अच्छी क्वालिटी का हेलमेट किस हद तक आपकी जान बचा सकता है!"
    },
    {
        "slot": 10,
        "clip": "assets/creator_clips/records_02_levitation_handstand.mp4",
        "title": "इस लड़के ने जमीन से हाथ उठाकर सबको चौंका दिया! 😱🤸 #Shorts #ImpossibleBalance",
        "banner": "ONE-ARM IMPOSSIBLE BALANCE! 🤸🔥",
        "description": "ताकत और एकाग्रता का सबसे बेमिसाल नमूना!\n\n#Shorts #CalisthenicsPower #HumanFeats #ViralShorts",
        "tags": ["impossible balance", "one arm handstand", "fitness motivation", "shorts", "viral"],
        "hindi_script": "कड़ी मेहनत और अटूट एकाग्रता से इंसान क्या नहीं कर सकता! इस एक हाथ के बैलेंस ने दुनिया भर के फिटनेस एक्सपर्ट्स को हैरान कर दिया है!"
    }
]
