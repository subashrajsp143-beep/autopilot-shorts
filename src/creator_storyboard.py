"""
Creator Storyboard Engine
Fetches real creator photos (MrBeast, Islands, Desert, Vault, Trophy)
and stitches them into dynamic multi-scene 9:16 vertical videos with voiceover and subtitles.
NEVER uses blank color backgrounds.
"""

import os
import requests
import subprocess
from typing import List, Dict, Any

USER_AGENT = "AutopilotShorts/1.0 (mailto:subashkum05@gmail.com)"

CREATOR_SCENE_MAP = {
    "island": ["MrBeast", "Tropical_island", "Yacht", "Wealth"],
    "desert": ["MrBeast", "Sahara", "Sun", "Water"],
    "challenge": ["MrBeast", "Bank_vault", "Competition", "Trophy"],
    "advice": ["Microphone", "The_Thinker", "Hourglass", "Cityscape"],
    "anvil": ["Anvil", "Cloud", "Explosion", "Science"]
}

CREATOR_SCRIPTS_HINDI = [
    {
        "key": "island",
        "title": "मिस्टर बीस्ट ने दिया 50 करोड़ का प्राइवेट आइलैंड! 🏝️ #Shorts #MrBeastHindi",
        "description": "मिस्टर बीस्ट का अब तक का सबसे महंगा चैलेंज!\n\n#Shorts #MrBeast #MrBeastHindi #Viral",
        "tags": ["mrbeast", "mrbeast hindi", "private island", "shorts", "viral"],
        "text": "मिस्टर बीस्ट ने एक अनजान सब्सक्राइबर को पचास करोड़ का पूरा प्राइवेट आइलैंड फ्री में दे दिया। इस विशाल आइलैंड पर सुंदर समुद्र, नारियल के पेड़ और अपना खुद का प्राइवेट बीच था। लेकिन इसे जीतने के लिए कंटेस्टेंट्स को कई मुश्किल चुनौतियों का सामना करना पड़ा। अंत में जिस प्रतियोगी ने हार नहीं मानी, वह पूरे आइलैंड का अकेला मालिक बन गया। क्या आप ऐसे चैलेंज में हिस्सा लेना चाहेंगे?"
    },
    {
        "key": "desert",
        "title": "रेगिस्तान में 100 घंटे तक बिना पानी के कैसे बचे? 🏜️ #Shorts #MrBeastHindi",
        "description": "मिस्टर बीस्ट का सबसे खतरनाक डेजर्ट सर्वाइवल चैलेंज!\n\n#Shorts #MrBeast #Survival #Viral",
        "tags": ["mrbeast", "survival", "desert", "shorts", "viral"],
        "text": "क्या कोई इंसान पचास डिग्री की भीषण गर्मी में सौ घंटे तक रेगिस्तान में जिंदा रह सकता है? मिस्टर बीस्ट और उनकी टीम ने दुनिया के सबसे गर्म रेगिस्तान में खुद को बिना किसी सुविधा के छोड़ दिया। दिन में तेज धूप और रात में जानलेवा ठंड ने सबकी हालत खराब कर दी। लेकिन सही सर्वाइवल तकनीक और टीम वर्क की मदद से उन्होंने इस जानलेवा चैलेंज को पूरा कर दिखाया। इंसान की सहनशक्ति सच में हैरान करने वाली है।"
    },
    {
        "key": "challenge",
        "title": "10 लाख डॉलर का सबसे बड़ा चैलेंज! 💰 #Shorts #MrBeastHindi",
        "description": "दस लाख डॉलर का ऐसा खेल जिसे देखकर सबके होश उड़ गए।\n\n#Shorts #MrBeast #MillionDollarChallenge #Viral",
        "tags": ["mrbeast", "million dollars", "challenge", "shorts", "viral"],
        "text": "कांच के बक्से में रखे दस लाख डॉलर यानी आठ करोड़ रुपये कैश। नियम बिल्कुल साधारण था: जो भी आखिरी इंसान हाथ इस पैसे से हटाएगा, वह खाली हाथ घर जाएगा और जो सबसे अंत तक हाथ टिकाए रखेगा, सारा पैसा उसका हो जाएगा। बत्तीस घंटे तक बिना सोए और बिना हिले खड़े रहने के बाद एक आम लड़के ने यह सारा पैसा जीत लिया। कभी-कभी सिर्फ एक फैसला आपकी पूरी जिंदगी बदल देता है।"
    },
    {
        "key": "advice",
        "title": "20 की उम्र में यह एक गलती आपकी पूरी जिंदगी बर्बाद कर देगी! 💡 #Shorts #Motivation",
        "description": "पॉडकास्ट की यह सबसे ताकतवर सलाह जो हर युवा को सुननी चाहिए।\n\n#Shorts #LifeLessons #MotivationHindi #Success",
        "tags": ["motivation", "life advice", "podcast clips", "success", "shorts"],
        "text": "दुनिया के सबसे सफल अरबपतियों का कहना है कि बीस से तीस की उम्र में लोग सबसे बड़ी गलती यह करते हैं कि वे दूसरों को खुश करने के लिए पैसे खर्च करते हैं। महंगे फोन और ब्रांडेड कपड़े खरीदने की बजाय, अपनी स्किल्स और नॉलेज में निवेश करें। जो समय आप दूसरों की रील्स देखने में गंवा रहे हैं, वही समय कुछ नया सीखने में लगाएं। दस साल बाद आपकी मेहनत आपको दूसरों से मीलों आगे खड़ा कर देगी।"
    },
    {
        "key": "anvil",
        "title": "हजार फीट की ऊंचाई से लोहे का एनविल गिराने पर क्या हुआ? 💥 #Shorts #CrazyScience",
        "description": "धीमी गति में देखिए भयानक विनाश का यह अद्भुत विज्ञान प्रयोग!\n\n#Shorts #PhysicsExperiment #SlowMotion #Science",
        "tags": ["physics", "experiment", "slow motion", "shorts", "destruction"],
        "text": "जब दो सौ किलो वजनी लोहे के एनविल को एक हजार फीट की ऊंचाई से जमीन पर गिराया गया, तो भौतिकी के नियमों ने कुछ ऐसा दिखाया जो आपने कभी नहीं देखा होगा। हवा की गति पकड़ते ही एनविल गोली की रफ्तार से नीचे गिरा और जमीन से टकराते ही तीन फीट गहरा गड्ढा बना दिया। वैज्ञानिकों ने हाई-स्पीड कैमरों से जब इस टक्कर को देखा, तो ऊर्जा का ऐसा विस्फोट हुआ जिसने पत्थरों को भी धूल बना दिया। गुरुत्वाकर्षण की ताकत वाकई असीम है।"
    }
]


