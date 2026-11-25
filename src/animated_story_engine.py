"""
Animated Story Engine (Channel 3: Web Series & Movies Animated Scenes)
----------------------------------------------------------------------
Generates 100% original, copyright-safe 2D/3D-shaded animated Hindi Shorts
inspired by Indian Web Series (Panchayat, Mirzapur, Scam 1992, Kota Factory,
The Family Man, Gullak) and Movies (Hera Pheri, 3 Idiots, Stree, KGF, Pushpa).

Features:
- Multi-character animated dialogue with lip-sync + expressive poses
- Natural human-like multi-speaker ElevenLabs TTS (Daniel / George / Sarah)
  with seamless Request Stitching & emotion presets (edge-tts / gTTS fallback)
- Exact millisecond Hindi captions for automatic A/V synchronization
- Custom story worlds (Panchayat village water tank, Mirzapur crimson hall, etc.)
- Guaranteed unique thumbnails via 64-bit dHash check
"""

import asyncio
import json
import os
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


FALLBACK_STORY_TOPICS: List[Dict[str, Any]] = [
    {
        "subject_key": "panchayat_laukki_crypto_twist",
        "title": "फुलेरा गांव में लौकी के बदले क्रिप्टो? 😂🎃 #Shorts #Panchayat",
        "description": "अगर फुलेरा पंचायत में प्रधान जी और सचिव जी को क्रिप्टोकरेंसी समझ आ जाए तो क्या होगा!\n\n#Shorts #Panchayat #Animation #Comedy #HindiShorts #Viral",
        "tags": ["shorts", "panchayat", "animation", "comedy", "hindishorts", "viral"],
        "music": "bed",
        "world": "panchayat_village",
        "banner": "PHULERA CRYPTO TWIST!",
        "char_a": {"skin": "#DFA37D", "shirt": "#F8F9FA", "shirtShade": "#DCE2EC", "hair": "#231F20", "moustache": True, "glasses": False, "beard": False},
        "char_b": {"skin": "#E8B89A", "shirt": "#3A7BD5", "shirtShade": "#2F67BE", "hair": "#3B2A20", "moustache": False, "glasses": False, "beard": False},
        "lines": [
            {"text": "क्या होगा अगर फुलेरा गांव में प्रधान जी लौकी की जगह बिटकॉइन बांटने लगें?", "caps": "फुलेरा में | *लौकी की जगह?", "speaker": "narrator", "shot": "two_shot", "emotion_a": "normal", "emotion_b": "shock", "pill": "PHULERA 2026!", "sfx": "pop"},
            {"text": "अरे सचिव जी, ये कंप्यूटर पर लाल हरी लाइनें क्यों भाग रही हैं?", "caps": "लाल हरी | *लाइनें क्यों?", "speaker": "A", "shot": "closeup_a", "emotion_a": "shock", "emotion_b": "normal", "pill": "", "sfx": "whoosh"},
            {"text": "प्रधान जी, इसे क्रिप्टो मार्केट कहते हैं, पैसा रातों-रात डबल हो जाता है!", "caps": "पैसा *डबल | हो जाता है!", "speaker": "B", "shot": "closeup_b", "emotion_a": "normal", "emotion_b": "laugh", "pill": "DOUBLE MONEY!", "sfx": "sparkle"},
            {"text": "बहुत बढ़िया! तो ऐसा करो पंचायत की टंकी पर वाई-फाई लगवा दो।", "caps": "टंकी पर | *वाई-फाई लगवाओ", "speaker": "A", "shot": "two_shot", "emotion_a": "laugh", "emotion_b": "normal", "pill": "", "sfx": "boing"},
            {"text": "लेकिन अगले ही दिन मार्केट पचास प्रतिशत नीचे गिर गया!", "caps": "मार्केट *पचास | प्रतिशत *गिरा!", "speaker": "narrator", "shot": "dramatic_zoom", "emotion_a": "shock", "emotion_b": "shock", "pill": "MARKET CRASH!", "sfx": "slam"},
            {"text": "सचिव जी, अब मेरी असली लौकी ही वापस ले आओ, वही सेफ थी!", "caps": "*असली लौकी | वापस लाओ!", "speaker": "A", "shot": "two_shot", "emotion_a": "angry", "emotion_b": "laugh", "pill": "GAJAB BEZZATI!", "sfx": "thud"},
        ],
    },
    {
        "subject_key": "mirzapur_exam_viva_parody",
        "title": "अगर कालीन भैया कॉलेज का वाइवा लेने आ जाएं! 😱🔥 #Shorts #Mirzapur",
        "description": "कॉलेज के वाइवा में अगर मिर्ज़ापुर वाला अंदाज़ आ जाए तो स्टूडेंट का क्या हाल होगा!\n\n#Shorts #Mirzapur #Animation #Comedy #HindiShorts #Viral",
        "tags": ["shorts", "mirzapur", "animation", "comedy", "college", "viral"],
        "music": "tension",
        "world": "mirzapur_hall",
        "banner": "MIRZAPUR VIVA TEST!",
        "char_a": {"skin": "#D99B78", "shirt": "#1E1E24", "shirtShade": "#111116", "hair": "#1C1A19", "moustache": True, "glasses": True, "beard": True},
        "char_b": {"skin": "#EBC2A6", "shirt": "#E05A47", "shirtShade": "#BA4232", "hair": "#3B2A20", "moustache": False, "glasses": False, "beard": False},
        "lines": [
            {"text": "सोचिए अगर आपके कॉलेज के वाइवा में टीचर की जगह मिर्ज़ापुर के बॉस बैठ जाएं!", "caps": "वाइवा में | *मिर्ज़ापुर बॉस!", "speaker": "narrator", "shot": "two_shot", "emotion_a": "normal", "emotion_b": "shock", "pill": "VIVA ALERT!", "sfx": "slam"},
            {"text": "बेटा, तुमने असाइनमेंट कॉपी किया है, ये बात सबको पता है।", "caps": "असाइनमेंट | *कॉपी किया!", "speaker": "A", "shot": "closeup_a", "emotion_a": "angry", "emotion_b": "shock", "pill": "", "sfx": "whoosh"},
            {"text": "सर, रात भर जागकर खुद लिखा है, बस थोड़ा गूगल देखा था!", "caps": "बस *थोड़ा | गूगल देखा!", "speaker": "B", "shot": "closeup_b", "emotion_a": "normal", "emotion_b": "shock", "pill": "FULL PANIC!", "sfx": "alarm"},
            {"text": "हमें नंबर देने से पहले एक शर्त है — चाय में अदरक सही होनी चाहिए!", "caps": "चाय में | *अदरक चाहिए!", "speaker": "A", "shot": "dramatic_zoom", "emotion_a": "normal", "emotion_b": "shock", "pill": "CHAI TEST!", "sfx": "pop"},
            {"text": "और स्टूडेंट ने अदरक वाली चाय पिलाकर पूरे सौ नंबर हासिल कर लिए!", "caps": "पूरे *सौ | नंबर मिले!", "speaker": "narrator", "shot": "two_shot", "emotion_a": "laugh", "emotion_b": "laugh", "pill": "100/100 PASS!", "sfx": "sparkle"},
        ],
    },
]


