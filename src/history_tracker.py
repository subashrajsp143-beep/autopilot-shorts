"""
Upload History Tracker
----------------------
Maintains a permanent database of all uploaded video titles, source clip IDs,
and script topics to guarantee 100% uniqueness and prevent duplicate uploads.
"""

import os
import sys
import json
from datetime import datetime
from typing import Dict, Any, List, Optional

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


class HistoryTracker:
    def __init__(self, history_file: str = "config/uploaded_history.json"):
        self.history_file = history_file
        self.history: Dict[str, Any] = self._load_history()

    def _load_history(self) -> Dict[str, Any]:
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "uploaded_video_ids": [],
            "used_source_ids": [],
            "used_queries": [],
            "used_script_titles": [],
            "upload_logs": []
        }

    def save(self):
        os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
        try:
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Warning: Failed to save history tracker: {e}")

    def is_source_used(self, source_id: str) -> bool:
        """Returns True if the source video has already been clipped before."""
        return source_id in self.history.get("used_source_ids", [])

    def is_title_used(self, title: str) -> bool:
        """Returns True if an identical title was already uploaded."""
        clean = title.strip().lower()
        return any(clean == t.strip().lower() for t in self.history.get("used_script_titles", []))

    def record_upload(
        self,
        title: str,
        video_type: str,
        youtube_video_id: Optional[str] = None,
        source_id: Optional[str] = None,
        query: Optional[str] = None
    ):
        """Records an upload into history."""
        if title:
            self.history.setdefault("used_script_titles", []).append(title)
        if youtube_video_id:
            self.history.setdefault("uploaded_video_ids", []).append(youtube_video_id)
        if source_id:
            self.history.setdefault("used_source_ids", []).append(source_id)
        if query:
            self.history.setdefault("used_queries", []).append(query)

        self.history.setdefault("upload_logs", []).append({
            "timestamp": datetime.now().isoformat(),
            "title": title,
            "type": video_type,
            "youtube_id": youtube_video_id,
            "source_id": source_id,
            "query": query
        })
        self.save()


if __name__ == "__main__":
    tracker = HistoryTracker()
    print("History tracker initialized. Used source clips:", len(tracker.history.get("used_source_ids", [])))
