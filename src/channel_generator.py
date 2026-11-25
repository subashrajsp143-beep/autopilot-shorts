"""
Channel Batch Generator (3 Distinct Niches, Zero Repeats)
---------------------------------------------------------
- Channel 1 (MiniTalesWorld): Zack D. Films-style Hindi 3D/X-Ray Animated Explainers
  via zack_engine/ + Gemini non-repeating topic generation + edge-tts WordBoundary.
- Channel 2 (Pawsome Productions): Viral Gaming Clips in their ORIGINAL creator language
  & authentic audio (NO AI Voice!) — CarryMinati, IShowSpeed, Techno Gamerz, Kai Cenat,
  CaseOh, Scout, Triggered Insaan, BeastBoyShub, Total Gaming, etc.
- Channel 3 (Next Level Facts): Pure Trending Viral Clips ("Jo Viral Hai Wahi") —
  Guinness Records, Hydraulic Press, Physics Magic, MrBeast Challenges, Trick Shots.

Strict Guarantees:
- Never reuses stale pre-rendered MP4 files from prior days.
- Never repeats source IDs, semantic subject keys, or similar titles.
- Never repeats thumbnails (enforced via 64-bit perceptual dHash).
"""

import glob
import os
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional, Set

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from src.dynamic_creator_engine import DynamicCreatorEngine
from src.gemini_engine import GeminiEngine
from src.history_tracker import HistoryTracker
from src.zack_explainer_engine import FALLBACK_ZACK_TOPICS, ZackExplainerEngine


ZACK_NICHES = [
    "Human Body Science (What happens if...)",
    "Brain & Sleep Mysteries",
    "Weird Medical & Survival Facts",
    "Space & Cosmos Extremes",
    "Deep Ocean & Earth Wonders",
    "Dark Psychology & Mind Tricks",
]


def _clear_stale_channel_outputs(channel_dir: str):
    """Deletes previous batch video/thumb/audio artifacts so old clips are never reused."""
    os.makedirs(channel_dir, exist_ok=True)
    for pattern in ("*.mp4", "*.jpg", "*.mp3", "*.wav", "*.ass"):
        for fpath in glob.glob(os.path.join(channel_dir, pattern)):
            try:
                os.remove(fpath)
            except Exception:
                pass


