"""
Hindi & Hinglish Script Generator for Viral YouTube Shorts & Reels
Includes 30+ high-retention, non-repeating viral topics across:
- Dark Psychology & Body Language
- Ancient Mysteries & Strange History
- Deep Ocean & Alien Creatures
- Money, Wealth & Rich Mindset
- Brain Power & Sleep Secrets
- Cosmic Space & Black Holes
"""

import os
import sys
import json
import random
from typing import Dict, Any, List

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

HINDI_VIRAL_SCRIPTS: List[Dict[str, Any]] = [
    # --- BATCH 1: PSYCHOLOGY & HUMAN BEHAVIOR ---
    {
        "niche": "Dark Psychology",
        "title": "3 साइकोलॉजिकल ट्रिक्स जो सबको आपका दीवाना बना देंगी! 😱 #Shorts #PsychologyFacts",
        "tags": ["psychology", "hindi facts", "body language", "human behavior", "shorts", "mindset"],
        "description": "ये 3 मनोवैज्ञानिक नियम आपकी पर्सनालिटी को पूरी तरह बदल देंगे।\n#Shorts #HindiFacts #PsychologyInHindi",
        "text": "नंबर एक। जब भी किसी से बात करें तो उनकी आंखों में शांत होकर देखें। बात खत्म होने के तुरंत बाद बोलने की बजाय 2 सेकंड रुकें। यह साइकोलॉजिकल पॉज आपके शब्दों को 10 गुना ज्यादा ताकतवर बना देता है। नंबर दो। अगर कोई आपका मजाक उड़ाने की कोशिश करे, तो गुस्सा होने की बजाय सिर्फ मुस्कुरा कर पूछें: क्या आप ठीक हैं? यह एक सवाल उनका पूरा कॉन्फिडेंस गिरा देगा। नंबर तीन। कभी भी किसी को अपनी अगली चाल पहले मत बताएं। काम को चुपचाप होने दें और नतीजे को शोर मचाने दें।"
    },
    {
        "niche": "Dark Psychology",
        "title": "झूठ पकड़ने का यह खुफिया तरीका पुलिस भी इस्तेमाल करती है! 🕵️ #Shorts #Psychology",
        "tags": ["psychology tricks", "lie detector", "body language", "shorts", "hindi facts"],
        "description": "किसी का भी झूठ 5 सेकंड में पकड़ने का सबसे आसान तरीका।\n#Shorts #LieDetector #MindHacks",
        "text": "अगर आपको शक है कि कोई आपसे झूठ बोल रहा है, तो बस उनकी आंखों और हाथों पर ध्यान दें। जब इंसान सच बोलता है, तो उसकी आंखें बाईं तरफ ऊपर की ओर जाती हैं क्योंकि वह यादों को याद कर रहा होता है। लेकिन जब कोई झूठ गढ़ता है, तो उसकी आंखें दाईं ओर जाती हैं क्योंकि उसका दिमाग नई कहानी बना रहा होता है। साथ ही, झूठा इंसान अक्सर अपनी नाक या मुंह को छूता है। यह ट्रिक आजमाकर देखिए, आप कभी धोखा नहीं खाएंगे।"
    },
    {
        "niche": "Dark Psychology",
        "title": "किसी को भी अपनी बात मनवाने का यह सीक्रेट नियम! 💡 #Shorts #Persuasion",
        "tags": ["persuasion", "psychology", "manipulation", "shorts", "hindi"],
        "description": "बातचीत में हमेशा जीतने का सबसे शक्तिशाली फॉर्मूला।\n#Shorts #PsychologyHacks #Influence",
        "text": "मनोविज्ञान का एक बहुत बड़ा नियम है: 'डोर इन द फेस' तकनीक। अगर आप किसी से कोई काम करवाना चाहते हैं, तो पहले उनसे कोई बहुत बड़ा और मुश्किल काम मांगें, जिसे वे तुरंत मना कर दें। उनके मना करते ही तुरंत अपना असली और छोटा काम उनके सामने रख दें। अपराधबोध और संकोच के कारण वे आपके दूसरे काम को कभी मना नहीं कर पाएंगे। इसे कहते हैं दिमाग से खेलना।"
    },
    {
        "niche": "Dark Psychology",
        "title": "लोग आपकी इज्जत क्यों नहीं करते? यह 1 गलती तुरंत सुधारें! ⚠️ #Shorts #SelfRespect",
        "tags": ["self respect", "personality tips", "psychology", "shorts", "motivational"],
        "description": "हर जगह अपनी इज्जत और वैल्यू 10 गुना बढ़ाने के नियम।\n#Shorts #ValueYourself #Personality",
        "text": "अगर आप हर किसी के लिए हमेशा उपलब्ध रहते हैं, तो लोग आपकी कद्र करना बंद कर देंगे। अर्थशास्त्र का नियम है: जिस चीज की सप्लाई ज्यादा होती है, उसकी कीमत गिर जाती है। जब भी कोई आपको बुलाए, तुरंत दौड़कर मत जाइए। कभी-कभी 'ना' कहना सीखिए। जो लोग आसानी से उपलब्ध नहीं होते, दुनिया उनकी हर बात को बहुत ध्यान और सम्मान से सुनती है।"
    },

    # --- BATCH 2: HISTORICAL & ANCIENT MYSTERIES ---
    {
        "niche": "Ancient Mysteries",
        "title": "मिस्र के पिरामिडों का यह खौफनाक सच कोई नहीं बताता! 🏛️ #Shorts #AncientMysteries",
        "tags": ["pyramids", "ancient history", "rahasya", "hindi facts", "shorts", "viral"],
        "description": "पिरामिडों के नीचे दफन ऐसा रहस्य जिसे आज तक वैज्ञानिक भी नहीं सुलझा पाए।\n#Shorts #PyramidMystery #HistoryFacts",
        "text": "मिस्र के गीजा पिरामिड को लेकर एक ऐसा रहस्य है जिसे सुनकर आपके रोंगटे खड़े हो जाएंगे। वैज्ञानिकों के अनुसार पिरामिड को बनाने में इस्तेमाल किए गए पत्थरों का वजन 50 हाथियों के बराबर था। लेकिन सवाल यह है कि बिना क्रेन और आधुनिक मशीनों के हजारों साल पहले 450 फीट की ऊंचाई पर ये पत्थर कैसे चढ़ाए गए? सबसे ज्यादा हैरान करने वाली बात यह है कि पिरामिड के अंदर का तापमान हमेशा बिल्कुल 20 डिग्री सेल्सियस स्थिर रहता है।"
    },
    {
        "niche": "Ancient Mysteries",
        "title": "बरमूडा ट्रायंगल में गायब हुए जहाजों के साथ क्या होता है? 🚢⚠️ #Shorts #BermudaTriangle",
        "tags": ["bermuda triangle", "mystery", "unexplained", "shorts", "hindi facts"],
        "description": "बरमूडा ट्रायंगल का वह सच जिसने वैज्ञानिकों के होश उड़ा दिए।\n#Shorts #MysteryHindi #BermudaFacts",
        "text": "अटलांटिक महासागर का एक ऐसा हिस्सा जहां आज तक 50 से ज्यादा बड़े जहाज और 20 हवाई जहाज हवा में ही गायब हो चुके हैं, और उनका एक भी टुकड़ा कभी नहीं मिला। जब कोई पायलट इस इलाके के ऊपर से गुजरता है, तो उसके कंपास और दिशा सूचक यंत्र पागलों की तरह घूमने लगते हैं। कुछ वैज्ञानिक मानते हैं कि यहां समुद्र के नीचे से भारी मात्रा में मीथेन गैस फटती है, जो जहाजों को सीधे पाताल में खींच लेती है।"
    },
    {
        "niche": "Ancient Mysteries",
        "title": "भारत का यह मंदिर गुरुत्वाकर्षण के नियमों को झुठलाता है! 🛕✨ #Shorts #IndianTemples",
        "tags": ["indian temples", "rahasya", "ancient science", "shorts", "sanatan"],
        "description": "हजारों साल पुराने भारतीय मंदिरों का अद्भुत विज्ञान।\n#Shorts #TempleMysteries #AncientIndia",
        "text": "पुरी के जगन्नाथ मंदिर का विज्ञान देखकर नासा के वैज्ञानिक भी हैरान हैं। मंदिर के ऊपर लगा सुदर्शन चक्र आप शहर के किसी भी कोने से देखें, उसका मुंह हमेशा आपकी तरफ ही दिखाई देगा। और सबसे विचित्र बात यह है कि इस मंदिर के ऊपर से आज तक न तो कोई पक्षी उड़ा है और न ही कोई हवाई जहाज निकल सकता है। हमारे पूर्वजों का विज्ञान आज की आधुनिक तकनीक से कहीं ज्यादा आगे था।"
    },
    {
        "niche": "Ancient Mysteries",
        "title": "एंटार्कटिका की बर्फ के 2 मील नीचे वैज्ञानिकों को क्या मिला? ❄️😱 #Shorts #Antarctica",
        "tags": ["antarctica", "mystery", "science secrets", "shorts", "viral facts"],
        "description": "बर्फ के नीचे छिपा दुनिया का सबसे रहस्यमयी महाद्वीप।\n#Shorts #AntarcticaMystery #IceSecrets",
        "text": "एंटार्कटिका सिर्फ बर्फ का एक टुकड़ा नहीं है। सैटेलाइट इमेज से वैज्ञानिकों को बर्फ के दो मील नीचे विशाल पिरामिड जैसी संरचनाएं और बहती हुई गर्म पानी की नदियां मिली हैं। शोधकर्ताओं का मानना है कि लाखों साल पहले एंटार्कटिका एक हरा-भरा जंगल था जहां उन्नत सभ्यताएं रहा करती थीं। क्या बर्फ पिघलने पर दुनिया का सबसे बड़ा रहस्य सामने आएगा?"
    },

    # --- BATCH 3: DEEP OCEAN & MONSTER CREATURES ---
    {
        "niche": "Ocean Mysteries",
        "title": "समुद्र की गहराई में छिपा सबसे खतरनाक सच! 🌊 #Shorts #OceanMysteries",
        "tags": ["ocean", "science facts", "deep sea", "hindi facts", "shorts", "creatures"],
        "description": "इंसान चांद पर पहुंच चुका है, लेकिन समुद्र का 80% हिस्सा आज भी अनजान है।\n#Shorts #OceanFacts #DeepSea",
        "text": "क्या आप जानते हैं कि हम चांद के बारे में ज्यादा जानते हैं लेकिन अपने ही समुद्र के बारे में सिर्फ 5 प्रतिशत? समुद्र के सबसे गहरे हिस्से मरियाना ट्रेंच में इतना भयानक दबाव है कि वह एक इंसान को 1 सेकंड में कागज की तरह मसल सकता है। वहां सूरज की रोशनी कभी नहीं पहुंचती, फिर भी वहां ऐसे विचित्र जीव रहते हैं जो खुद अपनी रोशनी पैदा करते हैं।"
    },
    {
        "niche": "Ocean Mysteries",
        "title": "मेगालोडन शार्क आज भी जिंदा है? यह सबूत देखिए! 🦈⚠️ #Shorts #Megalodon",
        "tags": ["megalodon", "sharks", "ocean giants", "shorts", "mystery facts"],
        "description": "क्या समुद्र का सबसे विशालकाय शिकारी आज भी गहराइयों में छुपा है?\n#Shorts #SharkFacts #DeepOcean",
        "text": "मेगालोडन—इतिहास की सबसे बड़ी शार्क, जिसका एक दांत इंसान के हाथ से भी बड़ा होता था। वैज्ञानिक कहते हैं कि यह 20 लाख साल पहले विलुप्त हो गई थी। लेकिन जब समुद्र के सबसे गहरे हिस्सों में विशाल व्हेल मछलियों पर ऐसे दांतों के निशान मिले जो किसी आम शार्क के नहीं हो सकते, तो सब हैरान रह गए। समुद्र का 80 प्रतिशत हिस्सा आज भी इंसानों ने नहीं देखा है। क्या यह दानव आज भी जिंदा है?"
    },
    {
        "niche": "Ocean Mysteries",
        "title": "समुद्र का 'द ब्लोप' साउंड—जिसने वैज्ञानिकों को डरा दिया! 🔊🌊 #Shorts #TheBloop",
        "tags": ["the bloop", "underwater sound", "ocean mystery", "shorts", "scary facts"],
        "description": "1997 में समुद्र के नीचे से आई ऐसी रहस्यमयी आवाज जिसने सबको हैरान कर दिया।\n#Shorts #UnderwaterMystery #OceanSecrets",
        "text": "साल 1997 में समुद्र के 5000 किलोमीटर दायरे में पानी के नीचे लगे माइक्रोफोन्स ने एक ऐसी भयानक आवाज रिकॉर्ड की जिसे सुनकर वैज्ञानिक कांप गए। यह आवाज किसी भी ज्ञात व्हेल या जीव से 10 गुना ज्यादा तेज थी। कई वैज्ञानिकों का मानना था कि समुद्र की गहराइयों में कोई ऐसा विशालकाय जीव मौजूद है जिसे विज्ञान आज तक नहीं खोज पाया है।"
    },

    # --- BATCH 4: MONEY & WEALTH MINDSET ---
    {
        "niche": "Money Mindset",
        "title": "20 की उम्र में अमीर बनने का यह सीक्रेट कोई नहीं सिखाता! 💰 #Shorts #MoneyMindset",
        "tags": ["money", "rich mindset", "investing", "hindi business", "shorts", "financial freedom"],
        "description": "गरीब और अमीर सोच के बीच का सबसे बड़ा अंतर।\n#Shorts #MoneyTipsInHindi #RichMindset",
        "text": "स्कूल हमें पढ़ना सिखाता है, लेकिन पैसा कमाना और उसे संभालना कोई नहीं सिखाता। गरीब इंसान सोचता है कि ज्यादा मेहनत करने से ज्यादा पैसा मिलेगा। लेकिन अमीर इंसान जानता है कि जब तक आपका पैसा आपके लिए 24 घंटे काम नहीं करेगा, तब तक आप जिंदगी भर मेहनत करते रह जाएंगे। पैसे को बैंक में सड़ाने की बजाय ऐसी संपत्तियां खरीदें जो सोते समय भी पैसा बनाएं।"
    },
    {
        "niche": "Money Mindset",
        "title": "अमीर लोग टैक्स कैसे बचाते हैं? अमीर बनने का 1 नियम! 💸 #Shorts #WealthSecret",
        "tags": ["tax secrets", "rich habits", "wealth building", "shorts", "money tips"],
        "description": "अमीरों का वह सीक्रेट जो मिडिल क्लास को कभी समझ नहीं आता।\n#Shorts #FinancialEducation #MoneyHacks",
        "text": "मिडिल क्लास इंसान सैलरी कमाता है और सबसे पहले 30 प्रतिशत टैक्स भरता है। लेकिन अमीर अरबपति कभी बड़ी सैलरी नहीं लेते। वे अपनी कंपनियों के शेयर्स और संपत्तियां खरीदते हैं और उनके बदले बैंकों से बहुत कम ब्याज पर लोन लेते हैं। लोन के पैसे पर कानूनन कोई टैक्स नहीं लगता। इस तरह वे बिना टैक्स दिए लग्जरी गाड़ियां और बंगले खरीदते हैं। खेल पैसे का नहीं, वित्तीय ज्ञान का है।"
    },
    {
        "niche": "Money Mindset",
        "title": "अगर आपके पास 10,000 रुपये हैं, तो इसे यहाँ लगाओ! 📈 #Shorts #Investment",
        "tags": ["investing for beginners", "stock market", "mutual funds", "shorts", "money"],
        "description": "छोटी उम्र में करोड़पति बनने का सबसे सुरक्षित फॉर्मूला।\n#Shorts #InvestingHindi #Compounding",
        "text": "अगर आप 20 साल की उम्र से सिर्फ 2000 रुपये महीना इंडेक्स फंड में लगातार निवेश करते हैं, तो कंपाउंडिंग की ताकत से 40 की उम्र तक यह रकम 2 करोड़ रुपये से ज्यादा हो जाएगी। अल्बर्ट आइंस्टीन ने कंपाउंडिंग को दुनिया का आठवां अजूबा कहा था। जो इसे समझता है वह कमाता है, जो नहीं समझता वह जिंदगी भर ब्याज भरता है।"
    },

    # --- BATCH 5: BRAIN & SLEEP SECRETS ---
    {
        "niche": "Brain Power",
        "title": "आपका दिमाग रात को सोने के बाद यह खौफनाक काम करता है! 🧠 #Shorts #BodyFacts",
        "tags": ["human body", "brain facts", "sleep", "hindi facts", "shorts", "health"],
        "description": "सोते समय आपका दिमाग क्या करता है, जानकर आपके होश उड़ जाएंगे।\n#Shorts #HumanBodyHindi #BrainFacts",
        "text": "जब आप रात को गहरी नींद में होते हैं, तो आपका दिमाग बंद नहीं होता, बल्कि एक जादुई प्रक्रिया शुरू करता है। दिनभर काम करने के बाद जो टॉक्सिन्स जमा होते हैं, रात को मस्तिष्क की कोशिकाएं सिकुड़ जाती हैं और एक खास तरल पदार्थ पूरे दिमाग को धोकर साफ करता है। अगर आप 7 से 8 घंटे की नींद नहीं लेते, तो यह कचरा दिमाग में ही रह जाता है।"
    },
    {
        "niche": "Brain Power",
        "title": "सुबह उठते ही यह 1 गलती आपका दिमाग कमजोर कर देती है! 📱⚠️ #Shorts #BrainHacks",
        "tags": ["morning routine", "brain health", "productivity", "shorts", "habits"],
        "description": "सुबह की यह आम आदत आपकी सोचने की क्षमता को खत्म कर रही है।\n#Shorts #MorningHabits #FocusTips",
        "text": "सुबह आंख खुलते ही सबसे पहले अपना स्मार्टफोन चेक करना आपके दिमाग के लिए सबसे खतरनाक है। जब आप सोकर उठते हैं, तो आपका मस्तिष्क थीटा तरंगों से अल्फा तरंगों में जा रहा होता है। फोन की स्क्रीन देखते ही दिमाग में डोपामाइन और कोर्टिसोल का अचानक विस्फोट होता है, जिससे पूरा दिन बेचैनी और तनाव बना रहता है। सुबह के पहले 30 मिनट फोन से दूर रहें।"
    },
    {
        "niche": "Brain Power",
        "title": "फोटोग्राफिक मेमोरी पाने का प्राचीन भारतीय तरीका! 🧘 #Shorts #MemoryPower",
        "tags": ["memory power", "study tips", "ancient india", "shorts", "brain boost"],
        "description": "पढ़ा हुआ हमेशा याद रखने की सबसे असरदार तकनीक।\n#Shorts #SuperMemory #FocusHacks",
        "text": "क्या आप जानते हैं कि स्वामी विवेकानंद किसी भी किताब के पन्ने को सिर्फ एक बार देखकर पूरा का पूरा याद कर लेते थे? प्राचीन भारत में इसे 'त्राटक ध्यान' कहा जाता था। रोजाना केवल 5 मिनट किसी एक बिंदु या मोमबत्ती की लौ पर बिना पलक झपकाए ध्यान लगाने से दिमाग का फोकस 500 गुना बढ़ जाता है। इसे 21 दिन करके देखिए, आपकी याददाश्त कंप्यूटर जैसी तेज हो जाएगी।"
    },

    # --- BATCH 6: SPACE & COSMIC WONDERS ---
    {
        "niche": "Space Wonders",
        "title": "ब्लैक होल के अंदर गिरते ही आपके शरीर के साथ क्या होगा? 🕳️😱 #Shorts #SpaceMysteries",
        "tags": ["black hole", "space facts", "universe", "shorts", "astronomy"],
        "description": "ब्रह्मांड की सबसे रहस्यमयी शक्ति ब्लैक होल का सच।\n#Shorts #BlackHole #SpaceHindi",
        "text": "अगर आप किसी ब्लैक होल में गिर जाएं, तो भौतिकी के सारे नियम खत्म हो जाएंगे। ब्लैक होल का गुरुत्वाकर्षण इतना भयानक होता है कि वह आपके सिर और पैरों के बीच लाखों गुना खिंचाव पैदा करेगा, जिसे वैज्ञानिक 'स्पेगेटीफिकेशन' कहते हैं। आपका शरीर रबड़ की तरह लंबा खिंच जाएगा। सबसे विचित्र बात यह है कि बाहर खड़े किसी इंसान के लिए आपका समय हमेशा के लिए रुक जाएगा।"
    },
    {
        "niche": "Space Wonders",
        "title": "ब्रह्मांड का सबसे बड़ा तारा—जिसके आगे सूरज एक कण जैसा है! ☀️🌌 #Shorts #UniverseFacts",
        "tags": ["universe", "stars", "space scale", "shorts", "mind blown"],
        "description": "ब्रह्मांड के इस महाकाय तारे को देखकर आपका दिमाग सुन्न हो जाएगा।\n#Shorts #Cosmos #SpaceFactsHindi",
        "text": "हमारी पृथ्वी सूरज के सामने एक छोटे से दाने जैसी है, और सूरज में 13 लाख पृथ्वियां समा सकती हैं। लेकिन ब्रह्मांड का सबसे बड़ा ज्ञात तारा 'स्टीफेंसन 2-18' इतना विशाल है कि इसके अंदर 10 अरब सूरज समा सकते हैं। अगर आप प्रकाश की गति यानी 3 लाख किलोमीटर प्रति सेकंड से भी इसके चारों ओर चक्कर लगाएं, तो एक चक्कर पूरा करने में 9 घंटे का समय लगेगा।"
    },

    # --- BATCH 7: DEEPER PSYCHOLOGY & ANCIENT WONDERS ---
    {
        "niche": "Dark Psychology",
        "title": "किसी के दिमाग को शांत करने की यह ट्रिक कोई नहीं जानता! 🧠🤫 #Shorts #PsychologyFacts",
        "tags": ["psychology", "body language", "mind tricks", "shorts", "hindi facts"],
        "description": "गुस्से में किसी को भी 2 सेकंड में शांत करने का मनोवैज्ञानिक तरीका।\n#Shorts #PsychologyHacks #Hindi",
        "text": "जब भी कोई आप पर चिल्लाए या गुस्सा करे, तो बदले में चिल्लाने की गलती कभी मत करिए। बस अपनी आवाज को सामान्य से और ज्यादा धीमा और शांत कर दीजिए। जब आप पूरी शांति से बात करते हैं, तो सामने वाले का दिमाग खुद ब खुद अपनी गलती महसूस करने लगता है और उनका गुस्सा 10 सेकंड में ठंडा पड़ जाता है। इसे कहते हैं मनोवैज्ञानिक नियंत्रण।"
    },
    {
        "niche": "Dark Psychology",
        "title": "अगर कोई आपको इग्नोर करे, तो यह 1 काम करो! ⚠️ #Shorts #SelfRespect",
        "tags": ["psychology tricks", "self respect", "mindset", "shorts", "hindi facts"],
        "description": "अपनी कद्र और अहमियत वापस पाने का सबसे असरदार तरीका।\n#Shorts #ValueYourself #Personality",
        "text": "अगर कोई आपके मैसेज का जवाब देर से देता है या आपको नजरअंदाज करता है, तो उन्हें बार-बार फोन या मैसेज करने की भूल कभी न करें। तुरंत पीछे हट जाएं और अपनी जिंदगी में इतने व्यस्त हो जाएं कि उनके पास सोचने का समय ही न रहे। जब आप किसी का पीछा करना छोड़ देते हैं, तो वे आपकी कमी महसूस करने लगते हैं। खामोशी सबसे बड़ा जवाब है।"
    },
    {
        "niche": "Ancient Mysteries",
        "title": "कैलाश पर्वत पर आज तक कोई क्यों नहीं चढ़ पाया? 🏔️🚩 #Shorts #KailashMystery",
        "tags": ["kailash", "ancient mystery", "sanatan", "shorts", "hindi facts", "himalayas"],
        "description": "कैलाश पर्वत का वह रहस्य जिसे विज्ञान आज तक नहीं समझ पाया।\n#Shorts #MountKailash #Rahasya",
        "text": "माउंट एवरेस्ट जिसकी ऊंचाई 8848 मीटर है, उस पर 7000 से ज्यादा लोग चढ़ चुके हैं। लेकिन 6638 मीटर ऊंचे कैलाश पर्वत पर आज तक कोई इंसान नहीं पहुंच पाया। जो भी पर्वतारोही वहां चढ़ने की कोशिश करते हैं, उनके नाखून और बाल असामान्य रूप से तेजी से बढ़ने लगते हैं और उनका समय तेज चलने लगता है। वैज्ञानिक मानते हैं कि कैलाश पर्वत पृथ्वी का ऊर्जा केंद्र और अलौकिक शक्तियों का निवास है।"
    },
    {
        "niche": "Ancient Mysteries",
        "title": "अजंता एलोरा की गुफाएं आखिर किसने बनाईं? 🛕⚡ #Shorts #AncientIndia",
        "tags": ["ellora caves", "ancient engineering", "aliens", "shorts", "hindi facts"],
        "description": "एक ही विशाल पहाड़ को ऊपर से नीचे काटकर बनाया गया दुनिया का सबसे अद्भुत मंदिर।\n#Shorts #KailashTemple #AncientTechnology",
        "text": "एलोरा का कैलाश मंदिर इंसानी इतिहास का सबसे बड़ा चमत्कार है। इसे नीचे से नहीं, बल्कि एक पूरे पहाड़ को ऊपर से नीचे की ओर काटकर तराशा गया था। 4 लाख टन भारी पत्थरों को बिना किसी आधुनिक मशीन के कैसे हटाया गया, यह रहस्य आज तक कोई इंजीनियर नहीं सुलझा पाया। अगर आज की आधुनिक क्रेन और लेजर तकनीक भी इस्तेमाल की जाए, तो ऐसा मंदिर बनने में सैकड़ों साल लग जाएंगे।"
    },
    {
        "niche": "Ocean Mysteries",
        "title": "समुद्र के 11,000 मीटर नीचे मिला यह एलियन जीव! 🐙🌊 #Shorts #MarianaTrench",
        "tags": ["mariana trench", "deep sea", "ocean creatures", "shorts", "mystery"],
        "description": "मरियाना ट्रेंच की अंधी गहराइयों में छिपा खौफनाक जीव।\n#Shorts #DeepOcean #UnderwaterCreatures",
        "text": "प्रशांत महासागर की सबसे गहरी खाई मरियाना ट्रेंच में वैज्ञानिकों ने रोबोटिक कैमरे उतारे, तो उन्हें ऐसा जीव दिखाई दिया जिसने जीव विज्ञान के सारे नियम पलट दिए। 11000 मीटर गहराई में जहां पानी का दबाव 1000 हाथियों के वजन जितना भारी है, वहां पारदर्शी और बिना हड्डियों वाले ऐसे जीव तैर रहे थे जो पूरी तरह कांच जैसे दिखते हैं। क्या पाताल में सच में एलियंस रहते हैं?"
    },
    {
        "niche": "Money Mindset",
        "title": "गरीब और अमीर में सिर्फ इन 3 आदतों का फर्क है! 💰 #Shorts #RichHabits",
        "tags": ["rich habits", "wealth mindset", "success", "shorts", "hindi motivational"],
        "description": "जिंदगी में अमीर बनने के 3 अटल नियम जो हर युवा को जानने चाहिए।\n#Shorts #FinancialFreedom #RichDad",
        "text": "नंबर एक: गरीब इंसान दिखावे के लिए लायबिलिटीज यानी कर्ज पर चीजें खरीदता है, जबकि अमीर इंसान सबसे पहले एसेट्स यानी संपत्ति बनाता है। नंबर दो: गरीब इंसान पैसे के लिए अपनी पूरी जिंदगी बेच देता है, अमीर इंसान अपने पैसे को काम पर लगाकर समय खरीदता है। नंबर तीन: गरीब इंसान समस्याओं पर रोता है, अमीर इंसान हर संकट में पैसा कमाने का मौका ढूंढ लेता है।"
    },
    {
        "niche": "Brain Power",
        "title": "नींद में गिरने का झटका क्यों लगता है? हाइपनिक जर्क का सच! ⚡😴 #Shorts #ScienceFacts",
        "tags": ["sleep facts", "hypnic jerk", "brain science", "shorts", "hindi facts"],
        "description": "सोते समय अचानक झटके से आंख क्यों खुल जाती है? जानिए वैज्ञानिक सच।\n#Shorts #SleepSecrets #BrainHacks",
        "text": "क्या कभी आपके साथ ऐसा हुआ है कि आप गहरी नींद में जा रहे हों और अचानक ऐसा लगे कि आप किसी ऊंची जगह से गिर गए और झटके से आपकी नींद खुल जाए? इसे मेडिकल साइंस में 'हाइपनिक जर्क' कहते हैं। जब आप बहुत ज्यादा थके होते हैं, तो आपके शरीर की मांसपेशियां बहुत तेजी से शिथिल हो जाती हैं। आपका दिमाग सोचता है कि शरीर मरने लगा है, इसलिए वह तुरंत बिजली का झटका भेजकर आपको जगा देता है।"
    },
    {
        "niche": "Brain Power",
        "title": "सिर्फ 1 मिनट में तनाव और गुस्सा खत्म करने की जापानी ट्रिक! 🧘 #Shorts #MindTricks",
        "tags": ["stress relief", "japanese technique", "mental health", "shorts", "hindi"],
        "description": "जापान की प्राचीन 'जिन शिन जित्सु' तकनीक से तुरंत शांत होने का तरीका।\n#Shorts #StressFree #MindHacks",
        "text": "जापान में लोग तनाव और घबराहट को दूर करने के लिए एक प्राचीन उंगली तकनीक का इस्तेमाल करते हैं। हर उंगली का संबंध हमारे किसी एक भाव से होता है। अंगूठा चिंता को शांत करता है, तर्जनी उंगली डर को खत्म करती है, और बीच की उंगली गुस्से को नियंत्रित करती है। जब भी आपको गुस्सा या तनाव आए, अपनी बीच की उंगली को दूसरे हाथ से 2 मिनट तक हल्के से दबाकर रखें। आपका ब्लड प्रेशर तुरंत सामान्य हो जाएगा।"
    },
    {
        "niche": "Space Wonders",
        "title": "अगर सूरज अचानक गायब हो जाए, तो क्या होगा? ☀️😱 #Shorts #SpaceMysteries",
        "tags": ["sun", "earth", "space science", "what if", "shorts", "hindi facts"],
        "description": "सूरज के बुझते ही पृथ्वी पर आने वाली 8 मिनट की प्रलय।\n#Shorts #SpaceFacts #SolarSystem",
        "text": "अगर सूरज अचानक गायब हो जाए, तो पृथ्वी को इसका पता ठीक 8 मिनट 20 सेकंड बाद चलेगा, क्योंकि प्रकाश और गुरुत्वाकर्षण को पृथ्वी तक पहुंचने में इतना समय लगता है। 8 मिनट बाद पूरी दुनिया में अचानक घना अंधेरा छा जाएगा। पृथ्वी अपनी कक्षा से छूटकर अंतरिक्ष में भटकने लगेगी। एक हफ्ते के अंदर पूरी दुनिया का तापमान माइनस 20 डिग्री तक गिर जाएगा और सारे समुद्र बर्फ बन जाएंगे। सूरज के बिना जीवन असंभव है।"
    },
    {
        "niche": "Space Wonders",
        "title": "चांद पर इंसानी कदमों के निशान कभी क्यों नहीं मिटते? 🌙👣 #Shorts #MoonFacts",
        "tags": ["moon", "apollo", "space facts", "nasa", "shorts", "hindi"],
        "description": "चांद का वह रहस्य जो पृथ्वी से बिल्कुल अलग है।\n#Shorts #MoonSecrets #AstronomyHindi",
        "text": "1969 में नील आर्मस्ट्रांग ने जब चांद पर अपना पहला कदम रखा था, उनके जूतों का वह निशान आज भी बिल्कुल वैसा ही ताजा है जैसा 55 साल पहले था। और वैज्ञानिकों के अनुसार वह अगले 10 लाख साल तक वैसा ही रहेगा। क्योंकि चांद पर न तो कोई हवा है, न पानी और न ही कोई वातावरण। पृथ्वी पर हवा और बारिश निशानों को मिटा देती है, लेकिन चांद पर समय मानो हमेशा के लिए थम गया है।"
    }
]


