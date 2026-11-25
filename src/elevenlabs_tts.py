"""
ElevenLabs Text-to-Speech Helper
--------------------------------
Provides natural human-like narration, consistent character/narrator voices,
accurate Hindi pronunciation (`language_code="hi"`, `apply_text_normalization="on"`),
expressive emotion presets, Request Stitching (`previous_text`/`next_text`),
and exact character-to-word timestamp extraction for automatic A/V synchronization.

Falls back cleanly when ELEVENLABS_API_KEY is unset or unavailable so scheduled
YouTube uploads never fail.
"""

from __future__ import annotations

import asyncio
import base64
import os
import re
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np
from dotenv import load_dotenv
from elevenlabs import ElevenLabs, VoiceSettings
from scipy.io import wavfile

# Load local .env automatically (no-op in GitHub Actions where env vars/secrets are injected)
load_dotenv(override=False)

DEFAULT_MODEL_ID = "eleven_v4"
DEFAULT_OUTPUT_FORMAT = "mp3_44100_128"

# Verified free-plan-safe pre-made voices (per ElevenLabs text-to-speech skill)
VOICE_GEORGE = "JBFqnCBsd6RMkjVDRZzb"  # Warm, captivating storyteller
VOICE_DANIEL = "onwK4e9ZLuTAKqWW03F9"  # Deep, authoritative male character
VOICE_SARAH = "EXAVITQu4vr4xnSDxMaL"   # Clear, expressive narrator

_DEVANAGARI_RE = re.compile(r"[\u0900-\u097F]")
_VOICE_ID_RE = re.compile(r"^[A-Za-z0-9]{15,32}$")
_CLIENT_CACHE: Dict[str, ElevenLabs] = {}


class ElevenLabsUnavailableError(RuntimeError):
    """Raised when ElevenLabs TTS cannot be used (missing key, auth/quota error, network issue)."""


@dataclass(frozen=True)
class VoiceProfile:
    voice_id: str
    stability: float
    similarity_boost: float
    label: str


def sanitize_hindi_tts_text(text: str, default_fallback: str = "आगे देखिए।") -> str:
    """Clean text while preserving Devanagari letters, matras, and basic punctuation."""
    clean = re.sub(r"[^\w\s\u0900-\u097F.,?!'\"।-]", " ", str(text or "")).strip()
    clean = re.sub(r"\s+", " ", clean)
    return clean or default_fallback


def detect_language_code(text: str, explicit_lang: Optional[str] = None) -> str:
    """Return ISO 639-1 language code; enforces Hindi when Devanagari script is present."""
    if explicit_lang:
        return explicit_lang.strip().lower()
    if _DEVANAGARI_RE.search(text or ""):
        return "hi"
    return "en"


def get_elevenlabs_api_key() -> Optional[str]:
    """Return ELEVENLABS_API_KEY from environment or .env without logging it."""
    load_dotenv(override=False)
    key = (os.environ.get("ELEVENLABS_API_KEY") or "").strip()
    return key or None


def is_elevenlabs_available() -> bool:
    return get_elevenlabs_api_key() is not None


def _get_client(api_key: str) -> ElevenLabs:
    client = _CLIENT_CACHE.get(api_key)
    if client is None:
        client = ElevenLabs(api_key=api_key)
        _CLIENT_CACHE[api_key] = client
    return client


def _clamp_stability(val: float) -> float:
    return round(max(0.25, min(0.70, val)), 2)


