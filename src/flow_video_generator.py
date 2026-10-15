"""
Google Flow & Veo AI Video Generator Engine
-------------------------------------------
Connects to Google's Veo generative video model via Google GenAI SDK (Gemini API).
Generates cinematic, photorealistic 9:16 vertical video scenes for each sentence
of the viral script, exactly like Google Flow studio.
"""

import os
import sys
import time
from typing import List, Dict, Any, Optional

try:
    from google import genai
    from google.genai import types
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False


class FlowVideoGenerator:
    """Generates cinematic AI video clips using Google Flow / Veo model."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        self.client = None
        if self.api_key and GENAI_AVAILABLE:
            try:
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                print(f"Flow/Veo initialization warning: {e}")

    def is_configured(self) -> bool:
        """Returns True if a valid Google Gemini/Veo API key is configured."""
        return bool(self.client)

    def generate_scene_clip(self, prompt: str, output_path: str, duration_sec: int = 5) -> Optional[str]:
        """
        Generates a 9:16 vertical AI video scene using Google Veo (Google Flow Engine).
        """
        if not self.is_configured():
            print("Google Flow/Veo not configured: Set GEMINI_API_KEY environment variable.")
            return None

        enhanced_prompt = (
            f"Cinematic photorealistic 9:16 vertical video, 4k ultra-detailed, dramatic studio lighting: {prompt}"
        )
        print(f"🎬 Requesting Google Flow/Veo video for prompt: '{prompt[:60]}...'")

        try:
            operation = self.client.models.generate_videos(
                model="veo-2.0-generate-001",
                prompt=enhanced_prompt,
                config=types.GenerateVideosConfig(
                    aspect_ratio="9:16",
                    resolution="720p"
                )
            )

            # Wait for asynchronous generation
            max_wait = 180
            elapsed = 0
            while not operation.done and elapsed < max_wait:
                time.sleep(10)
                elapsed += 10
                operation = self.client.operations.get(operation)

            if operation.response and operation.response.generated_videos:
                video = operation.response.generated_videos[0]
                self.client.files.download(file=video.video)
                video.video.save(output_path)
                print(f"✓ Google Flow/Veo clip saved to {output_path}")
                return output_path
            else:
                print("Veo generation returned empty response.")
                return None
        except Exception as e:
            print(f"Google Flow/Veo generation failed: {e}")
            return None


if __name__ == "__main__":
    flow = FlowVideoGenerator()
    print("Google Flow / Veo Engine initialized. Configured:", flow.is_configured())
