"""
Zack Explainer Engine (Channel 1: MiniTalesWorld)
-------------------------------------------------
Renders Zack D. Films-style animated X-ray & body/science explainers in Hindi
fully in code using zack_engine/ (Node + Headless Chrome + ffmpeg + numpy/scipy)
with natural ElevenLabs Hindi narration + exact character-to-word captions
(and seamless edge-tts / gTTS fallback).
"""

import asyncio
import json
import os
import random
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import numpy as np
from scipy.io import wavfile

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from src.thumbnail_generator import ThumbnailGenerator
from src.elevenlabs_tts import synthesize_line_pcm_and_words


HERO_THEMES = [
    {"skin": "#E8B89A", "skinShade": "#D49C7E", "shirt": "#3A7BD5", "shirtShade": "#2F67BE", "hair": "#3B2A20", "hairHi": "#5A4030", "bg": "#F4F1EA"},
    {"skin": "#D99B78", "skinShade": "#BE7E5C", "shirt": "#E05A47", "shirtShade": "#BA4232", "hair": "#1C1A19", "hairHi": "#3B3734", "bg": "#EEF3F7"},
    {"skin": "#F2C8AC", "skinShade": "#DCA787", "shirt": "#2E9F75", "shirtShade": "#217E5B", "hair": "#6E472B", "hairHi": "#8C5D3B", "bg": "#F7F3E8"},
    {"skin": "#C68662", "skinShade": "#A86B49", "shirt": "#6C5CE7", "shirtShade": "#5344C4", "hair": "#18181C", "hairHi": "#34343D", "bg": "#F2EEF7"},
    {"skin": "#EBC2A6", "skinShade": "#D2A07E", "shirt": "#E67E22", "shirtShade": "#C26415", "hair": "#4A3525", "hairHi": "#6B4E38", "bg": "#F5F2EB"},
]