def resolve_voice_profile(
    role_or_voice: Optional[str] = None,
    emotion: Optional[str] = None,
    text_hint: str = "",
) -> VoiceProfile:
    """Map semantic speaker roles (or explicit voice IDs) to consistent voice + emotion settings."""
    role = (role_or_voice or "explainer").strip()
    role_low = role.lower()

    default_voice = (os.environ.get("ELEVENLABS_VOICE_ID") or "").strip() or VOICE_GEORGE

    if _VOICE_ID_RE.match(role) and "neural" not in role_low:
        voice_id = role
        base_stability = 0.38
        similarity = 0.80
        label = f"custom:{role[:8]}"
    elif role_low in ("a", "speaker_a", "speaker-a"):
        voice_id = (os.environ.get("ELEVENLABS_VOICE_A") or "").strip() or VOICE_DANIEL
        base_stability = 0.42
        similarity = 0.82
        label = "speaker_a:daniel"
    elif role_low in ("b", "speaker_b", "speaker-b"):
        voice_id = (os.environ.get("ELEVENLABS_VOICE_B") or "").strip() or VOICE_GEORGE
        base_stability = 0.32
        similarity = 0.78
        label = "speaker_b:george"
    elif role_low in ("narrator",):
        voice_id = (os.environ.get("ELEVENLABS_VOICE_NARRATOR") or "").strip() or default_voice
        # Distinct default narrator for multi-speaker stories when no override is forced
        if not os.environ.get("ELEVENLABS_VOICE_NARRATOR") and not os.environ.get("ELEVENLABS_VOICE_ID"):
            voice_id = VOICE_SARAH
        base_stability = 0.40
        similarity = 0.80
        label = "narrator:sarah"
    else:
        voice_id = (os.environ.get("ELEVENLABS_VOICE_EXPLAINER") or "").strip() or default_voice
        base_stability = 0.36
        similarity = 0.80
        label = "explainer:george"

    emo = (emotion or "").strip().lower()
    if emo in ("shocked", "panic", "excited", "laugh", "angry") or "!" in (text_hint or ""):
        base_stability -= 0.06
    elif emo in ("question", "curious") or "?" in (text_hint or ""):
        base_stability -= 0.04
    elif emo in ("calm", "serious", "sad", "thinking"):
        base_stability += 0.04

    return VoiceProfile(
        voice_id=voice_id,
        stability=_clamp_stability(base_stability),
        similarity_boost=similarity,
        label=label,
    )


def _proportional_word_fallback(text: str, duration: float) -> List[Dict[str, Any]]:
    tokens = [t for t in (text or "").split() if t.strip()]
    if not tokens:
        return []
    total_chars = sum(len(t) for t in tokens) or len(tokens)
    cursor = 0.0
    words: List[Dict[str, Any]] = []
    for tok in tokens:
        dur = max(0.05, (len(tok) / total_chars) * max(0.2, duration))
        end = min(max(0.2, duration), cursor + dur)
        words.append({"w": tok, "s": round(cursor, 3), "e": round(max(cursor + 0.02, end), 3)})
        cursor = end
    return words


def alignment_to_words(
    alignment: Any,
    fallback_text: str = "",
    fallback_duration: Optional[float] = None,
) -> List[Dict[str, Any]]:
    """
    Convert ElevenLabs character-level alignment into exact word timestamps:
    [{"w": str, "s": float, "e": float}, ...]
    Devanagari vowel signs/matras remain joined because splitting occurs only on whitespace.
    """
    if alignment is None:
        return _proportional_word_fallback(fallback_text, fallback_duration or 1.5)

    if isinstance(alignment, dict):
        chars = alignment.get("characters") or []
        starts = alignment.get("character_start_times_seconds") or []
        ends = alignment.get("character_end_times_seconds") or []
    else:
        chars = getattr(alignment, "characters", None) or []
        starts = getattr(alignment, "character_start_times_seconds", None) or []
        ends = getattr(alignment, "character_end_times_seconds", None) or []

    n = min(len(chars), len(starts), len(ends))
    if n == 0:
        return _proportional_word_fallback(fallback_text, fallback_duration or 1.5)

    words: List[Dict[str, Any]] = []
    buf: List[str] = []
    w_start: Optional[float] = None
    w_end: float = 0.0

    for i in range(n):
        ch = str(chars[i])
        s_t = float(starts[i])
        e_t = float(ends[i])

        if ch.isspace():
            if buf:
                tok = "".join(buf).strip()
                if tok:
                    words.append({
                        "w": tok,
                        "s": round(w_start if w_start is not None else s_t, 3),
                        "e": round(max((w_start or 0.0) + 0.02, w_end), 3),
                    })
                buf.clear()
                w_start = None
        else:
            if w_start is None:
                w_start = s_t
            w_end = max(w_end, e_t, s_t + 0.02)
            buf.append(ch)

    if buf:
        tok = "".join(buf).strip()
        if tok:
            words.append({
                "w": tok,
                "s": round(w_start if w_start is not None else 0.0, 3),
                "e": round(max((w_start or 0.0) + 0.02, w_end), 3),
            })

    if not words:
        inferred_dur = float(ends[-1]) if ends else (fallback_duration or 1.5)
        return _proportional_word_fallback(fallback_text, inferred_dur)

    return words


