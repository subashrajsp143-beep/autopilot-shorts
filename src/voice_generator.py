"""
Voice & Subtitle Generator
Uses Microsoft Neural TTS (Edge-TTS) with seamless Google TTS (gTTS) fallback.
Creates styled ASS subtitles with dynamic short-chunk timing (Hormozi style).
"""

import asyncio
import os
import re
import subprocess
from typing import Dict, Any, List, Tuple
import edge_tts


def format_ass_time(seconds: float) -> str:
    """Formats float seconds into ASS timestamp format H:MM:SS.cs"""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    cs = int(round((seconds - int(seconds)) * 100))
    if cs >= 100:
        cs = 99
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


class VoiceGenerator:
    """Generates neural voiceover and synchronized ASS subtitles."""

    def __init__(self, voice: str = "en-US-ChristopherNeural"):
        self.voice = voice

    async def generate_speech_and_subtitles(
        self,
        text: str,
        output_audio_path: str,
        output_ass_path: str,
        words_per_chunk: int = 3
    ) -> Dict[str, Any]:
        """
        Synthesizes speech and generates styled ASS subtitles.
        Splits sentences into fast 2-4 word chunks for maximum retention.
        """
        # Ensure output directory exists
        if os.path.dirname(output_audio_path):
            os.makedirs(os.path.dirname(output_audio_path), exist_ok=True)
        if os.path.dirname(output_ass_path):
            os.makedirs(os.path.dirname(output_ass_path), exist_ok=True)

        sentence_events: List[Dict[str, Any]] = []

        try:
            # 1. Primary: Edge-TTS
            communicate = edge_tts.Communicate(text, self.voice)
            with open(output_audio_path, "wb") as audio_file:
                async for chunk in communicate.stream():
                    if chunk["type"] == "audio":
                        audio_file.write(chunk["data"])
                    elif chunk["type"] == "SentenceBoundary":
                        start_s = chunk["offset"] / 10_000_000.0
                        duration_s = chunk["duration"] / 10_000_000.0
                        sentence_events.append({
                            "start": start_s,
                            "end": start_s + duration_s,
                            "duration": duration_s,
                            "text": chunk["text"].strip()
                        })
        except Exception as e:
            # 2. Fallback: Google TTS (reliable on all cloud datacenters)
            print(f"Notice: Edge-TTS error ({e}). Using Google TTS fallback...")
            from gtts import gTTS
            lang = "hi" if "hi" in self.voice.lower() else "en"
            tts = gTTS(text=text, lang=lang, slow=False)
            tts.save(output_audio_path)

            try:
                cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", output_audio_path]
                out = subprocess.check_output(cmd, text=True).strip()
                total_dur = float(out)
            except Exception:
                total_dur = 30.0

            raw_sents = [s.strip() for s in re.split(r'[।\.!\?]+', text) if s.strip()]
            if not raw_sents:
                raw_sents = [text]
            time_per_sent = total_dur / len(raw_sents)
            cur_time = 0.0
            for sent in raw_sents:
                s_end = min(total_dur, cur_time + time_per_sent)
                sentence_events.append({
                    "start": cur_time,
                    "end": s_end,
                    "duration": s_end - cur_time,
                    "text": sent
                })
                cur_time = s_end

        # Calculate total duration
        total_duration = sentence_events[-1]["end"] if sentence_events else 0.0

        # Build dynamic chunks for subtitles
        dialogue_lines: List[str] = []
        for sent in sentence_events:
            sentence_text = sent["text"]
            words = sentence_text.split()
            if not words:
                continue

            num_words = len(words)
            chunk_size = max(1, words_per_chunk)
            chunks: List[List[str]] = [words[i:i + chunk_size] for i in range(0, num_words, chunk_size)]

            total_chars = sum(len(w) for w in words)
            time_per_char = sent["duration"] / max(1, total_chars)

            current_time = sent["start"]
            for chunk in chunks:
                chunk_chars = sum(len(w) for w in chunk)
                chunk_duration = max(0.4, chunk_chars * time_per_char)
                start_time_str = format_ass_time(current_time)
                end_time = min(sent["end"], current_time + chunk_duration)
                end_time_str = format_ass_time(end_time)

                chunk_text = " ".join(chunk).upper()
                dialogue_lines.append(
                    f"Dialogue: 0,{start_time_str},{end_time_str},ViralYellow,,0,0,0,,{chunk_text}"
                )
                current_time = end_time

        # Font selection based on platform
        font_name = "Nirmala UI" if os.name == "nt" else "Noto Sans Devanagari"

        # Build ASS file content with bold vertical layout styling
        ass_content = f"""[Script Info]
Title: Viral Shorts Subtitles
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: ViralYellow,{font_name},72,&H0000FFFF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,6,2,2,60,60,1180,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""" + "\n".join(dialogue_lines) + "\n"

        with open(output_ass_path, "w", encoding="utf-8") as f:
            f.write(ass_content)

        return {
            "audio_path": output_audio_path,
            "ass_path": output_ass_path,
            "duration": total_duration,
            "chunks_count": len(dialogue_lines),
            "sentences": sentence_events
        }


def generate_audio(text: str, audio_path: str, ass_path: str, voice: str = "en-US-ChristopherNeural") -> Dict[str, Any]:
    """Synchronous wrapper for generate_speech_and_subtitles."""
    vg = VoiceGenerator(voice=voice)
    return asyncio.run(vg.generate_speech_and_subtitles(text, audio_path, ass_path))


if __name__ == "__main__":
    test_text = "मिस्टर बीस्ट ने एक अनजान सब्सक्राइबर को पचास करोड़ का पूरा प्राइवेट आइलैंड फ्री में दे दिया।"
    res = generate_audio(test_text, "output/test_voice.mp3", "output/test_voice.ass", voice="hi-IN-MadhurNeural")
    print(f"Generated {res['duration']:.2f}s audio with {res['chunks_count']} subtitle chunks.")