class CreatorStoryboard:
    """Creates rich multi-scene creator videos with real imagery & Ken Burns motion."""

    def __init__(self, cache_dir: str = "assets/image_cache"):
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)

    def fetch_image(self, query: str) -> str:
        """Fetches HD image from Wikipedia API."""
        filename = f"{query}.jpg"
        local_path = os.path.join(self.cache_dir, filename)
        if os.path.exists(local_path):
            return local_path

        try:
            url = f"https://en.wikipedia.org/w/api.php?action=query&titles={query}&prop=pageimages&format=json&pithumbsize=1080"
            r = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=5)
            if r.status_code == 200:
                pages = r.json().get("query", {}).get("pages", {})
                for p in pages.values():
                    thumb = p.get("thumbnail", {}).get("source")
                    if thumb:
                        img_data = requests.get(thumb, headers={"User-Agent": USER_AGENT}, timeout=8).content
                        with open(local_path, "wb") as f:
                            f.write(img_data)
                        return local_path
        except Exception as e:
            print(f"Error fetching {query}: {e}")

        # Fallback to MrBeast photo
        return os.path.join(self.cache_dir, "MrBeast.jpg")

    def build_creator_video_background(self, key: str, duration: float, output_path: str) -> str:
        """Stitches 4 real scenes with Ken Burns effect for creator video."""
        scene_queries = CREATOR_SCENE_MAP.get(key, ["MrBeast", "Trophy", "Wealth", "Competition"])
        clip_duration = duration / len(scene_queries)
        clips = []

        for i, q in enumerate(scene_queries):
            img_path = self.fetch_image(q)
            clip_file = os.path.join(self.cache_dir, f"creator_{key}_{i}.mp4")

            # Ken Burns slow zoom
            cmd = [
                "ffmpeg", "-y",
                "-loop", "1",
                "-i", img_path,
                "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,zoompan=z='min(zoom+0.0014,1.20)':d=125:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920",
                "-t", f"{clip_duration:.2f}",
                "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", "-r", "30",
                clip_file
            ]
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if res.returncode != 0:
                # fallback simple crop
                cmd_simple = [
                    "ffmpeg", "-y", "-loop", "1", "-i", img_path,
                    "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
                    "-t", f"{clip_duration:.2f}",
                    "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", "-r", "30",
                    clip_file
                ]
                subprocess.run(cmd_simple, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            clips.append(clip_file)

        # Concat clips
        concat_txt = os.path.join(self.cache_dir, f"concat_{key}.txt")
        with open(concat_txt, "w", encoding="utf-8") as f:
            for c in clips:
                clean = os.path.abspath(c).replace("\\", "/")
                f.write(f"file '{clean}'\n")

        cmd_concat = [
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0", "-i", concat_txt,
            "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p",
            output_path
        ]
        subprocess.run(cmd_concat, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return output_path