def generate_channel_batch(
    channel_id: int,
    base_output_dir: str = "output/batch_today",
    force_render: bool = True,
    day_offset: Optional[int] = None,
    target_count: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """
    Generates a fresh, strictly non-repeating batch of Shorts for the given channel ID.
    """
    if day_offset is None:
        day_offset = datetime.now().timetuple().tm_yday

    count = target_count or int(os.environ.get(f"DAILY_QUOTA_CH{channel_id}", 6))
    channel_dir = os.path.join(base_output_dir, f"channel_{channel_id}")
    _clear_stale_channel_outputs(channel_dir)

    tracker = HistoryTracker()
    results: List[Dict[str, Any]] = []
    batch_hashes: Set[str] = set()

    print("\n=======================================================")
    print(f"🎬 Generating {count} Unique Shorts for Channel {channel_id}")
    print(f"📂 Output directory: {channel_dir}")
    print("=======================================================\n")

    if channel_id == 1:
        # CHANNEL 1: Zack D. Films-style Hindi Explainers
        zack_engine = ZackExplainerEngine(engine_dir="zack_engine", output_dir=channel_dir)
        gemini = GeminiEngine()

        used_titles = list(tracker.history.get("used_script_titles", []))
        used_subjects = list(tracker.history.get("used_subject_keys", []))
        session_subjects: Set[str] = set()

        for slot in range(1, count + 1):
            niche = ZACK_NICHES[(day_offset + slot - 1) % len(ZACK_NICHES)]
            blueprint = None

            if gemini.is_available():
                for attempt in range(3):
                    try:
                        cand = gemini.generate_zack_explainer(
                            niche=niche,
                            used_titles=used_titles,
                            used_subjects=used_subjects + list(session_subjects),
                        )
                        sk = str(cand.get("subject_key") or f"topic_{day_offset}_{slot}_{attempt}").strip().lower()
                        title = str(cand.get("title") or "").strip()
                        source_id = f"zack3d_{sk}"

                        if (
                            cand.get("lines")
                            and sk not in session_subjects
                            and not tracker.is_subject_used(sk)
                            and not tracker.is_source_used(source_id)
                            and not tracker.is_title_used(title)
                        ):
                            cand["subject_key"] = sk
                            blueprint = cand
                            break
                        else:
                            print(f"⚠️ Gemini returned duplicate/empty topic '{sk}'; retrying...")
                    except Exception as ge_err:
                        print(f"⚠️ Gemini attempt {attempt + 1} failed: {ge_err}")

            if blueprint is None:
                for fb in FALLBACK_ZACK_TOPICS:
                    sk = fb["subject_key"]
                    source_id = f"zack3d_{sk}"
                    if sk not in session_subjects and not tracker.is_subject_used(sk) and not tracker.is_source_used(source_id) and not tracker.is_title_used(fb["title"]):
                        blueprint = fb
                        break

            if blueprint is None:
                print(f"⚠️ Skipping Channel 1 slot {slot}: no unique unused topic available.")
                continue

            sk = blueprint["subject_key"]
            source_id = f"zack3d_{sk}"
            session_subjects.add(sk)
            used_subjects.append(sk)
            used_titles.append(blueprint["title"])

            out_vid = os.path.join(channel_dir, f"ch1_v{slot:02d}.mp4")
            out_thumb = os.path.join(channel_dir, f"ch1_v{slot:02d}_thumb.jpg")
            print(f"[{slot}/{count}] Channel 1 (Zack 3D Hindi): Rendering '{blueprint['title'][:50]}'...")

            try:
                r = zack_engine.render_short(
                    blueprint=blueprint,
                    output_video_path=out_vid,
                    output_thumb_path=out_thumb,
                    slot_index=slot,
                    tracker=tracker,
                    batch_hashes=batch_hashes,
                )
                results.append({
                    "index": slot,
                    "channel_id": 1,
                    "type": f"Zack 3D Hindi Explainer ({niche[:18]})",
                    "title": r["title"],
                    "description": r["description"],
                    "tags": r["tags"],
                    "video_path": r["video_path"],
                    "thumbnail_path": r["thumbnail_path"],
                    "thumbnail_dhash": r["thumbnail_dhash"],
                    "duration": r["duration"],
                    "source_id": source_id,
                    "subject_key": sk,
                    "query": niche,
                })
                print(f"  ✓ Rendered Ch1 Slot {slot}: {os.path.basename(r['video_path'])}")
            except Exception as err:
                print(f"  ❌ Ch1 Slot {slot} render failed: {err}")

    elif channel_id in (2, 3):
        # CHANNEL 2: Viral Gaming Clips (Original language & audio ONLY — NO AI Voice)
        # CHANNEL 3: Pure Trending Viral Clips ("Jo Viral Hai Wahi")
        mode = "gaming" if channel_id == 2 else "viral_trending"
        label = "Gaming Clip (Original Audio)" if channel_id == 2 else "Trending Viral Short"
        creator_engine = DynamicCreatorEngine(
            downloads_dir=os.path.join("assets", "downloads", f"ch{channel_id}"),
            output_dir=channel_dir,
        )
        session_used_ids: Set[str] = set()

        for slot in range(1, count + 1):
            out_vid = os.path.join(channel_dir, f"ch{channel_id}_v{slot:02d}.mp4")
            out_thumb = os.path.join(channel_dir, f"ch{channel_id}_v{slot:02d}_thumb.jpg")
            print(f"[{slot}/{count}] Channel {channel_id} ({label}): Discovering fresh clip...")

            try:
                res = creator_engine.discover_and_render_slot(
                    mode=mode,
                    slot_index=slot,
                    output_video_path=out_vid,
                    output_thumb_path=out_thumb,
                    day_offset=day_offset,
                    session_used_ids=session_used_ids,
                    batch_hashes=batch_hashes,
                    require_audio=True,
                )
                if not res:
                    print(f"  ⚠️ No fresh clip found for Ch{channel_id} Slot {slot}.")
                    continue

                results.append({
                    "index": slot,
                    "channel_id": channel_id,
                    "type": label,
                    "title": res["title"],
                    "description": res["description"],
                    "tags": res["tags"],
                    "video_path": res["video_path"],
                    "thumbnail_path": res["thumbnail_path"],
                    "thumbnail_dhash": res.get("thumbnail_dhash", ""),
                    "duration": res["duration"],
                    "source_id": res["source_id"],
                    "subject_key": f"{mode}_{res['source_id']}",
                    "creator": res.get("creator", ""),
                    "source_url": res.get("source_url", ""),
                    "query": res.get("query", mode),
                })
                print(f"  ✓ Ready Ch{channel_id} Slot {slot}: {res['title'][:48]} ({res['source_id']})")
            except Exception as err:
                print(f"  ❌ Ch{channel_id} Slot {slot} failed: {err}")

    print(f"\n✅ Ready with {len(results)}/{count} unique videos for Channel {channel_id}!\n")
    return results
