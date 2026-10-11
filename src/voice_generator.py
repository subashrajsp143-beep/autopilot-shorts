"""
Voice & Subtitle Generator
Uses Microsoft Neural TTS (Edge-TTS) to generate ultra-realistic human voices
and creates styled ASS subtitles with dynamic short-chunk timing (Hormozi style).
"""

import asyncio
import os
import re
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
        communicate = edge_tts.Communicate(text, self.voice)
        sentence_events: List[Dict[str, Any]] = []

        # Ensure output directory exists
        if os.path.dirname(output_audio_path):
            os.makedirs(os.path.dirname(output_audio_path), exist_ok=True)
        if os.path.dirname(output_ass_path):
            os.makedirs(os.path.dirname(output_ass_path), exist_ok=True)

        # Open audio output stream
        with open(output_audio_path, "wb") as audio_file:
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_file.write(chunk["data"])
                elif chunk["type"] == "SentenceBoundary":
                    # offset and duration in 100-nanosecond ticks
                    start_s = chunk["offset"] / 10_000_000.0
                    duration_s = chunk["duration"] / 10_000_000.0
                    sentence_events.append({
                        "start": start_s,
                        "end": start_s + duration_s,
                        "duration": duration_s,
                        "text": chunk["text"].strip()
                    })

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
            
            chunk_duration = sent["duration"] / len(chunks)
            for idx, c in enumerate(chunks):
                c_start = sent["start"] + (idx * chunk_duration)
                c_end = c_start + chunk_duration
                chunk_str = " ".join(c).upper()

                # Clean punctuation for punchier display
                chunk_str = re.sub(r'[,;]', '', chunk_str)

                start_ass = format_ass_time(c_start)
                end_ass = format_ass_time(c_end)
                dialogue_lines.append(
                    f"Dialogue: 0,{start_ass},{end_ass},ViralYellow,,0,0,0,,{chunk_str}"
                )

        # Detect if Hindi text (Devanagari characters)
        is_hindi = bool(re.search(r'[\u0900-\u097F]', text))
        font_name = "Nirmala UI" if is_hindi else "Arial"

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
Style: ViralYellow,{font_name},72,&H0000FFFF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,6,2,2,60,60,860,1

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
    test_text = "Number one. In 216 BC, Hannibal trapped 70000 Romans. Watch till the end to discover how."
    res = generate_audio(test_text, "../output/test_voice.mp3", "../output/test_voice.ass")
    print(f"Generated {res['duration']:.2f}s audio with {res['chunks_count']} subtitle chunks.")
