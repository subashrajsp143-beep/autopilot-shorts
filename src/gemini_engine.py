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
                    return json.loads(raw_text)
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
