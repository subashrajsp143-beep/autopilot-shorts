"""
Verification suite for ElevenLabs TTS integration & fallback safety.
Uses mocked ElevenLabs SDK responses and generated audio bytes so tests never
spend paid characters or require live network calls, while verifying exact API
parameters, Request Stitching, Hindi word alignment, and caption synchronization.
"""

import asyncio
import base64
import io
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import numpy as np
from elevenlabs.types import AudioWithTimestampsResponse, CharacterAlignmentResponseModel
from scipy.io import wavfile

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from src import elevenlabs_tts
from src.animated_story_engine import AnimatedStoryEngine
from src.voice_generator import VoiceGenerator, generate_audio
from src.zack_explainer_engine import ZackExplainerEngine


def _make_sample_mp3_b64(duration_s: float = 0.8) -> str:
    """Create tiny valid MP3 audio encoded as base64 using ffmpeg."""
    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        wav_p = td_path / "tone.wav"
        mp3_p = td_path / "tone.mp3"
        sr = 44100
        t = np.linspace(0, duration_s, int(sr * duration_s), endpoint=False)
        pcm = (np.sin(2 * np.pi * 440 * t) * 4000).astype(np.int16)
        wavfile.write(wav_p, sr, pcm)
        subprocess.run(
            ["ffmpeg", "-v", "error", "-y", "-i", str(wav_p), "-b:a", "64k", str(mp3_p)],
            check=True,
        )
        return base64.b64encode(mp3_p.read_bytes()).decode("ascii")


def _build_alignment(text: str, total_s: float = 0.8) -> CharacterAlignmentResponseModel:
    chars = list(text)
    step = total_s / max(1, len(chars))
    starts = [round(i * step, 4) for i in range(len(chars))]
    ends = [round((i + 1) * step, 4) for i in range(len(chars))]
    return CharacterAlignmentResponseModel(
        characters=chars,
        character_start_times_seconds=starts,
        character_end_times_seconds=ends,
    )


class ElevenLabsIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sample_mp3_b64 = _make_sample_mp3_b64(0.8)

    def test_language_and_voice_profiles(self):
        self.assertEqual(elevenlabs_tts.detect_language_code("छींक रोकने पर क्या होगा?"), "hi")
        self.assertEqual(elevenlabs_tts.detect_language_code("Hello world"), "en")

        p_exp = elevenlabs_tts.resolve_voice_profile("explainer")
        p_a = elevenlabs_tts.resolve_voice_profile("A", emotion="calm")
        p_b = elevenlabs_tts.resolve_voice_profile("B", emotion="shocked", text_hint="क्या?!")
        p_n = elevenlabs_tts.resolve_voice_profile("narrator")

        self.assertEqual(p_exp.voice_id, elevenlabs_tts.VOICE_SARAH)
        self.assertEqual(p_a.voice_id, elevenlabs_tts.VOICE_SARAH)
        self.assertEqual(p_b.voice_id, elevenlabs_tts.VOICE_SARAH)
        self.assertEqual(p_n.voice_id, elevenlabs_tts.VOICE_SARAH)
        # Emotion modulation lowers stability for shocked/excited lines
        self.assertLess(p_b.stability, p_a.stability)

    def test_hindi_alignment_preserves_matras(self):
        text = "फुलेरा पंचायत में गजब हो गया।"
        align = _build_alignment(text, total_s=1.2)
        words = elevenlabs_tts.alignment_to_words(align, fallback_text=text)
        extracted = [w["w"] for w in words]
        self.assertEqual(extracted, text.split())
        self.assertGreater(words[-1]["e"], words[0]["s"])

        sents = elevenlabs_tts.words_to_sentences(words, text)
        self.assertEqual(len(sents), 1)
        self.assertEqual(sents[0]["text"], text)

    def test_mocked_voice_generator_ass_sync(self):
        captured_calls = []

        def fake_convert_with_timestamps(**kwargs):
            captured_calls.append(kwargs)
            return AudioWithTimestampsResponse(
                audio_base_64=self.sample_mp3_b64,
                alignment=_build_alignment(kwargs["text"], total_s=1.6),
                normalized_alignment=None,
            )

        fake_client = SimpleNamespace(
            text_to_speech=SimpleNamespace(convert_with_timestamps=fake_convert_with_timestamps)
        )

        with tempfile.TemporaryDirectory() as td:
            out_mp3 = str(Path(td) / "out.mp3")
            out_ass = str(Path(td) / "out.ass")
            text = "दुनिया का सबसे रहस्यमयी सच क्या आप जानते हैं?"
            with patch.dict(os.environ, {"ELEVENLABS_API_KEY": "test_key_mock"}, clear=False):
                with patch.object(elevenlabs_tts, "_get_client", return_value=fake_client):
                    res = generate_audio(text, out_mp3, out_ass, voice="hi-IN-MadhurNeural")

            self.assertTrue(Path(out_mp3).exists())
            self.assertTrue(Path(out_ass).exists())
            self.assertGreater(res["chunks_count"], 1)
            self.assertGreater(res["duration"], 0.5)
            self.assertEqual(len(res["sentences"]), 1)
            self.assertEqual(captured_calls[0]["model_id"], "eleven_v4")
            self.assertEqual(captured_calls[0]["language_code"], "hi")
            self.assertEqual(captured_calls[0]["apply_text_normalization"], "on")
            self.assertEqual(captured_calls[0]["voice_id"], elevenlabs_tts.VOICE_SARAH)
            ass_txt = Path(out_ass).read_text(encoding="utf-8")
            self.assertIn("Dialogue: 0,", ass_txt)
            self.assertIn("दुनिया", ass_txt)

    def test_zack_and_story_stitching_and_sync(self):
        captured_calls = []

        def fake_convert_with_timestamps(**kwargs):
            captured_calls.append(kwargs)
            return AudioWithTimestampsResponse(
                audio_base_64=self.sample_mp3_b64,
                alignment=_build_alignment(kwargs["text"], total_s=0.8),
                normalized_alignment=None,
            )

        fake_client = SimpleNamespace(
            text_to_speech=SimpleNamespace(convert_with_timestamps=fake_convert_with_timestamps)
        )

        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            zack = ZackExplainerEngine(engine_dir=str(td_path / "zack"), output_dir=str(td_path / "out1"))
            story = AnimatedStoryEngine(engine_dir=str(td_path / "story"), output_dir=str(td_path / "out3"))

            zack_lines = [
                {"text": "पहली लाइन का सच!", "pose": "shocked"},
                {"text": "दूसरी लाइन का जवाब।", "pose": "thinking"},
            ]
            story_lines = [
                {"speaker": "A", "emotion_a": "angry", "text": "ई का बवाल है सचिव जी!"},
                {"speaker": "B", "emotion_b": "shocked", "text": "सर जी लॉकी क्रिप्टो में बदल गई!"},
                {"speaker": "narrator", "text": "और पूरा गांव हैरान रह गया।"},
            ]

            with patch.dict(os.environ, {"ELEVENLABS_API_KEY": "test_key_mock"}, clear=False):
                with patch.object(elevenlabs_tts, "_get_client", return_value=fake_client):
                    pcm1, lines_json1, words1 = asyncio.run(zack._build_narration_and_timing(zack_lines))
                    pcm3, lines_json3, words3 = asyncio.run(story._build_narration_and_timing(story_lines))

            self.assertEqual(pcm1.ndim, 2)
            self.assertEqual(pcm1.shape[1], 2)
            self.assertTrue(lines_json1["voice"].startswith("elevenlabs:eleven_v4"))
            self.assertEqual(len(lines_json1["lines"]), 2)
            self.assertGreater(len(words1), 4)

            self.assertEqual(pcm3.ndim, 2)
            self.assertEqual(pcm3.shape[1], 2)
            self.assertTrue(lines_json3["voice"].startswith("elevenlabs:eleven_v4"))
            self.assertEqual(len(lines_json3["lines"]), 3)
            self.assertGreater(len(words3), 6)

            # Check Request Stitching on Zack lines (indices 0 and 1)
            self.assertIsNone(captured_calls[0].get("previous_text"))
            self.assertEqual(captured_calls[0].get("next_text"), "दूसरी लाइन का जवाब।")
            self.assertEqual(captured_calls[1].get("previous_text"), "पहली लाइन का सच!")
            self.assertIsNone(captured_calls[1].get("next_text"))

            # Check Sarah female voice across all story lines
            self.assertEqual(captured_calls[2]["voice_id"], elevenlabs_tts.VOICE_SARAH)
            self.assertEqual(captured_calls[3]["voice_id"], elevenlabs_tts.VOICE_SARAH)
            self.assertEqual(captured_calls[4]["voice_id"], elevenlabs_tts.VOICE_SARAH)

    def test_channel2_trending_games_include_gta6(self):
        from src.dynamic_creator_engine import GAMING_QUERY_POOL, TWITCH_GAMING_SOURCES

        yt_queries = " ".join(item["q"].lower() for item in GAMING_QUERY_POOL)
        twitch_games = [item["name"] for item in TWITCH_GAMING_SOURCES if item["kind"] == "game"]
        self.assertIn("gta 6", yt_queries)
        self.assertIn("marvel rivals", yt_queries)
        self.assertIn("Grand Theft Auto VI", twitch_games)
        self.assertIn("Marvel Rivals", twitch_games)

    def test_graceful_fallback_when_no_key(self):
        async def fake_stream():
            yield {"type": "audio", "data": base64.b64decode(self.sample_mp3_b64)}
            yield {"type": "WordBoundary", "offset": 1000000, "duration": 2000000, "text": "नमस्ते"}

        fake_comm = SimpleNamespace(stream=fake_stream)

        with tempfile.TemporaryDirectory() as td:
            with patch.dict(os.environ, {"ELEVENLABS_API_KEY": ""}, clear=False):
                with patch("src.elevenlabs_tts.load_dotenv", return_value=False):
                    with patch("edge_tts.Communicate", return_value=fake_comm):
                        pcm, words, backend = asyncio.run(
                            elevenlabs_tts.synthesize_line_pcm_and_words(
                                "नमस्ते",
                                Path(td),
                                "fallback_test",
                            )
                        )
            self.assertTrue(backend.startswith("edge-tts:"))
            self.assertEqual(words[0]["w"], "नमस्ते")
            self.assertGreater(len(pcm), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