class AnimatedStoryEngine:
    """Renders 2D/3D-shaded Hindi animated webseries & movie Shorts via zack_engine/."""

    SR = 48000

    def __init__(self, engine_dir: str = "zack_engine", output_dir: str = "output/batch_today/channel_3"):
        self.engine_dir = Path(engine_dir).resolve()
        self.output_dir = Path(output_dir).resolve()
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.thumb_gen = ThumbnailGenerator(output_dir=str(self.output_dir))

    @staticmethod
    def _voice_for_speaker(speaker: str) -> Tuple[str, str, str]:
        # Female fallback voice profiles when Edge-TTS fallback is used (primary uses ElevenLabs Sarah)
        if speaker == "A":
            return ("hi-IN-SwaraNeural", "-4Hz", "+4%")
        elif speaker == "B":
            return ("hi-IN-SwaraNeural", "+6Hz", "+8%")
        return ("hi-IN-SwaraNeural", "+0Hz", "+6%")

    @staticmethod
    async def _tts_line(
        text: str,
        tmp_dir: Path,
        idx: int,
        speaker: str,
        previous_text: Optional[str] = None,
        next_text: Optional[str] = None,
        emotion: Optional[str] = None,
    ) -> Tuple[np.ndarray, List[Dict[str, Any]], str]:
        voice, pitch, rate = AnimatedStoryEngine._voice_for_speaker(speaker)
        attempts = [
            (voice, rate, pitch),
            ("hi-IN-MadhurNeural", "+5%", "+0Hz"),
            ("hi-IN-SwaraNeural", "+5%", "+0Hz"),
        ]
        pcm, words, backend = await synthesize_line_pcm_and_words(
            text=text,
            tmp_dir=tmp_dir,
            stem=f"story_line_{idx}",
            role_or_voice=speaker,
            emotion=emotion,
            previous_text=previous_text,
            next_text=next_text,
            edge_attempts=attempts,
            default_fallback_text="आगे देखिए क्या होता है।",
        )
        return pcm, words, backend

    async def _build_narration_and_timing(
        self, lines: List[Dict[str, Any]], lead: float = 0.25, gap: float = 0.18, outro: float = 0.70
    ) -> Tuple[np.ndarray, Dict[str, Any], List[Dict[str, Any]]]:
        data_dir = self.engine_dir / "data"
        data_dir.mkdir(parents=True, exist_ok=True)

        chunks = []
        used_backends: List[str] = []
        for idx, ln in enumerate(lines):
            prev_txt = lines[idx - 1]["text"] if idx > 0 else None
            next_txt = lines[idx + 1]["text"] if idx + 1 < len(lines) else None
            spk = ln.get("speaker", "narrator")
            emotion = (
                ln.get("emotion_a") if spk == "A"
                else (ln.get("emotion_b") if spk == "B" else None)
            ) or ln.get("pose") or ln.get("emotion")
            pcm, words, backend = await self._tts_line(
                ln["text"],
                data_dir,
                idx,
                spk,
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
        full_audio = full_audio[: int(total_dur * self.SR)]
        active_backend = used_backends[0] if used_backends else "multi_hindi"
        print(f"🎙️ AnimatedStory TTS backend: {active_backend}")
        lines_json = {"duration": total_dur, "voice": active_backend, "speed": 1.0, "lines": line_entries}
        return full_audio, lines_json, word_entries

    def render_story_short(
        self,
        blueprint: Dict[str, Any],
        output_video_path: str,
        output_thumb_path: str,
        slot_index: int = 1,
        tracker=None,
        batch_hashes: Optional[Set[str]] = None,
    ) -> Dict[str, Any]:
        """Renders full 1080x1920 animated story Short + guaranteed unique dHash thumbnail."""
        data_dir = self.engine_dir / "data"
        data_dir.mkdir(parents=True, exist_ok=True)

        lines = blueprint.get("lines", [])
        if not lines:
            raise ValueError("Story blueprint must contain at least 1 line")

        full_audio, lines_json, words_json = asyncio.run(self._build_narration_and_timing(lines))
        wavfile.write(data_dir / "narration.wav", self.SR, full_audio)
        (data_dir / "lines.json").write_text(json.dumps(lines_json, ensure_ascii=False, indent=2), encoding="utf-8")
        (data_dir / "words.json").write_text(json.dumps(words_json, ensure_ascii=False, indent=2), encoding="utf-8")

        script_json = {
            "title": blueprint.get("title", "Animated WebSeries Short"),
            "voice": lines_json.get("voice", "elevenlabs"),
            "music": blueprint.get("music", "bed"),
            "lines": [{"text": ln["text"], "caps": ln.get("caps", "")} for ln in lines],
        }
        storyboard_json = {
            "mode": "story",
            "world": blueprint.get("world", "panchayat_village"),
            "char_a": blueprint.get("char_a", {}),
            "char_b": blueprint.get("char_b", {}),
            "lines": [
                {
                    "speaker": ln.get("speaker", "narrator"),
                    "shot": ln.get("shot", "two_shot"),
                    "emotion_a": ln.get("emotion_a", "normal"),
                    "emotion_b": ln.get("emotion_b", "normal"),
                    "pill": ln.get("pill", ""),
                    "sfx": ln.get("sfx", "whoosh"),
                }
                for ln in lines
            ],
        }
        (self.engine_dir / "script.json").write_text(json.dumps(script_json, ensure_ascii=False, indent=2), encoding="utf-8")
        (data_dir / "storyboard.json").write_text(json.dumps(storyboard_json, ensure_ascii=False, indent=2), encoding="utf-8")

        subprocess.run(["node", "tools/capture.mjs", "cues"], cwd=str(self.engine_dir), check=True)
        subprocess.run([sys.executable, "tools/mix.py", "."], cwd=str(self.engine_dir), check=True)

        out_vid_abs = Path(output_video_path).resolve()
        out_vid_abs.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["node", "tools/capture.mjs", "video", str(out_vid_abs)], cwd=str(self.engine_dir), check=True)

        dur = float(lines_json["duration"])
        probe_times = [round(dur * k, 2) for k in (0.28, 0.50, 0.72, 0.14)]
        clean_dir = data_dir / "clean_thumbs"
        clean_dir.mkdir(parents=True, exist_ok=True)
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
                badge_text=blueprint.get("banner", "BOLLYWOOD TWIST!"),
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
            "duration": dur,
            "title": blueprint["title"],
            "description": blueprint["description"],
            "tags": blueprint.get("tags", ["shorts", "animation", "webseries", "movies", "comedy"]),
            "subject_key": blueprint.get("subject_key", ""),
        }
