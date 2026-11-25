"""
Dynamic Viral Creator & Gaming Clip Engine
-----------------------------------------
Channel 2: Viral Gaming Clips (Original Creator Language & Audio ONLY — NO AI Voice)
           CarryMinati, IShowSpeed, Techno Gamerz, Kai Cenat, CaseOh, Scout,
           Triggered Insaan, BeastBoyShub, Total Gaming, etc.
Channel 3: Pure Trending Viral Clips ("Jo Viral Hai Wahi")
           Guinness Records, Hydraulic Press, Physics Experiments, Viral Stunts,
           MrBeast Challenges, Trick Shots & Caught-on-Camera Moments.

Guarantees:
- ZERO repeated source IDs or near-duplicate titles via HistoryTracker
- ZERO reused pre-cached static pools
- ZERO repeated thumbnails via 64-bit perceptual dHash verification
"""

import glob
import json
import os
import random
import re
import subprocess
import sys
import urllib.request
from datetime import datetime
from typing import Any, Dict, List, Optional, Set, Tuple

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

try:
    from history_tracker import HistoryTracker
except ModuleNotFoundError:
    from src.history_tracker import HistoryTracker

from src.gemini_engine import GeminiEngine
from src.thumbnail_generator import ThumbnailGenerator


GAMING_QUERY_POOL: List[Dict[str, str]] = [
    {"q": "GTA 6 viral gameplay trailer reaction shorts", "creator": "GTA VI", "lang": "en", "banner": "GTA 6 IS INSANE!"},
    {"q": "GTA VI secret details trailer breakdown viral shorts", "creator": "GTA VI", "lang": "en", "banner": "GTA 6 HIDDEN DETAILS!"},
    {"q": "IShowSpeed GTA 6 reaction rage gaming shorts", "creator": "IShowSpeed", "lang": "en", "banner": "SPEED ON GTA 6!"},
    {"q": "Techno Gamerz GTA 6 GTA 5 trending gameplay shorts", "creator": "Techno Gamerz", "lang": "hi", "banner": "TECHNO GAMERZ GTA!"},
    {"q": "Marvel Rivals insane clutch viral gaming shorts", "creator": "Marvel Rivals", "lang": "en", "banner": "MARVEL RIVALS INSANE!"},
    {"q": "CarryMinati trending game live reaction shorts", "creator": "CarryMinati", "lang": "hi", "banner": "CARRYMINATI OP REACTION!"},
    {"q": "Kai Cenat trending game viral reaction shorts", "creator": "Kai Cenat", "lang": "en", "banner": "KAI CENAT CRAZY MOMENT!"},
    {"q": "Triggered Insaan trending game funny shorts", "creator": "Triggered Insaan", "lang": "hi", "banner": "TRIGGERED INSAAN FUNNY!"},
    {"q": "GTA 5 FiveM RP craziest viral stunt shorts", "creator": "GTA 5 RP", "lang": "en", "banner": "GTA IMPOSSIBLE STUNT!"},
    {"q": "Total Gaming Ajju Bhai trending clutch shorts", "creator": "Total Gaming", "lang": "hi", "banner": "AJJU BHAI OP MOMENT!"},
    {"q": "Black Myth Wukong Elden Ring insane boss fight shorts", "creator": "Trending RPG", "lang": "en", "banner": "UNREAL BOSS FIGHT!"},
    {"q": "Scout OP BGMI insane 1v4 clutch shorts", "creator": "Scout", "lang": "hi", "banner": "SCOUT 1V4 INSANE CLUTCH!"},
    {"q": "CaseOh trending horror game jumpscare shorts", "creator": "CaseOh", "lang": "en", "banner": "CASEOH JUMPSCARE RAGE!"},
    {"q": "Valorant craziest ace streamer reaction shorts", "creator": "Valorant", "lang": "en", "banner": "IMPOSSIBLE VALORANT ACE!"},
    {"q": "BeastBoyShub trending horror game reaction shorts", "creator": "BeastBoyShub", "lang": "hi", "banner": "BBS CRAZY REACTION!"},
    {"q": "FC 26 FIFA craziest goal viral gaming shorts", "creator": "EA Sports FC 26", "lang": "en", "banner": "IMPOSSIBLE FC 26 GOAL!"},
    {"q": "Payal Gaming live stream trending clutch shorts", "creator": "Payal Gaming", "lang": "hi", "banner": "LIVE STREAM CHAOS!"},
    {"q": "MrBeast Gaming trending challenge shorts", "creator": "MrBeast Gaming", "lang": "en", "banner": "CRAZIEST GAMING CHALLENGE!"},
]

