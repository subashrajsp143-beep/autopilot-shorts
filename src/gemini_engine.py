"""
Gemini AI Engine for High-Retention YouTube Shorts
Powered by Google Gemini (Multi-model resilient fallback: gemini-3.6-flash, gemini-3.1-flash-lite, etc.)
Generates:
1. FactTechz-style psychological hooks & high-retention Hindi scripts
2. Dynamic B-roll visual theme tagging
3. High-CTR Hindi titles, descriptions, and hashtags
4. Top hook banner headlines for 0-second scroll stopping
"""

import os
import sys
import json
import base64
import re
import requests
from typing import Dict, Any, List, Optional

# UTF-8 fix for Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


class GeminiEngine:
    """Interface to Gemini for viral short-form script & metadata generation."""

    CANDIDATE_MODELS = [
        "gemini-3.6-flash",
        "gemini-3.1-flash-lite",
        "gemini-3-flash-preview",
        "gemini-3.5-flash"
    ]

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            self._load_key_from_credentials()

    def _load_key_from_credentials(self):
        """Attempts to load Gemini API key from credentials.dat bundle."""
        dat_path = "config/credentials.dat"
        if os.path.exists(dat_path):
            try:
                with open(dat_path, "r", encoding="utf-8") as f:
                    encoded = f.read().strip()
                payload = json.loads(base64.b85decode(encoded.encode("utf-8")).decode("utf-8"))
                if "gemini_api_key" in payload:
                    self.api_key = payload["gemini_api_key"]
                    os.environ["GEMINI_API_KEY"] = self.api_key
            except Exception as e:
                print(f"Notice: Could not extract Gemini key from credentials.dat: {e}")

    def is_available(self) -> bool:
        return bool(self.api_key)

    def _call_gemini_json(self, prompt: str) -> Dict[str, Any]:
        """Calls Gemini with automatic fallback across candidate models."""
        if not self.api_key:
            raise RuntimeError("Gemini API key is not configured.")

        last_error = "Unknown error"
        for model in self.CANDIDATE_MODELS:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={self.api_key}"
            data = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"response_mime_type": "application/json"}
            }
            try:
                response = requests.post(url, json=data, timeout=20)
                if response.status_code == 200:
                    res_json = response.json()
                    raw_text = res_json["candidates"][0]["content"]["parts"][0]["text"]
                    parsed_obj = json.loads(raw_text)
                    if isinstance(parsed_obj, list) and parsed_obj and isinstance(parsed_obj[0], dict):
                        return parsed_obj[0]
                    return parsed_obj
                else:
                    last_error = f"{model} returned {response.status_code}: {response.text[:120]}"
            except Exception as e:
                last_error = f"{model} error: {e}"

        raise RuntimeError(f"All Gemini candidate models failed. Last error: {last_error}")

    def generate_fact_script(self, niche: str, specific_topic: Optional[str] = None) -> Dict[str, Any]:
        """
        Generates a 30-second viral FactTechz-style Hindi script.
        Returns JSON with:
        - title: High CTR Hindi title under 70 chars with emoji + #Shorts
        - description: Rich description with viral tags
        - tags: 6-8 relevant tags
        - spoken_text: Clean Hindi words ONLY (no brackets, no sound effects)
        - visual_theme: One of dark_psychology, ancient_temple, pyramid, bermuda_ocean, deep_sea, wealth_money, brain_sleep, deep_space
        - top_hook: 2-4 word bold uppercase English/Hindi text for top banner
        """
        topic_instruction = f"Specific topic focus: {specific_topic}" if specific_topic else f"Niche category: {niche}"

        prompt = f"""
You are the world's most successful YouTube Shorts scriptwriter, specializing in FactTechz, Dhruv Rathee, and Zack D. Films style viral shorts in Hindi.
Your goal is 1,000,000+ views with 90%+ audience retention.

{topic_instruction}

CRITICAL RULES:
1. Spoken Duration: Exactly 28 to 33 seconds when spoken out loud (~65 to 80 Hindi words).
2. The Hook (First 2 Seconds): Must shock the viewer with a question or crazy fact that makes it impossible to swipe away.
3. Language: Clean, conversational, engaging Hindi with punchy delivery.
4. spoken_text MUST CONTAIN ONLY WORDS TO BE READ BY TTS. NO stage directions like '[Visual: ...]', NO '[Sound Effect]', NO brackets whatsoever.
5. visual_theme MUST BE STRICTLY ONE OF:
   - "dark_psychology"
   - "ancient_temple"
   - "pyramid"
   - "bermuda_ocean"
   - "deep_sea"
   - "wealth_money"
   - "brain_sleep"
   - "deep_space"
6. top_hook: 2 to 4 bold words in uppercase for the top screen banner (e.g. "MIND CONTROL TRICK ⚠️", "GIZA SECRET 🏛️", "DO NOT SLEEP! 🧠", "10,000 CRORE SECRET 💰").

Return strictly valid JSON with this exact schema:
{{
  "title": "Shocking Hindi Title With Emoji #Shorts",
  "description": "Engaging Hindi description\\n\\n#Shorts #Viral #Facts #FactTechz",
  "tags": ["tag1", "tag2", "tag3", "tag4", "shorts", "viral"],
  "spoken_text": "शुद्ध और रोमांचक हिंदी में बोलने वाला पाठ...",
  "visual_theme": "dark_psychology",
  "top_hook": "BANNER HOOK TEXT"
}}
"""
        parsed = self._call_gemini_json(prompt)

        # Sanitize spoken_text just in case any brackets leaked through
        cleaned_spoken = parsed.get("spoken_text", "")
        cleaned_spoken = re.sub(r'\[.*?\]', '', cleaned_spoken)
        cleaned_spoken = re.sub(r'\(.*?\)', '', cleaned_spoken)
        cleaned_spoken = re.sub(r'\s+', ' ', cleaned_spoken).strip()
        parsed["spoken_text"] = cleaned_spoken

        return parsed

    def generate_creator_metadata(self, niche: str, original_query: str, lang: str = "en") -> Dict[str, Any]:
        """
        Generates high-CTR viral title and top hook banner.
        Strictly enforces:
        - If lang == 'en': 100% English font (Latin script only, ZERO Devanagari) to match English audio.
        - If lang == 'hi': 100% Hindi font (Devanagari) to match Hindi audio (MrBeast Hindi / Cricket).
        """
        is_hindi = lang == "hi" or "hindi" in niche.lower() or "cricket" in niche.lower()

        if is_hindi:
            title_rule = """CRITICAL: The audio is in HINDI (MrBeast Official Hindi Dubbed or Cricket Hindi Commentary).
Title MUST BE IN HINDI (Devanagari script) with high curiosity shock hook under 65 chars with emojis + #Shorts.
Examples:
- 'मिस्टर बीस्ट ने दिया $1,000,000 का सबसे बड़ा गिफ्ट! 💰😱 #Shorts #MrBeastHindi'
- 'विराट कोहली का यह गुस्सा देखकर सब दंग रह गए! 😱🔥 #Shorts #ViratKohli'"""
            fallback_title = f"{niche.replace('_', ' ').title()} का सबसे हैरान कर देने वाला वीडियो! 😱🔥 #Shorts"
        else:
            title_rule = """CRITICAL: The audio is in ENGLISH (Ronaldo, Messi, Speed, Football).
Title MUST BE 100% IN ENGLISH FONT (Latin letters ONLY, STRICTLY ZERO DEVANAGARI CHARACTERS).
Examples:
- 'When Cristiano Ronaldo Scored That Impossible Goal! 😱⚽ #Shorts #Ronaldo'
- 'IShowSpeed Craziest Reaction Ever On Live Stream! 😂🔥 #Shorts #Speed'
- 'Lionel Messi Magic Dribble That Broke 4 Defenders! 😱👑 #Shorts #Messi'"""
            fallback_title = f"{niche.replace('_', ' ').title()} Most INSANE Viral Moment! 😱🔥 #Shorts"

        prompt = f"""
You are an expert YouTube title and thumbnail optimizer for viral shorts (Ronaldo, Messi, Speed, MrBeast, Cricket).
Niche: {niche}
Video query/topic: {original_query}

{title_rule}

Generate:
1. title: Under 65 chars with shock emoji + #Shorts (following the strict language rule above)
2. banner: 3-5 word high energy bold uppercase English text for the top hook banner (e.g. 'RONALDO IMPOSSIBLE GOAL! ⚽', 'MRBEAST $1M CHALLENGE! 💰')
3. description: Short 2-line description with 5 trending hashtags

Return strictly valid JSON:
{{
  "title": "...",
  "banner": "...",
  "description": "..."
}}
"""
        try:
            return self._call_gemini_json(prompt)
        except Exception as e:
            print(f"Notice: Gemini creator metadata generation failed ({e}), using default.")

        return {
            "title": fallback_title,
            "banner": f"{niche.upper().replace('_', ' ')} UNBELIEVABLE MOMENT! 💥",
            "description": f"{niche.replace('_', ' ').title()} viral moment.\n\n#Shorts #Viral #Trending"
        }

    def generate_zack_explainer(
        self,
        niche: str,
        used_titles: Optional[List[str]] = None,
        used_subjects: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Generates a Zack D. Films style "What happens if...?" Hindi explainer storyboard
        with strict topic uniqueness and per-cut visual scene choreography.
        """
        avoid_titles = (used_titles or [])[-40:]
        avoid_subjects = (used_subjects or [])[-60:]

        prompt = f"""
You are a viral YouTube Shorts writer creating Zack D. Films-style "What happens if...?" explainers in natural conversational HINDI.
Category focus: {niche}

STRICT ANTI-REPEAT RULE:
NEVER repeat or paraphrase any of these previously covered topics/titles:
- Used subject keys: {json.dumps(avoid_subjects, ensure_ascii=False)}
- Recent titles: {json.dumps(avoid_titles, ensure_ascii=False)}

Choose a 100% FRESH, fascinating, scientifically accurate topic (e.g. holding a sneeze, cracking knuckles, drinking 5 energy drinks, staying awake 7 days, swallowing an apple seed, swimming in Dead Sea, brain freeze, ear ringing, hiccups, cold shower shock, zero gravity body changes, deep sea pressure, etc.) that is NOT in the lists above.

STORY & SCRIPT RULES:
1. Write 8 to 10 lines (cuts) totaling ~75 to 95 spoken Hindi words (~28-35 seconds).
2. Line 1 MUST open immediately with a shocking "क्या होगा अगर..." question (0-second hook).
3. Every sentence flows naturally like talking to a friend (no stage directions, no brackets).
4. Write numbers in Hindi words as spoken (e.g. "सात", "तीस", "दो").
5. Each line object must have:
   - "text": pure Hindi Devanagari sentence/clause to be spoken by TTS.
   - "caps": short 1-3 word Hindi/English caption chunks separated by "|", with EXACTLY ONE word per chunk prefixed with "*" for yellow highlight (e.g. "क्या होगा *अगर | आप छींक *रोक लें?"). Keep every chunk under 3 words!
   - "scene": strictly one of ["hook_shock", "xray_lungs", "xray_heart", "xray_brain", "xray_stomach", "blood_vessel", "myth_bust", "clock_pass", "cosmos", "ocean_mystery", "outro_twist"]
   - "pill": optional 1-3 word uppercase badge (e.g. "PRESSURE ↑", "HEART 140 BPM", "BRAIN ALARM", "MYTH BUSTED") or ""
   - "sfx": strictly one of ["pop", "whoosh", "heartbeat", "bubbles", "alarm", "thud", "slide", "sparkle", "slam"]

Return strictly valid JSON:
{{
  "subject_key": "short_unique_snake_case_topic_key",
  "title": "Curiosity Hindi Title Under 70 Chars With Emoji #Shorts",
  "description": "2-line Hindi summary + 6 viral hashtags",
  "tags": ["shorts", "viral", "zackdfilms", "hindifacts", "science", "bodyfacts"],
  "music": "tension",
  "banner": "2-4 UPPERCASE ENGLISH WORDS ONLY (NO HINDI, NO EMOJIS, e.g. 'DONT HOLD SNEEZE!')",
  "lines": [
    {{
      "text": "...",
      "caps": "...",
      "scene": "hook_shock",
      "pill": "",
      "sfx": "pop"
    }}
  ]
}}
"""
        parsed = self._call_gemini_json(prompt)
        # Sanitize lines
        clean_lines = []
        for idx, ln in enumerate(parsed.get("lines", [])):
            txt = re.sub(r'\[.*?\]|\(.*?\)', '', str(ln.get("text", ""))).strip()
            txt = re.sub(r'\s+', ' ', txt)
            if not txt:
                continue
            caps = str(ln.get("caps", "")).strip()
            scene = str(ln.get("scene", "hook_shock")).strip()
            clean_lines.append({
                "text": txt,
                "caps": caps,
                "scene": scene,
                "pill": str(ln.get("pill", "")).strip()[:24],
                "sfx": str(ln.get("sfx", "whoosh")).strip(),
            })
        parsed["lines"] = clean_lines
        return parsed

    def generate_webseries_movie_story(
        self,
        franchise: str,
        used_titles: Optional[List[str]] = None,
        used_subjects: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Generates a 100% original, copyright-safe 2D/3D animated storytelling/parody/what-if
        Hindi script inspired by Indian Web Series (Panchayat, Mirzapur, Scam 1992, Kota Factory,
        Family Man, Gullak) and Iconic Movies (Hera Pheri, 3 Idiots, Stree, KGF, Pushpa, Munna Bhai).
        """
        avoid_titles = (used_titles or [])[-40:]
        avoid_subjects = (used_subjects or [])[-60:]

        prompt = f"""
You are a viral Indian YouTube Shorts animation creator writing hilarious, gripping, copyright-safe
animated scenes/parodies/untold fan-stories inspired by Indian Web Series and Movies.
Target Franchise / Vibe: {franchise}

STRICT ANTI-REPEAT RULE:
NEVER repeat any of these previously covered topics/titles:
- Used subject keys: {json.dumps(avoid_subjects, ensure_ascii=False)}
- Recent titles: {json.dumps(avoid_titles, ensure_ascii=False)}

STORY & DIALOGUE RULES:
1. Write 7 to 9 short punchy Hindi lines (~70 to 90 words total, ~28-35 seconds) as an animated scene (funny "What if...", clever parody twist, untold fan-theory, or iconic character dilemma — 100% original writing, NOT copied verbatim script).
2. Line 1 MUST hook immediately in 0-2 seconds!
3. Choose matching visual set `"world"` strictly from:
   ["panchayat_village", "mirzapur_hall", "scam_office", "college_hostel", "chawl_comedy", "cinema_night"]
4. Choose `"char_a"` and `"char_b"` appearance colors/props matching the characters (e.g. kurta + moustache for village leader, dark blazer + glasses for boss/scammer, bright casual shirt for comedy hero).
5. Each line has:
   - "text": clean conversational Hindi Devanagari line (no stage directions, no brackets, no speaker prefix like "A:")
   - "caps": 1-3 word chunks separated by "|", with ONE "*" yellow highlight word per chunk
   - "speaker": "A", "B", or "narrator"
   - "shot": strictly one of ["two_shot", "closeup_a", "closeup_b", "dramatic_zoom"]
   - "emotion_a": strictly one of ["normal", "shock", "angry", "laugh"]
   - "emotion_b": strictly one of ["normal", "shock", "angry", "laugh"]
   - "pill": optional 1-3 word UPPERCASE ENGLISH reaction tag (e.g. "GAJAB BEZZATI!", "MIRZAPUR TWIST", "25 DIN DOUBLE!", "RISK HAI!") or ""
   - "sfx": strictly one of ["pop", "whoosh", "slam", "boing", "sparkle", "thud", "alarm"]

Return strictly valid JSON:
{{
  "subject_key": "short_unique_snake_case_key",
  "title": "Catchy Hindi Title With Emoji Under 68 Chars #Shorts",
  "description": "2-line engaging Hindi summary + 6 viral hashtags",
  "tags": ["shorts", "viral", "animated", "webseries", "panchayat", "mirzapur", "comedy"],
  "music": "bed",
  "world": "panchayat_village",
  "banner": "2-4 UPPERCASE ENGLISH WORDS ONLY (NO HINDI, NO EMOJIS)",
  "char_a": {{"skin": "#DFA37D", "shirt": "#F8F9FA", "shirtShade": "#DCE2EC", "hair": "#231F20", "moustache": true, "glasses": false, "beard": false}},
  "char_b": {{"skin": "#E6B898", "shirt": "#2E67BE", "shirtShade": "#1F4B94", "hair": "#2D221C", "moustache": false, "glasses": false, "beard": true}},
  "lines": [
    {{"text": "...", "caps": "...", "speaker": "narrator", "shot": "two_shot", "emotion_a": "normal", "emotion_b": "shock", "pill": "", "sfx": "pop"}}
  ]
}}
"""
        parsed = self._call_gemini_json(prompt)
        clean_lines = []
        for ln in parsed.get("lines", []):
            txt = re.sub(r'\[.*?\]|\(.*?\)', '', str(ln.get("text", ""))).strip()
            txt = re.sub(r'^[ABab]\s*:\s*', '', txt)
            txt = re.sub(r'\s+', ' ', txt)
            if not txt:
                continue
            clean_lines.append({
                "text": txt,
                "caps": str(ln.get("caps", "")).strip(),
                "speaker": str(ln.get("speaker", "A")),
                "shot": str(ln.get("shot", "two_shot")),
                "emotion_a": str(ln.get("emotion_a", "normal")),
                "emotion_b": str(ln.get("emotion_b", "normal")),
                "pill": str(ln.get("pill", "")).strip()[:24],
                "sfx": str(ln.get("sfx", "whoosh")).strip(),
            })
        parsed["lines"] = clean_lines
        return parsed


if __name__ == "__main__":
    engine = GeminiEngine()
    if engine.is_available():
        print("Testing Gemini Engine with Fact Script...")
        res = engine.generate_fact_script("Dark Psychology")
        print("Title:", res["title"])
        print("Banner:", res["top_hook"])
        print("Theme:", res["visual_theme"])
        print("Spoken:", res["spoken_text"][:100] + "...")
    else:
        print("Gemini API key not found.")
