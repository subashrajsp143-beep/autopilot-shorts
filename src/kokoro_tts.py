"""
Kokoro TTS — Free Local AI Voice Engine
----------------------------------------
Wraps the HyperFrames Kokoro-82M CLI for unlimited free TTS.
Supports Hindi (native hf_alpha, hf_beta, hm_omega, hm_psi voices)
and 9 other languages.

Voice Selection for YouTube Channels:
  Female: hf_alpha / hf_beta (alternating per video for variety)
  Male: hm_psi (deep Hindi male narrator)

Falls back cleanly when HyperFrames CLI or Node.js is not available.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from scipy.io import wavfile

# ---------------------------------------------------------------------------
# Kokoro Hindi Voice IDs
# ---------------------------------------------------------------------------
KOKORO_FEMALE_ALPHA = "hf_alpha"
KOKORO_FEMALE_BETA = "hf_beta"
KOKORO_MALE_PSI = "hm_psi"
KOKORO_MALE_OMEGA = "hm_omega"

# Rotation counter for alternating female voices across videos
_female_voice_counter = 0

# HyperFrames CLI path (Node.js script)
_HYPERFRAMES_CLI = Path(
    os.environ.get(
        "HYPERFRAMES_CLI",
        os.path.expanduser(r"~\.gemini\config\skills\hyperframes\scripts\plugin-cli.mjs"),
    )
)

_DEVANAGARI_RE = re.compile(r"[\u0900-\u097F]")


def _detect_lang(text: str) -> str:
    """Auto-detect language from text content."""
    if _DEVANAGARI_RE.search(text or ""):
        return "hi"
    return "en-us"


def is_kokoro_available() -> bool:
    """Check if HyperFrames Kokoro TTS CLI is available."""
    if not _HYPERFRAMES_CLI.exists():
        return False
    # Check node.js is available
    return shutil.which("node") is not None


def get_next_female_voice() -> str:
    """Alternate between hf_alpha and hf_beta for voice variety."""
    global _female_voice_counter
    voice = KOKORO_FEMALE_ALPHA if _female_voice_counter % 2 == 0 else KOKORO_FEMALE_BETA
    _female_voice_counter += 1
    return voice


def resolve_kokoro_voice(
    role_or_voice: Optional[str] = None,
    gender: str = "female",
) -> str:
    """
    Map role/speaker to a Kokoro Hindi voice ID.

    Roles:
      - explainer / narrator → female (alternating alpha/beta)
      - speaker_a / A → female alpha (consistent per character)
      - speaker_b / B → female beta (consistent per character)
      - male / hm_psi → male psi
      - Any explicit Kokoro voice ID (hf_*, hm_*) → passed through
    """
    role = (role_or_voice or "").strip().lower()

    # Pass through explicit Kokoro voice IDs
    if role.startswith(("hf_", "hm_", "af_", "am_", "bf_", "bm_")):
        return role

    # Male override
    if gender == "male" or role in ("male",):
        return KOKORO_MALE_PSI

    # Character-consistent voice mapping for animated stories
    if role in ("a", "speaker_a", "speaker-a"):
        return KOKORO_FEMALE_ALPHA
    if role in ("b", "speaker_b", "speaker-b"):
        return KOKORO_FEMALE_BETA

    # Default: alternating female voices for variety across videos
    return get_next_female_voice()


def kokoro_synthesize(
    text: str,
    output_path: str,
    *,
    voice: str = "",
    speed: float = 1.0,
    lang: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Synthesize speech using Kokoro TTS via HyperFrames CLI.

    Returns dict with:
      - ok: bool
      - output_path: str (absolute path to .wav)
      - duration: float (seconds)
      - voice: str
      - lang: str
    """
    if not is_kokoro_available():
        raise RuntimeError("Kokoro TTS not available (HyperFrames CLI or Node.js missing)")

    detected_lang = lang or _detect_lang(text)
    chosen_voice = voice or resolve_kokoro_voice(gender="female")

    # Write text to temp file (avoids shell escaping issues with Hindi text)
    tmp_dir = Path(tempfile.mkdtemp(prefix="kokoro_"))
    text_file = tmp_dir / "input.txt"
    text_file.write_text(text.strip(), encoding="utf-8")

    out_path = Path(output_path).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        "node",
        str(_HYPERFRAMES_CLI),
        "tts",
        "--text-file", str(text_file),
        "--voice", chosen_voice,
        "--lang", detected_lang,
        "--speed", str(speed),
        "--output", str(out_path),
        "--json",
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,
            encoding="utf-8",
            errors="replace",
        )

        if result.returncode != 0:
            stderr = (result.stderr or "").strip()
            raise RuntimeError(f"Kokoro TTS failed (exit {result.returncode}): {stderr}")

        # Parse JSON output
        stdout = (result.stdout or "").strip()
        try:
            data = json.loads(stdout)
        except json.JSONDecodeError:
            # Fallback: check if file was created
            if out_path.exists() and out_path.stat().st_size > 500:
                data = {"ok": True}
            else:
                raise RuntimeError(f"Kokoro TTS returned invalid JSON: {stdout[:200]}")

        if not data.get("ok"):
            raise RuntimeError(f"Kokoro TTS returned ok=false: {stdout[:200]}")

        # Get duration from file if not in response
        duration = data.get("durationSeconds", 0)
        if not duration and out_path.exists():
            try:
                probe = subprocess.check_output(
                    ["ffprobe", "-v", "error", "-show_entries", "format=duration",
                     "-of", "default=noprint_wrappers=1:nokey=1", str(out_path)],
                    text=True,
                ).strip()
                duration = float(probe)
            except Exception:
                duration = 0.0

        return {
            "ok": True,
            "output_path": str(out_path),
            "duration": duration,
            "voice": chosen_voice,
            "lang": detected_lang,
        }
    finally:
        # Cleanup temp files
        try:
            text_file.unlink(missing_ok=True)
            tmp_dir.rmdir()
        except Exception:
            pass


def kokoro_synthesize_pcm(
    text: str,
    tmp_dir: Path,
    stem: str,
    *,
    voice: str = "",
    speed: float = 1.0,
    lang: Optional[str] = None,
) -> Tuple[np.ndarray, float]:
    """
    Synthesize and return 48kHz stereo int16 PCM numpy array + duration.
    Converts Kokoro WAV (24kHz mono) → 48kHz stereo via ffmpeg.
    """
    tmp_dir = Path(tmp_dir)
    tmp_dir.mkdir(parents=True, exist_ok=True)

    raw_wav = tmp_dir / f"{stem}_kokoro_raw.wav"
    out_wav = tmp_dir / f"{stem}_kokoro_48k.wav"

    try:
        result = kokoro_synthesize(text, str(raw_wav), voice=voice, speed=speed, lang=lang)

        # Convert to 48kHz stereo
        subprocess.run(
            ["ffmpeg", "-v", "error", "-y", "-i", str(raw_wav),
             "-ar", "48000", "-ac", "2", str(out_wav)],
            check=True,
        )

        sr, pcm = wavfile.read(out_wav)
        if pcm.ndim == 1:
            pcm = np.stack([pcm, pcm], axis=1)
        pcm = pcm.astype(np.int16, copy=False)

        duration = len(pcm) / 48000.0
        return pcm, duration
    finally:
        raw_wav.unlink(missing_ok=True)
        out_wav.unlink(missing_ok=True)


def kokoro_proportional_words(text: str, duration: float) -> List[Dict[str, Any]]:
    """Generate proportional word timings (Kokoro doesn't provide word-level timestamps)."""
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