VIRAL_TRENDING_POOL: List[Dict[str, str]] = [
    {"q": "100 ton hydraulic press vs strongest object shorts", "creator": "Viral Science", "lang": "en", "banner": "100 TON HYDRAULIC PRESS!"},
    {"q": "craziest guinness world record viral shorts", "creator": "World Records", "lang": "en", "banner": "INSANE WORLD RECORD!"},
    {"q": "mrbeast craziest viral challenge moment shorts", "creator": "MrBeast", "lang": "en", "banner": "UNBELIEVABLE CHALLENGE!"},
    {"q": "impossible trick shot viral video shorts", "creator": "Trick Shots", "lang": "en", "banner": "99% IMPOSSIBLE SHOT!"},
    {"q": "most viral mind blowing physics trick shorts", "creator": "Physics Magic", "lang": "en", "banner": "SCIENCE OR MAGIC?!"},
    {"q": "death defying parkour jump viral shorts", "creator": "Extreme Stunts", "lang": "en", "banner": "DO NOT TRY THIS!"},
    {"q": "most satisfying domino chain reaction shorts", "creator": "Viral Satisfying", "lang": "en", "banner": "MOST SATISFYING VIDEO!"},
    {"q": "unbelievable caught on camera viral shorts", "creator": "Viral Moments", "lang": "en", "banner": "CAUGHT ON CAMERA!"},
    {"q": "optical illusion viral brain trick shorts", "creator": "Illusions", "lang": "en", "banner": "YOUR EYES ARE LYING!"},
    {"q": "insane human talent viral clip shorts", "creator": "Viral Talent", "lang": "en", "banner": "NEXT LEVEL TALENT!"},
    {"q": "trending viral video india funny shocking shorts", "creator": "India Viral", "lang": "hi", "banner": "VIRAL MOMENT TODAY!"},
    {"q": "crushing lava vs ice hydraulic press shorts", "creator": "Viral Experiments", "lang": "en", "banner": "LAVA VS HYDRAULIC PRESS!"},
]


TWITCH_GAMING_SOURCES: List[Dict[str, str]] = [
    {"kind": "game", "name": "Grand Theft Auto VI", "creator": "GTA VI Viral", "banner": "GTA 6 TRENDING CLIP!"},
    {"kind": "game", "name": "Marvel Rivals", "creator": "Marvel Rivals Viral", "banner": "INSANE MARVEL RIVALS PLAY!"},
    {"kind": "game", "name": "Grand Theft Auto V", "creator": "GTA 5 Viral", "banner": "GTA 5 INSANE CLIP!"},
    {"kind": "user", "name": "kaicenat", "creator": "Kai Cenat", "banner": "KAI CENAT CRAZY STREAM!"},
    {"kind": "game", "name": "EA Sports FC 26", "creator": "FC 26 Viral", "banner": "CRAZY FC 26 GOAL!"},
    {"kind": "game", "name": "Call of Duty: Warzone", "creator": "Warzone Viral", "banner": "UNREAL WARZONE CLUTCH!"},
    {"kind": "user", "name": "caseoh_", "creator": "CaseOh", "banner": "CASEOH INSANE REACTION!"},
    {"kind": "game", "name": "VALORANT", "creator": "Valorant Viral", "banner": "IMPOSSIBLE VALORANT PLAY!"},
    {"kind": "game", "name": "Elden Ring", "creator": "Elden Ring Viral", "banner": "INSANE BOSS CLUTCH!"},
    {"kind": "user", "name": "jynxzi", "creator": "Jynxzi", "banner": "JYNXZI FUNNIEST RAGE!"},
    {"kind": "game", "name": "Fortnite", "creator": "Fortnite Viral", "banner": "INSANE FORTNITE CLUTCH!"},
    {"kind": "game", "name": "Counter-Strike", "creator": "CS2 Viral", "banner": "UNREAL CS2 ACE!"},
    {"kind": "user", "name": "xqc", "creator": "xQc", "banner": "XQC UNHINGED MOMENT!"},
    {"kind": "user", "name": "tarik", "creator": "Tarik", "banner": "INSANE PRO CLUTCH!"},
]