def words_to_sentences(words: Sequence[Dict[str, Any]], original_text: str = "") -> List[Dict[str, Any]]:
    """Aggregate word timestamps into sentence events compatible with VoiceGenerator."""
    if not words:
        return []

    sentences: List[Dict[str, Any]] = []
    cur_words: List[Dict[str, Any]] = []
    end_punct = re.compile(r"[।.!?]+$")

    for w in words:
        cur_words.append(w)
        if end_punct.search(str(w.get("w", "")).strip()):
            start_s = float(cur_words[0]["s"])
            end_s = float(cur_words[-1]["e"])
            sentences.append({
                "start": start_s,
                "end": end_s,
                "duration": max(0.05, end_s - start_s),
                "text": " ".join(str(x["w"]) for x in cur_words),
            })
            cur_words = []

    if cur_words:
        start_s = float(cur_words[0]["s"])
        end_s = float(cur_words[-1]["e"])
        sentences.append({
            "start": start_s,
            "end": end_s,
            "duration": max(0.05, end_s - start_s),
            "text": " ".join(str(x["w"]) for x in cur_words) or original_text,
        })

    return sentences


def synthesize_with_timestamps(
    text: str,
    role_or_voice: Optional[str] = None,
    *,
    language_code: Optional[str] = None,
    emotion: Optional[str] = None,
    previous_text: Optional[str] = None,
    next_text: Optional[str] = None,
    output_format: str = DEFAULT_OUTPUT_FORMAT,
    model_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Synthesize speech via ElevenLabs `convert_with_timestamps` and return decoded MP3 bytes
    alongside word-level and sentence-level timestamps.
    """
    api_key = get_elevenlabs_api_key()
    if not api_key:
        raise ElevenLabsUnavailableError("ELEVENLABS_API_KEY is not set")

    clean_text = sanitize_hindi_tts_text(text)
    chosen_model = (model_id or os.environ.get("ELEVENLABS_MODEL_ID") or DEFAULT_MODEL_ID).strip()
    lang = detect_language_code(clean_text, explicit_lang=language_code)
    profile = resolve_voice_profile(role_or_voice, emotion=emotion, text_hint=clean_text)

    kwargs: Dict[str, Any] = {
        "voice_id": profile.voice_id,
        "text": clean_text,
        "model_id": chosen_model,
        "output_format": output_format,
        "voice_settings": VoiceSettings(
            stability=profile.stability,
            similarity_boost=profile.similarity_boost,
        ),
        "apply_text_normalization": "on",
    }

    # eleven_multilingual_v2 does not support language_code parameter cleanly
    if chosen_model != "eleven_multilingual_v2":
        kwargs["language_code"] = lang

    if previous_text and str(previous_text).strip():
        kwargs["previous_text"] = sanitize_hindi_tts_text(str(previous_text), "")
    if next_text and str(next_text).strip():
        kwargs["next_text"] = sanitize_hindi_tts_text(str(next_text), "")

    client = _get_client(api_key)
    last_err: Optional[Exception] = None
    resp = None
    for attempt in range(2):
        try:
            resp = client.text_to_speech.convert_with_timestamps(**kwargs)
            break
        except Exception as err:
            last_err = err
            msg = str(err).lower()
            # Auth / plan / quota errors will not succeed on immediate retry
            if any(code in msg for code in ("401", "402", "403", "422", "invalid_api_key", "paid_plan_required")):
                raise ElevenLabsUnavailableError(f"ElevenLabs API rejected request: {err}") from err
            if attempt == 0:
                time.sleep(0.8)

    if resp is None:
        raise ElevenLabsUnavailableError(f"ElevenLabs synthesis failed: {last_err}") from last_err

    audio_b64 = getattr(resp, "audio_base_64", None)
    if not audio_b64:
        raise ElevenLabsUnavailableError("ElevenLabs returned empty audio_base_64")

    audio_bytes = base64.b64decode(audio_b64)
    if len(audio_bytes) <= 250:
        raise ElevenLabsUnavailableError("ElevenLabs returned unexpectedly small audio payload")

    alignment = getattr(resp, "alignment", None) or getattr(resp, "normalized_alignment", None)
    words = alignment_to_words(alignment, fallback_text=clean_text)
    has_alignment = alignment is not None and bool(
        (alignment.get("characters") if isinstance(alignment, dict) else getattr(alignment, "characters", None))
    )
    duration = float(words[-1]["e"]) if words else 0.0
    sentences = words_to_sentences(words, original_text=clean_text)

    return {
        "audio_bytes": audio_bytes,
        "words": words,
        "has_alignment": has_alignment,
        "sentences": sentences,
        "duration": duration,
        "voice_id": profile.voice_id,
        "voice_label": profile.label,
        "model_id": chosen_model,
        "language_code": lang,
    }


def mp3_bytes_to_pcm_48k_stereo(audio_bytes: bytes, tmp_dir: Path, stem: str) -> Tuple[np.ndarray, float]:
    """Convert MP3/encoded audio bytes to 48kHz stereo int16 numpy PCM safely via ffmpeg."""
    tmp_dir.mkdir(parents=True, exist_ok=True)
    mp3_path = tmp_dir / f"{stem}.mp3"
    wav_path = tmp_dir / f"{stem}.wav"
    try:
        mp3_path.write_bytes(audio_bytes)
        subprocess.run(
            ["ffmpeg", "-v", "error", "-y", "-i", str(mp3_path), "-ar", "48000", "-ac", "2", str(wav_path)],
            check=True,
        )
        _, pcm = wavfile.read(wav_path)
        if pcm.ndim == 1:
            pcm = np.stack([pcm, pcm], axis=1)
        return pcm.astype(np.int16, copy=False), len(pcm) / 48000.0
    finally:
        mp3_path.unlink(missing_ok=True)
        wav_path.unlink(missing_ok=True)


async def synthesize_line_pcm_and_words(
    text: str,
    tmp_dir: Path,
    stem: str,
    *,
    role_or_voice: Optional[str] = None,
    emotion: Optional[str] = None,
    previous_text: Optional[str] = None,
    next_text: Optional[str] = None,
    edge_attempts: Optional[Sequence[Tuple[str, str, str]]] = None,
    default_fallback_text: str = "आगे देखिए।",
) -> Tuple[np.ndarray, List[Dict[str, Any]], str]:
    """
    Unified high-level TTS helper for frame-accurate pipelines (Channel 1 & Channel 3).
    Returns: (pcm_48k_stereo_int16, word_timings, backend_used).
    Uses ElevenLabs v4 + character timestamps first; falls back seamlessly to edge-tts / gTTS.
    """
    clean_text = sanitize_hindi_tts_text(text, default_fallback=default_fallback_text)

    if is_elevenlabs_available():
        try:
            res = await asyncio.to_thread(
                synthesize_with_timestamps,
                clean_text,
                role_or_voice,
                emotion=emotion,
                previous_text=previous_text,
                next_text=next_text,
            )
            pcm, dur = await asyncio.to_thread(mp3_bytes_to_pcm_48k_stereo, res["audio_bytes"], tmp_dir, stem)
            words = res["words"] if (res.get("has_alignment") and res.get("words")) else _proportional_word_fallback(clean_text, dur)
            return pcm, words, f"elevenlabs:{res['model_id']}:{res['voice_label']}"
        except Exception as el_err:
            print(f"⚠️ ElevenLabs fallback triggered for {stem} ({el_err}); using edge-tts...")

    import edge_tts

    attempts = list(edge_attempts or [
        ("hi-IN-MadhurNeural", "+6%", "+0Hz"),
        ("hi-IN-SwaraNeural", "+6%", "+0Hz"),
    ])
    words: List[Dict[str, Any]] = []
    audio_bytes = bytearray()

    for att_idx, (v_name, r_str, p_str) in enumerate(attempts):
        try:
            words.clear()
            audio_bytes.clear()
            comm = edge_tts.Communicate(clean_text, voice=v_name, rate=r_str, pitch=p_str, boundary="WordBoundary")
            async for msg in comm.stream():
                if msg["type"] == "audio":
                    audio_bytes.extend(msg["data"])
                elif msg["type"] == "WordBoundary":
                    start_s = msg["offset"] / 1e7
                    dur_s = msg["duration"] / 1e7
                    words.append({"w": msg["text"], "s": start_s, "e": start_s + dur_s})
            if len(audio_bytes) > 500:
                pcm, dur = await asyncio.to_thread(mp3_bytes_to_pcm_48k_stereo, bytes(audio_bytes), tmp_dir, stem)
                if not words:
                    words = _proportional_word_fallback(clean_text, dur)
                return pcm, words, f"edge-tts:{v_name}"
        except Exception as tts_err:
            print(f"⚠️ edge-tts attempt {att_idx + 1} failed ({tts_err}); retrying...")
            await asyncio.sleep(0.8)

    from gtts import gTTS

    tmp_dir.mkdir(parents=True, exist_ok=True)
    mp3_path = tmp_dir / f"{stem}_gtts.mp3"
    try:
        lang = detect_language_code(clean_text)
        await asyncio.to_thread(lambda: gTTS(text=clean_text, lang=lang).save(str(mp3_path)))
        raw_bytes = mp3_path.read_bytes()
    finally:
        mp3_path.unlink(missing_ok=True)

    pcm, dur = await asyncio.to_thread(mp3_bytes_to_pcm_48k_stereo, raw_bytes, tmp_dir, stem)
    return pcm, _proportional_word_fallback(clean_text, dur), "gtts"