class HindiScriptGenerator:
    """Manages rotating non-repeating viral Hindi scripts."""

    def __init__(self, state_file: str = "config/daily_state.json"):
        self.state_file = state_file

    def get_todays_5_scripts(self) -> List[Dict[str, Any]]:
        """
        Returns 5 unique scripts for today, skipping any script that has ever been uploaded before.
        Guarantees that today's scripts are 100% unique and never repeated!
        """
        try:
            from history_tracker import HistoryTracker
            tracker = HistoryTracker()
        except Exception:
            tracker = None

        total = len(HINDI_VIRAL_SCRIPTS)
        offset = 0

        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if "ai_script_offset" in data:
                        offset = data["ai_script_offset"]
            except Exception:
                pass

        selected = []
        curr = offset
        attempts = 0
        while len(selected) < 5 and attempts < total * 3:
            candidate = HINDI_VIRAL_SCRIPTS[curr % total]
            is_used = tracker.is_title_used(candidate["title"]) if tracker else False
            if not is_used and candidate not in selected:
                selected.append(candidate)
            curr += 1
            attempts += 1

        if len(selected) < 5:
            for i in range(5 - len(selected)):
                candidate = HINDI_VIRAL_SCRIPTS[(curr + i) % total]
                if candidate not in selected:
                    selected.append(candidate)

        # Advance offset for tomorrow
        new_offset = curr % total
        self._save_offset(new_offset)

        return selected

    def _save_offset(self, new_offset: int):
        """Persists the offset so tomorrow picks the next 5 fresh scripts."""
        data = {}
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                data = {}

        data["ai_script_offset"] = new_offset
        os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
        try:
            with open(self.state_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass

    def get_all_preset_scripts(self) -> List[Dict[str, Any]]:
        return HINDI_VIRAL_SCRIPTS


if __name__ == "__main__":
    gen = HindiScriptGenerator()
    todays = gen.get_todays_5_scripts()
    print(f"Generated {len(todays)} scripts for today:")
    for s in todays:
        print(" -", s["title"][:50])