FALLBACK_ZACK_TOPICS = [
    {
        "subject_key": "hold_sneeze_pressure",
        "title": "छींक रोकने पर शरीर में क्या फट सकता है? 🤧😱 #Shorts",
        "description": "छींक रोकना आपके शरीर और दिमाग के लिए कितना खतरनाक हो सकता है?\n\n#Shorts #Science #ZackDFilms #HindiFacts #BodyFacts",
        "tags": ["shorts", "science", "bodyfacts", "hindifacts", "viral", "sneeze"],
        "music": "tension",
        "banner": "DON'T HOLD SNEEZE! 🤧",
        "lines": [
            {"text": "क्या होगा अगर आप छींक आने पर अपनी नाक बंद करके उसे रोक लें?", "caps": "छींक *रोकने पर | *क्या होगा?", "scene": "hook_shock", "pill": "", "sfx": "pop"},
            {"text": "एक छींक आपके फेफड़ों से करीब सौ मील प्रति घंटे की रफ्तार से बाहर निकलती है।", "caps": "100 MPH *की | रफ्तार से *हवा", "scene": "xray_lungs", "pill": "100 MPH AIR", "sfx": "whoosh"},
            {"text": "जब आप इसे अंदर दबाते हैं, तो हवा का पूरा दबाव गले और कान की नलियों में चला जाता है।", "caps": "*दबाव कान | में *जाता है", "scene": "xray_brain", "pill": "PRESSURE ↑", "sfx": "alarm"},
            {"text": "इससे आपके कान का पर्दा तक फट सकता है और चक्कर आ सकते हैं।", "caps": "कान का *पर्दा | फट *सकता है", "scene": "myth_bust", "pill": "DANGER!", "sfx": "slam"},
            {"text": "यही नहीं, अचानक बढ़ा दबाव दिमाग की बारीक नसों पर भी जोर डाल सकता है।", "caps": "दिमाग की *नसें | *खतरे में", "scene": "blood_vessel", "pill": "BLOOD FLOW ↑", "sfx": "bubbles"},
            {"text": "इतने दबाव से आपकी दिल की धड़कन कुछ पलों के लिए तेज हो जाती है।", "caps": "दिल की *धड़कन | *तेज होती है", "scene": "xray_heart", "pill": "HEART ↑", "sfx": "heartbeat"},
            {"text": "तो अगली बार छींक आए तो टिशू या कोहनी में खुले तौर पर छींकें, उसे रोकें नहीं।", "caps": "कभी *रोकें नहीं | *सुरक्षित रहें", "scene": "outro_twist", "pill": "STAY SAFE", "sfx": "sparkle"},
        ],
    },
    {
        "subject_key": "no_sleep_seven_days",
        "title": "अगर आप 7 दिन तक न सोएं तो दिमाग के साथ क्या होगा? 🧠⚠️ #Shorts",
        "description": "नींद के बिना सात दिन रहने पर इंसान के शरीर और दिमाग में क्या बदलाव आते हैं?\n\n#Shorts #SleepScience #Brain #HindiFacts #Viral",
        "tags": ["shorts", "sleep", "brain", "science", "hindifacts", "viral"],
        "music": "tension",
        "banner": "7 DAYS NO SLEEP 🧠",
        "lines": [
            {"text": "क्या होगा अगर आप लगातार सात दिनों तक बिल्कुल भी न सोएं?", "caps": "7 दिन *बिना | *नींद के?", "scene": "hook_shock", "pill": "", "sfx": "pop"},
            {"text": "पहले चौबीस घंटों में आपका दिमाग नशे जैसी हालत में आ जाता है और फोकस टूटने लगता है।", "caps": "24 *घंटे | फोकस *खत्म", "scene": "clock_pass", "pill": "24 HOURS", "sfx": "tock"},
            {"text": "अड़तालीस घंटों के बाद आपका शरीर माइक्रो स्लीप लेने लगता है, यानी आंखें खुली रहते हुए भी दिमाग सो जाता है।", "caps": "दिमाग *माइक्रो | स्लीप *लेता है", "scene": "xray_brain", "pill": "MICRO SLEEP", "sfx": "alarm"},
            {"text": "खून में स्ट्रेस हार्मोन कोर्टिसोल तेजी से बढ़ने लगता है और इम्यून सिस्टम कमजोर हो जाता है।", "caps": "*स्ट्रेस हार्मोन | तेजी से *बढ़ता", "scene": "blood_vessel", "pill": "CORTISOL ↑", "sfx": "bubbles"},
            {"text": "चौथे दिन तक आपको अजीब आवाजें और परछाइयां दिखने लग सकती हैं जिन्हें हैलुसिनेशन कहते हैं।", "caps": "चौथे *दिन | अजीब *भ्रम", "scene": "myth_bust", "pill": "HALLUCINATION", "sfx": "slam"},
            {"text": "इतने तनाव से आपके दिल पर भी भारी दबाव पड़ता है और ब्लड प्रेशर बढ़ जाता है।", "caps": "दिल पर *दबाव | *बढ़ जाता है", "scene": "xray_heart", "pill": "BP HIGH ↑", "sfx": "heartbeat"},
            {"text": "इसलिए रोज कम से कम सात से आठ घंटे की गहरी नींद लेना आपके दिमाग के लिए बेहद जरूरी है।", "caps": "8 घंटे *नींद | बेहद *जरूरी", "scene": "outro_twist", "pill": "SLEEP 8 HRS", "sfx": "sparkle"},
        ],
    },
]