class DynamicCreatorEngine:
    """Manages live discovery, clipping, and zero-repeat formatting for Channels 2 & 3."""

    def __init__(self, downloads_dir: str = "assets/downloads", output_dir: str = "output/batch_today"):
        self.downloads_dir = downloads_dir
        self.output_dir = output_dir
        self.tracker = HistoryTracker()
        self.gemini = GeminiEngine()
        self.thumb_gen = ThumbnailGenerator(output_dir=output_dir)
        os.makedirs(self.downloads_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)

    @staticmethod
    def _clean_banner(banner_text: str) -> str:
        cleaned = re.sub(r'[^\w\s!?,.$#@\-%/:]', '', str(banner_text or ''))
        cleaned = cleaned.replace(":", "\\:").replace("'", "").replace('"', "").strip()
        return cleaned[:42] or "VIRAL CLIP"

    @staticmethod
    def _get_font_opt() -> str:
        candidates = [
            ("C:/Windows/Fonts/impact.ttf", "C\\:/Windows/Fonts/impact.ttf"),
            ("C:/Windows/Fonts/arialbd.ttf", "C\\:/Windows/Fonts/arialbd.ttf"),
            ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
            ("/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf", "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"),
        ]
        for check_path, esc_path in candidates:
            if os.path.exists(check_path):
                return f"fontfile='{esc_path}':"
        return ""

    @staticmethod
    def _probe_streams(file_path: str) -> Dict[str, Any]:
        try:
            cmd = [
                "ffprobe", "-v", "error",
                "-show_entries", "format=duration:stream=codec_type,width,height",
                "-of", "json",
                file_path
            ]
            out = subprocess.check_output(cmd, text=True, timeout=15)
            data = json.loads(out)
            streams = data.get("streams", [])
            has_video = any(s.get("codec_type") == "video" for s in streams)
            has_audio = any(s.get("codec_type") == "audio" for s in streams)
            dur = float(data.get("format", {}).get("duration", 0) or 0)
            return {"duration": dur, "has_video": has_video, "has_audio": has_audio}
        except Exception:
            return {"duration": 0.0, "has_video": False, "has_audio": False}

    def _build_metadata(
        self,
        raw_title: str,
        niche_mode: str,
        cfg: Dict[str, str],
        vid_id: str,
    ) -> Dict[str, Any]:
        clean_src_title = re.sub(r'#\S+', '', raw_title or '').strip()
        # Keep the video's native language (if Hindi/Devanagari/Indian creator -> Hindi/Hinglish style; else English)
        has_devanagari = bool(re.search(r'[\u0900-\u097F]', clean_src_title))
        lang = "hi" if (has_devanagari or cfg.get("lang") == "hi") else "en"
        creator = cfg.get("creator", "Creator")

        if self.gemini.is_available():
            try:
                lang_note = (
                    "Match the clip's original Hindi/Hinglish vibe (clean Hindi or Hinglish title with emoji + #Shorts)."
                    if lang == "hi"
                    else "Keep 100% English Latin script title with shock emoji + #Shorts."
                )
                prompt = f"""
Create a punchy YouTube Shorts title, top banner text, and short description for this {niche_mode} clip.
Original source video title: "{clean_src_title}"
Creator/Category: {creator}
Language Rule: {lang_note}
Rules:
1. Title must be unique, under 68 chars, catchy, ending with #Shorts
2. Banner must be 2 to 4 UPPERCASE ENGLISH WORDS ONLY (no emojis) for top video overlay (e.g. "SPEED GOES INSANE!", "CARRYMINATI RAGE!")
3. Description: 2 short lines + 5 relevant hashtags

Return strict JSON:
{{"title": "...", "banner": "...", "description": "...", "tags": ["shorts", "viral", "..."]}}
"""
                res = self.gemini._call_gemini_json(prompt)
                if res.get("title"):
                    title = str(res["title"]).strip()
                    if "#Shorts" not in title:
                        title = title[:88].strip() + " #Shorts"
                    return {
                        "title": title[:96],
                        "banner": str(res.get("banner") or cfg["banner"]).strip(),
                        "description": str(res.get("description") or f"{clean_src_title}\n\n#Shorts #Viral").strip(),
                        "tags": res.get("tags") or ["shorts", "viral", niche_mode, creator.lower().replace(" ", "")],
                    }
            except Exception as e:
                print(f"Notice: Gemini metadata fallback ({e})")

        base = clean_src_title[:55].strip() if clean_src_title else f"{creator} Viral Moment"
        suffix = "🎮🔥 #Shorts" if niche_mode == "gaming" else "😱🔥 #Shorts"
        return {
            "title": f"{base} {suffix}"[:96],
            "banner": cfg["banner"],
            "description": f"{clean_src_title or creator}\n\n#Shorts #Viral #Trending #{creator.replace(' ', '')}",
            "tags": ["shorts", "viral", niche_mode, creator.lower().replace(" ", ""), "trending"],
        }

    def _discover_twitch_candidates(
        self,
        slot_index: int,
        day_offset: int,
        session_ids: Set[str],
    ) -> List[Tuple[str, str, float, str, Dict[str, str]]]:
        """Queries Twitch GraphQL for top viral English/Hindi gaming clips (immune to Google datacenter bot blocks)."""
        results: List[Tuple[str, str, float, str, Dict[str, str]]] = []
        start_idx = (day_offset * 5 + slot_index - 1) % len(TWITCH_GAMING_SOURCES)
        for offset in range(len(TWITCH_GAMING_SOURCES)):
            src = TWITCH_GAMING_SOURCES[(start_idx + offset) % len(TWITCH_GAMING_SOURCES)]
            name = src["name"]
            if src["kind"] == "user":
                gql = f'query {{ user(login: "{name}") {{ clips(first: 15, criteria: {{ period: LAST_WEEK }}) {{ edges {{ node {{ slug title url durationSeconds viewCount broadcaster {{ displayName }} }} }} }} }} }}'
            else:
                gql = f'query {{ game(name: "{name}") {{ clips(first: 15, criteria: {{ period: LAST_WEEK, languages: [EN, HI] }}) {{ edges {{ node {{ slug title url durationSeconds viewCount broadcaster {{ displayName }} }} }} }} }} }}'
            try:
                req = urllib.request.Request(
                    "https://gql.twitch.tv/gql",
                    data=json.dumps({"query": gql}).encode("utf-8"),
                    headers={
                        "Client-ID": "kimne78kx3ncx6brgo4mv6wki5h1ko",
                        "Content-Type": "application/json",
                        "User-Agent": "Mozilla/5.0",
                    },
                )
                payload = json.loads(urllib.request.urlopen(req, timeout=12).read().decode("utf-8"))
                container = (payload.get("data") or {}).get(src["kind"]) or {}
                edges = (container.get("clips") or {}).get("edges") or []
                for edge in edges:
                    node = (edge or {}).get("node") or {}
                    slug = node.get("slug", "")
                    title = node.get("title", "")
                    dur = float(node.get("durationSeconds") or 0)
                    bname = (node.get("broadcaster") or {}).get("displayName") or src["creator"]
                    if not slug or slug in session_ids or self.tracker.is_source_used(slug) or self.tracker.is_title_used(title):
                        continue
                    if dur < 10 or dur > 60:
                        continue
                    cfg_item = {"creator": bname, "lang": "en", "banner": src["banner"]}
                    results.append((slug, title, dur, node.get("url") or f"https://clips.twitch.tv/{slug}", cfg_item))
                if len(results) >= 8:
                    break
            except Exception as e:
                print(f"Notice: Twitch query failed for {name}: {e}")
        return results

    def _finalize_clip(
        self,
        raw_file: str,
        vid_id: str,
        vid_title: str,
        target_url: str,
        mode: str,
        cfg: Dict[str, str],
        slot_index: int,
        output_video_path: str,
        output_thumb_path: str,
        session_ids: Set[str],
        batch_hashes: Optional[Set[str]],
        require_audio: bool,
        query: str,
    ) -> Optional[Dict[str, Any]]:
        probe = self._probe_streams(raw_file)
        if not probe["has_video"] or probe["duration"] < 8.0:
            try:
                os.remove(raw_file)
            except Exception:
                pass
            return None
        if require_audio and not probe["has_audio"]:
            print(f"⚠️ Skipping {vid_id} — missing authentic audio track.")
            try:
                os.remove(raw_file)
            except Exception:
                pass
            return None

        meta = self._build_metadata(vid_title, mode, cfg, vid_id)
        if self.tracker.is_title_used(meta["title"]):
            meta["title"] = f"{meta['title'].replace('#Shorts', '').strip()[:62]} [{vid_id[:4]}] #Shorts"

        render_dur = min(31.0, max(10.0, probe["duration"] - 0.1))
        clean_banner = self._clean_banner(meta["banner"])
        font_opt = self._get_font_opt()
        os.makedirs(os.path.dirname(output_video_path) or ".", exist_ok=True)

        vf = (
            "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,"
            f"drawtext={font_opt}text='{clean_banner}':fontsize=50:fontcolor=yellow:box=1:boxcolor=black@0.85:boxborderw=18:x=(w-text_w)/2:y=210[v]"
        )
        ff_cmd = [
            "ffmpeg", "-y",
            "-i", raw_file,
            "-t", f"{render_dur:.2f}",
            "-filter_complex", vf,
            "-map", "[v]",
            "-map", "0:a?" if not require_audio else "0:a",
            "-af", "loudnorm=I=-14:TP=-1.5:LRA=11",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
            output_video_path
        ]
        ff_res = subprocess.run(ff_cmd, capture_output=True, text=True)
        if ff_res.returncode != 0 or not os.path.exists(output_video_path):
            print(f"⚠️ FFmpeg format failed for {vid_id}: {ff_res.stderr[-200:]}")
            return None

        thumb_path = self.thumb_gen.generate(
            video_path=raw_file,
            output_thumb_path=output_thumb_path,
            badge_text=meta["banner"],
            timestamp_sec=min(3.5, render_dur * 0.4),
            slot_index=slot_index,
            tracker=self.tracker,
            batch_hashes=batch_hashes,
        )

        session_ids.add(vid_id)
        try:
            os.remove(raw_file)
        except Exception:
            pass

        return {
            "video_path": output_video_path,
            "thumbnail_path": thumb_path,
            "thumbnail_dhash": self.thumb_gen.last_dhash,
            "duration": render_dur,
            "title": meta["title"],
            "description": meta["description"],
            "tags": meta["tags"],
            "source_id": vid_id,
            "source_url": target_url,
            "creator": cfg["creator"],
            "query": query,
        }

    def discover_and_render_slot(
        self,
        mode: str,
        slot_index: int,
        output_video_path: str,
        output_thumb_path: str,
        day_offset: int = 0,
        session_used_ids: Optional[Set[str]] = None,
        batch_hashes: Optional[Set[str]] = None,
        require_audio: bool = True,
    ) -> Optional[Dict[str, Any]]:
        """
        Discovers a 100% never-before-used clip via YouTube (with Node JS runtime)
        and automatically falls back to Twitch Viral Gaming Clips on cloud IPs
        if YouTube bot-blocks datacenter downloads.
        """
        pool = GAMING_QUERY_POOL if mode == "gaming" else VIRAL_TRENDING_POOL
        session_ids = session_used_ids if session_used_ids is not None else set()
        start_q_idx = (day_offset * 7 + slot_index - 1) % len(pool)

        # 1. Try YouTube discovery (try up to 3 rotating queries, 3 candidates each)
        yt_bot_blocked = False
        for q_offset in range(min(3, len(pool))):
            if yt_bot_blocked:
                break
            cfg = pool[(start_q_idx + q_offset) % len(pool)]
            query = cfg["q"]
            print(f"🔍 [{mode.upper()} | Slot {slot_index}] Searching YouTube: '{query}'...")

            search_cmd = [
                sys.executable, "-m", "yt_dlp",
                "--no-update",
                "--js-runtimes", "node",
                "--extractor-args", "youtube:player_client=android,tv,web",
                "--flat-playlist",
                "--print", "%(id)s|||%(title)s|||%(duration)s",
                f"ytsearch15:{query}"
            ]
            candidates = []
            try:
                res = subprocess.run(search_cmd, capture_output=True, text=True, timeout=30)
                for line in res.stdout.splitlines():
                    parts = line.strip().split("|||", 2)
                    if len(parts) != 3:
                        continue
                    vid_id, vid_title, dur_raw = parts[0].strip(), parts[1].strip(), parts[2].strip()
                    if not vid_id or len(vid_id) != 11:
                        continue
                    if vid_id in session_ids or self.tracker.is_source_used(vid_id) or self.tracker.is_title_used(vid_title):
                        continue
                    try:
                        dur = float(dur_raw) if dur_raw not in ("NA", "None", "") else 45.0
                    except ValueError:
                        dur = 45.0
                    if 10 <= dur <= 3600:
                        candidates.append((vid_id, vid_title, dur))
            except Exception as e:
                print(f"Warning: yt-dlp search error for '{query}': {e}")
                continue

            for vid_id, vid_title, dur in candidates[:3]:
                target_url = f"https://www.youtube.com/watch?v={vid_id}"
                out_prefix = f"fresh_{mode}_{vid_id}"
                out_tmpl = os.path.join(self.downloads_dir, f"{out_prefix}.%(ext)s")

                if dur <= 58:
                    t_start, t_end = 0, min(33, int(dur))
                else:
                    t_start = max(15, min(int(dur * 0.32), int(dur) - 32))
                    t_end = t_start + 30

                sec_spec = f"*{t_start // 3600:02d}:{(t_start % 3600) // 60:02d}:{t_start % 60:02d}-{t_end // 3600:02d}:{(t_end % 3600) // 60:02d}:{t_end % 60:02d}"
                dl_cmd = [
                    sys.executable, "-m", "yt_dlp",
                    "--no-update",
                    "--js-runtimes", "node",
                    "--extractor-args", "youtube:player_client=android,tv,web",
                    "-f", "bv*[height<=720]+ba/b[height<=720]/b",
                    "--merge-output-format", "mp4",
                    "--download-sections", sec_spec,
                    "--force-keyframes-at-cuts",
                    "-o", out_tmpl,
                    "--no-playlist",
                    target_url
                ]

                print(f"📥 Downloading YouTube {vid_id} ({sec_spec})...")
                try:
                    dl_res = subprocess.run(dl_cmd, capture_output=True, text=True, timeout=55)
                    if dl_res.returncode != 0:
                        err_tail = (dl_res.stderr or "").strip().splitlines()[-2:]
                        err_msg = " | ".join(err_tail)
                        print(f"⚠️ yt-dlp YouTube error ({vid_id}): {err_msg[:180]}")
                        if "Sign in to confirm" in (dl_res.stderr or "") or "not a bot" in (dl_res.stderr or ""):
                            yt_bot_blocked = True
                            break
                        continue
                except Exception as dl_exc:
                    print(f"⚠️ Download timeout/error ({vid_id}): {dl_exc}")
                    continue

                found = [f for f in glob.glob(os.path.join(self.downloads_dir, f"{out_prefix}*.*")) if not f.endswith(".part")]
                if not found or os.path.getsize(found[0]) < 150000:
                    continue

                finalized = self._finalize_clip(
                    raw_file=found[0],
                    vid_id=vid_id,
                    vid_title=vid_title,
                    target_url=target_url,
                    mode=mode,
                    cfg=cfg,
                    slot_index=slot_index,
                    output_video_path=output_video_path,
                    output_thumb_path=output_thumb_path,
                    session_ids=session_ids,
                    batch_hashes=batch_hashes,
                    require_audio=require_audio,
                    query=query,
                )
                if finalized:
                    return finalized

        # 2. Twitch Viral Gaming Clips (works 100% cleanly on GitHub Actions cloud IPs without Google bot blocks!)
        if mode == "gaming":
            print(f"🎮 [GAMING | Slot {slot_index}] Discovering fresh viral Twitch gaming clips...")
            tw_cands = self._discover_twitch_candidates(slot_index, day_offset, session_ids)
            for slug, tw_title, dur, tw_url, cfg_item in tw_cands[:6]:
                out_prefix = f"fresh_twitch_{slug[:24]}"
                out_tmpl = os.path.join(self.downloads_dir, f"{out_prefix}.%(ext)s")
                dl_cmd = [
                    sys.executable, "-m", "yt_dlp",
                    "--no-update",
                    "-f", "b/bv*[height<=720]+ba/best",
                    "-o", out_tmpl,
                    "--no-playlist",
                    tw_url,
                ]
                print(f"📥 Downloading Twitch clip {slug[:20]} ({cfg_item['creator']})...")
                try:
                    dl_res = subprocess.run(dl_cmd, capture_output=True, text=True, timeout=45)
                    if dl_res.returncode != 0:
                        print(f"⚠️ Twitch download err: {(dl_res.stderr or '')[-150:]}")
                        continue
                except Exception as exc:
                    print(f"⚠️ Twitch timeout: {exc}")
                    continue

                found = [f for f in glob.glob(os.path.join(self.downloads_dir, f"{out_prefix}*.*")) if not f.endswith(".part")]
                if not found or os.path.getsize(found[0]) < 150000:
                    continue

                finalized = self._finalize_clip(
                    raw_file=found[0],
                    vid_id=slug,
                    vid_title=tw_title,
                    target_url=tw_url,
                    mode=mode,
                    cfg=cfg_item,
                    slot_index=slot_index,
                    output_video_path=output_video_path,
                    output_thumb_path=output_thumb_path,
                    session_ids=session_ids,
                    batch_hashes=batch_hashes,
                    require_audio=require_audio,
                    query=f"twitch:{cfg_item['creator']}",
                )
                if finalized:
                    return finalized

        return None