class ZackExplainerEngine:
    """Self-contained Zack D. Films-style Hindi video & thumbnail generator."""

    SR = 48000

    def __init__(self, engine_dir: str = "zack_engine", output_dir: str = "output/batch_today/channel_1"):
        self.engine_dir = Path(engine_dir).resolve()
        self.output_dir = Path(output_dir).resolve()
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.thumb_gen = ThumbnailGenerator(output_dir=str(self.output_dir))

    @staticmethod
    async def _tts_line(
        text: str,
        tmp_dir: Path,
        idx: int,
        voice: str = "explainer",
        previous_text: Optional[str] = None,
        next_text: Optional[str] = None,
        emotion: Optional[str] = None,
    ) -> Tuple[np.ndarray, List[Dict[str, Any]], str]:
        fallback_attempts = [
            ("hi-IN-MadhurNeural", "+6%", "+0Hz"),
            ("hi-IN-SwaraNeural", "+6%", "+0Hz"),
        ]
        if voice and "-" in voice and "neural" in voice.lower():
            fallback_attempts.insert(0, (voice, "+6%", "+0Hz"))
        pcm, words, backend = await synthesize_line_pcm_and_words(
            text=text,
            tmp_dir=tmp_dir,
            stem=f"line_{idx}",
            role_or_voice=voice,
            emotion=emotion,
            previous_text=previous_text,
            next_text=next_text,
            edge_attempts=fallback_attempts,
            default_fallback_text="आगे देखिए।",
        )
        return pcm, words, backend

    async def _build_narration_and_timing(
        self, lines: List[Dict[str, Any]], voice: str = "explainer", lead: float = 0.28, gap: float = 0.20, outro: float = 0.75
    ) -> Tuple[np.ndarray, Dict[str, Any], Dict[str, Any]]:
        data_dir = self.engine_dir / "data"
        data_dir.mkdir(parents=True, exist_ok=True)

        chunks: List[Tuple[np.ndarray, List[Dict[str, Any]], str]] = []
        used_backends: List[str] = []
        for idx, ln in enumerate(lines):
            prev_txt = lines[idx - 1]["text"] if idx > 0 else None
            next_txt = lines[idx + 1]["text"] if idx + 1 < len(lines) else None
            emotion = ln.get("pose") or ln.get("emotion")
            pcm, words, backend = await self._tts_line(
                ln["text"],
                data_dir,
                idx,
                voice=voice,
                previous_text=prev_txt,
                next_text=next_txt,
                emotion=emotion,
            )
            chunks.append((pcm, words, ln["text"]))
            used_backends.append(backend)

        cursor = lead
        line_entries = []
        word_entries = []
        total_samples = int((lead + outro + sum(len(c[0]) / self.SR + gap for c in chunks)) * self.SR) + self.SR // 2
        full_audio = np.zeros((total_samples, 2), dtype=np.int16)

        for idx, (pcm, words, text) in enumerate(chunks):
            dur = len(pcm) / self.SR
            start_s = cursor
            end_s = start_s + dur
            s_idx = int(start_s * self.SR)
            e_idx = min(s_idx + len(pcm), total_samples)
            full_audio[s_idx:e_idx] = pcm[: e_idx - s_idx]

            line_entries.append({"i": idx, "text": text, "start": round(start_s, 3), "end": round(end_s, 3)})
            for w in words:
                word_entries.append({
                    "line": idx,
                    "w": w["w"],
                    "s": round(start_s + w["s"], 3),
                    "e": round(start_s + w["e"], 3),
                })
            cursor = end_s + gap

        total_dur = round(cursor - gap + outro, 3)
        trim_samples = int(total_dur * self.SR)
        full_audio = full_audio[:trim_samples]

        active_voice = used_backends[0] if used_backends else voice
        print(f"🎙️ ZackExplainer TTS backend: {active_voice}")
        lines_json = {"duration": total_dur, "voice": active_voice, "speed": 1.0, "lines": line_entries}
        return full_audio, lines_json, word_entries

    def render_short(
        self,
        blueprint: Dict[str, Any],
        output_video_path: str,
        output_thumb_path: str,
        slot_index: int = 1,
        tracker=None,
        batch_hashes: Optional[Set[str]] = None,
    ) -> Dict[str, Any]:
        """Renders full 1080x1920 explainer video + guaranteed unique thumbnail."""
        data_dir = self.engine_dir / "data"
        data_dir.mkdir(parents=True, exist_ok=True)

        lines = blueprint.get("lines", [])
        if not lines:
            raise ValueError("Storyboard blueprint must contain at least 1 line")

        # 1. Generate Hindi narration + millisecond WordBoundary alignment
        full_audio, lines_json, words_json = asyncio.run(self._build_narration_and_timing(lines))
        wavfile.write(data_dir / "narration.wav", self.SR, full_audio)
        (data_dir / "lines.json").write_text(json.dumps(lines_json, ensure_ascii=False, indent=2), encoding="utf-8")
        (data_dir / "words.json").write_text(json.dumps(words_json, ensure_ascii=False, indent=2), encoding="utf-8")

        # 2. Write script.json + data/storyboard.json with unique hero visual theme
        theme = HERO_THEMES[(slot_index + random.randint(0, len(HERO_THEMES) - 1)) % len(HERO_THEMES)]
        script_json = {
            "title": blueprint.get("title", "Amazing Body Science"),
            "voice": lines_json.get("voice", "elevenlabs"),
            "music": blueprint.get("music", "tension"),
            "lines": [{"text": ln["text"], "caps": ln.get("caps", "")} for ln in lines],
        }
        storyboard_json = {
            "hero_theme": theme,
            "lines": [
                {
                    "scene": ln.get("scene", "hook_shock"),
                    "pill": ln.get("pill", ""),
                    "sfx": ln.get("sfx", "whoosh"),
                }
                for ln in lines
            ],
        }
        (self.engine_dir / "script.json").write_text(json.dumps(script_json, ensure_ascii=False, indent=2), encoding="utf-8")
        (data_dir / "storyboard.json").write_text(json.dumps(storyboard_json, ensure_ascii=False, indent=2), encoding="utf-8")

        # 3. Extract sound cues + synthesize procedural audio bed/SFX mix
        subprocess.run(["node", "tools/capture.mjs", "cues"], cwd=str(self.engine_dir), check=True)
        subprocess.run([sys.executable, "tools/mix.py", "."], cwd=str(self.engine_dir), check=True)

        # 4. Render 1080x1920 30fps MP4 via headless Chrome -> ffmpeg
        out_vid_abs = Path(output_video_path).resolve()
        out_vid_abs.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["node", "tools/capture.mjs", "video", str(out_vid_abs)], cwd=str(self.engine_dir), check=True)

        # 5. Extract clean caption-free & pill-free cover frames from 3 peak scenes, then enforce dHash uniqueness
        dur = float(lines_json["duration"])
        probe_times = [round(dur * k, 2) for k in (0.30, 0.52, 0.72, 0.16)]
        clean_dir = data_dir / "clean_thumbs"
        for old_f in clean_dir.glob("*.jpg"):
            old_f.unlink(missing_ok=True)
        subprocess.run(
            ["node", "tools/capture.mjs", "frames", "data/clean_thumbs", ",".join(map(str, probe_times)), "--clean"],
            cwd=str(self.engine_dir),
            check=True,
        )
        clean_imgs = sorted(clean_dir.glob("*.jpg"))
        thumb_path = ""
        for idx_c, c_img in enumerate(clean_imgs or [out_vid_abs]):
            candidate_thumb = self.thumb_gen.generate(
                video_path=str(c_img),
                output_thumb_path=str(Path(output_thumb_path).resolve()),
                badge_text=blueprint.get("banner", "WHAT HAPPENS IF?"),
                timestamp_sec=probe_times[0],
                slot_index=slot_index + idx_c,
                tracker=tracker,
                batch_hashes=batch_hashes,
            )
            if candidate_thumb:
                thumb_path = candidate_thumb
                break

        return {
            "video_path": str(out_vid_abs),
            "thumbnail_path": thumb_path,
            "thumbnail_dhash": self.thumb_gen.last_dhash,
            "duration": float(lines_json["duration"]),
            "title": blueprint["title"],
            "description": blueprint["description"],
            "tags": blueprint.get("tags", ["shorts", "viral", "facts", "science"]),
            "subject_key": blueprint.get("subject_key", ""),
        }
