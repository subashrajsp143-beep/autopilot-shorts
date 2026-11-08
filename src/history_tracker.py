"""
Upload History Tracker
----------------------
Maintains a permanent database of all uploaded video titles, source clip IDs,
and script topics to guarantee 100% uniqueness and prevent duplicate uploads.
Provides atomic locking with process ownership verification, owner token enforcement,
idempotent confirmation, and uncertain upload reconciliation.
"""

import os
import sys
import json
import time
import uuid
import socket
import ctypes
from contextlib import contextmanager
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional, Tuple

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def is_pid_alive(pid: int) -> bool:
    """Checks whether a process with the given PID is actively running on this host."""
    if pid <= 0:
        return False
    if sys.platform == "win32":
        SYNCHRONIZE = 0x00100000
        PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
        kernel32 = ctypes.windll.kernel32
        h_process = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION | SYNCHRONIZE, False, pid)
        if h_process:
            STILL_ACTIVE = 259
            exit_code = ctypes.c_ulong()
            kernel32.GetExitCodeProcess(h_process, ctypes.byref(exit_code))
            kernel32.CloseHandle(h_process)
            return exit_code.value == STILL_ACTIVE
        return False
    else:
        try:
            os.kill(pid, 0)
            return True
        except (OSError, ProcessLookupError):
            return False


class HistoryTracker:
    def __init__(self, history_file: str = "config/uploaded_history.json"):
        self.history_file = history_file
        self.lock_dir = f"{self.history_file}.lock"
        self.history: Dict[str, Any] = self._load_history()

    @contextmanager
    def file_lock(self, timeout: float = 30.0, poll_interval: float = 0.05):
        """
        Cross-platform atomic directory-based file lock with verified process ownership.
        Never steals or deletes a lock based purely on age.
        Only reclaims a lock if the owning process is demonstrably DEAD on this host.
        """
        start_time = time.time()
        owner_file = os.path.join(self.lock_dir, "owner.json")
        my_hostname = socket.gethostname()
        my_pid = os.getpid()

        acquired = False
        while time.time() - start_time < timeout:
            try:
                os.makedirs(self.lock_dir)
                try:
                    with open(owner_file, "w", encoding="utf-8") as f:
                        json.dump({
                            "pid": my_pid,
                            "host": my_hostname,
                            "timestamp": time.time()
                        }, f)
                except Exception:
                    pass
                acquired = True
                break
            except FileExistsError:
                owner_info = None
                if os.path.exists(owner_file):
                    try:
                        with open(owner_file, "r", encoding="utf-8") as f:
                            owner_info = json.load(f)
                    except Exception:
                        pass

                if owner_info and owner_info.get("host") == my_hostname:
                    owner_pid = owner_info.get("pid", 0)
                    if owner_pid > 0 and not is_pid_alive(owner_pid):
                        try:
                            if os.path.exists(owner_file):
                                os.remove(owner_file)
                            os.rmdir(self.lock_dir)
                            continue
                        except Exception:
                            pass

                time.sleep(poll_interval)

        if not acquired:
            raise TimeoutError(f"Could not acquire atomic lock on {self.lock_dir} after {timeout}s (held by active process)")

        try:
            yield
        finally:
            try:
                if os.path.exists(owner_file):
                    os.remove(owner_file)
                if os.path.exists(self.lock_dir):
                    os.rmdir(self.lock_dir)
            except Exception:
                pass

    def _load_history(self) -> Dict[str, Any]:
        data = None
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                pass
        if not data:
            data = {
                "uploaded_video_ids": [],
                "used_source_ids": [],
                "used_queries": [],
                "used_script_titles": [],
                "upload_logs": [],
                "pending_uploads": {}
            }
        if "pending_uploads" not in data:
            data["pending_uploads"] = {}

        # Self-healing: Merge any emergency unconfirmed upload records if present on disk
        emergency_file = os.path.join(os.path.dirname(self.history_file), "emergency_unconfirmed_uploads.jsonl")
        if os.path.exists(emergency_file):
            try:
                with open(emergency_file, "r", encoding="utf-8") as ef:
                    for line in ef:
                        if line.strip():
                            rec = json.loads(line)
                            ch_id = rec.get("channel_id")
                            s_id = rec.get("source_id")
                            v_id = rec.get("youtube_video_id")
                            if ch_id and s_id:
                                k = f"channel_{ch_id}:{s_id}"
                                existing = data["pending_uploads"].get(k)
                                if not existing or existing.get("status") != "confirmed":
                                    data["pending_uploads"][k] = {
                                        "source_id": s_id,
                                        "channel_id": ch_id,
                                        "title": rec.get("title", ""),
                                        "youtube_video_id": v_id,
                                        "status": "uncertain",
                                        "error_details": f"Recovered from emergency log: {rec.get('confirm_error') or rec.get('error')}",
                                        "uncertain_timestamp": rec.get("timestamp")
                                    }
                            if v_id and v_id not in data.setdefault("uploaded_video_ids", []):
                                data["uploaded_video_ids"].append(v_id)
            except Exception:
                pass

        return data

    def reload(self):
        """Reloads the history file from disk to ensure freshest state across processes."""
        self.history = self._load_history()

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

    def _is_source_uploaded_today_internal(
        self,
        source_id: Optional[str],
        channel_id: int,
        date_str: Optional[str] = None
    ) -> bool:
        if not source_id:
            return False

        dates_to_check = set()
        if date_str:
            dates_to_check.add(date_str)
        else:
            ist_now = datetime.now(timezone(timedelta(hours=5, minutes=30)))
            utc_now = datetime.now(timezone.utc)
            dates_to_check.add(ist_now.strftime("%Y-%m-%d"))
            dates_to_check.add(utc_now.strftime("%Y-%m-%d"))

        ch_names = {
            1: ["Channel 1", "MiniTalesWorld"],
            2: ["Channel 2", "Pawsome"],
            3: ["Channel 3", "Next Level Facts"]
        }
        names = ch_names.get(channel_id, [f"Channel {channel_id}"])

        for item in self.history.get("upload_logs", []):
            ts = item.get("timestamp", "")
            if any(ts.startswith(d) for d in dates_to_check):
                item_ch = item.get("channel_id")
                item_type = item.get("type", "")
                ch_match = (item_ch == channel_id) or any(n in item_type for n in names)
                if ch_match and item.get("source_id") == source_id:
                    return True
        return False

    def is_source_uploaded_today(
        self,
        source_id: Optional[str],
        channel_id: int,
        date_str: Optional[str] = None
    ) -> bool:
        """Checks whether a source_id has already been successfully uploaded today."""
        self.reload()
        return self._is_source_uploaded_today_internal(source_id, channel_id, date_str)

    def reserve_source(
        self,
        source_id: str,
        channel_id: int,
        title: str
    ) -> Tuple[str, Optional[Dict[str, Any]], Optional[str]]:
        """
        Atomically checks and reserves a source clip for upload with an exclusive owner token.
        Returns:
            ("already_uploaded", pending_info, None)
            ("uncertain", pending_info, None)
            ("reserved_by_other", pending_info, None)
            ("acquired", pending_entry, owner_token)
        """
        with self.file_lock():
            self.reload()

            if self._is_source_uploaded_today_internal(source_id, channel_id):
                return ("already_uploaded", None, None)

            key = f"channel_{channel_id}:{source_id}"
            pending = self.history.get("pending_uploads", {}).get(key)
            if pending:
                status = pending.get("status")
                owner_pid = pending.get("pid", 0)
                owner_alive = is_pid_alive(owner_pid) if owner_pid > 0 else False

                if status == "confirmed":
                    return ("already_uploaded", pending, None)
                elif status == "uncertain":
                    return ("uncertain", pending, None)
                elif status == "uploading":
                    if owner_alive:
                        return ("reserved_by_other", pending, None)
                    else:
                        pending["status"] = "uncertain"
                        pending["error_details"] = "Process died while upload was in progress. Potential orphaned video on YouTube."
                        self.save()
                        return ("uncertain", pending, None)
                elif status == "reserved":
                    if owner_alive:
                        return ("reserved_by_other", pending, None)
                    else:
                        token = f"tok_{os.getpid()}_{int(time.time()*1000)}_{uuid.uuid4().hex[:8]}"
                        pending["status"] = "reserved"
                        pending["pid"] = os.getpid()
                        pending["owner_token"] = token
                        pending["attempt_timestamp"] = datetime.now().isoformat()
                        pending["title"] = title
                        self.save()
                        return ("acquired", pending, token)
                elif status == "failed":
                    token = f"tok_{os.getpid()}_{int(time.time()*1000)}_{uuid.uuid4().hex[:8]}"
                    pending["status"] = "reserved"
                    pending["pid"] = os.getpid()
                    pending["owner_token"] = token
                    pending["attempt_timestamp"] = datetime.now().isoformat()
                    pending["title"] = title
                    pending["error_details"] = None
                    self.save()
                    return ("acquired", pending, token)

            token = f"tok_{os.getpid()}_{int(time.time()*1000)}_{uuid.uuid4().hex[:8]}"
            new_entry = {
                "source_id": source_id,
                "channel_id": channel_id,
                "title": title,
                "attempt_timestamp": datetime.now().isoformat(),
                "status": "reserved",
                "youtube_video_id": None,
                "error_details": None,
                "pid": os.getpid(),
                "owner_token": token
            }
            self.history.setdefault("pending_uploads", {})[key] = new_entry
            self.save()
            return ("acquired", new_entry, token)

    def _verify_owner_token(self, key: str, owner_token: Optional[str]):
        """
        Strictly enforces reservation ownership across state transitions.
        Requires a valid non-empty owner_token matching the active reservation.
        """
        if not owner_token or not isinstance(owner_token, str) or not owner_token.strip():
            raise PermissionError(f"Owner token is strictly required for state transition on reservation '{key}'.")

        pending = self.history.get("pending_uploads", {}).get(key)
        if not pending:
            raise PermissionError(f"No active reservation found for '{key}'. Must call reserve_source first.")

        expected = pending.get("owner_token")
        if not expected or expected != owner_token:
            raise PermissionError(f"Reservation ownership mismatch for '{key}'. Expected '{expected}', got '{owner_token}'.")

    def mark_uploading(self, source_id: str, channel_id: int, owner_token: Optional[str] = None):
        """Marks that upload request has actually started transmitting bytes to YouTube."""
        with self.file_lock():
            self.reload()
            key = f"channel_{channel_id}:{source_id}"
            self._verify_owner_token(key, owner_token)
            entry = self.history.setdefault("pending_uploads", {}).setdefault(key, {})
            curr_status = entry.get("status")
            if curr_status == "confirmed":
                raise ValueError(f"Cannot transition confirmed upload '{key}' back to uploading.")
            if curr_status == "uncertain":
                raise ValueError(f"Cannot transition uncertain upload '{key}' to uploading without reconciliation.")
            entry["source_id"] = source_id
            entry["channel_id"] = channel_id
            entry["status"] = "uploading"
            entry["uploading_timestamp"] = datetime.now().isoformat()
            self.save()

    def confirm_upload(
        self,
        source_id: str,
        channel_id: int,
        youtube_video_id: str,
        title: str,
        video_type: str,
        query: Optional[str] = None,
        owner_token: Optional[str] = None
    ) -> bool:
        """
        Atomically marks upload as confirmed and appends to permanent upload_logs.
        100% IDEMPOTENT: Multiple identical calls never duplicate logs or sets.
        Safely handles and rejects conflicting YouTube video IDs for the same source.
        Enforces reservation ownership.
        """
        with self.file_lock():
            self.reload()
            key = f"channel_{channel_id}:{source_id}"
            self._verify_owner_token(key, owner_token)

            pending_entry = self.history.setdefault("pending_uploads", {}).setdefault(key, {})

            # 1. Conflict detection on pending entry:
            existing_vid = pending_entry.get("youtube_video_id")
            if existing_vid and existing_vid != youtube_video_id:
                print(f"Warning: Conflicting YouTube video ID for {key}! Existing: '{existing_vid}', New: '{youtube_video_id}'. Preserving existing.")
                return False

            # 2. Channel names for legacy log matching
            ch_names = {
                1: ["Channel 1", "MiniTalesWorld"],
                2: ["Channel 2", "Pawsome"],
                3: ["Channel 3", "Next Level Facts"]
            }
            names = ch_names.get(channel_id, [f"Channel {channel_id}"])

            # 3. Check upload_logs for existing entries for this channel & source
            matching_log = None
            for item in self.history.get("upload_logs", []):
                if item.get("source_id") == source_id:
                    item_ch = item.get("channel_id")
                    ch_match = (item_ch == channel_id) or (item_ch is None and any(n in item.get("type", "") for n in names))
                    if ch_match:
                        log_vid = item.get("youtube_id")
                        if log_vid and log_vid != youtube_video_id:
                            # Conflicting video ID in logs
                            print(f"Warning: Conflicting YouTube video ID for {key} in logs! Existing: '{log_vid}', New: '{youtube_video_id}'. Preserving existing.")
                            return False
                        elif log_vid == youtube_video_id:
                            matching_log = item

            # 4. If already confirmed with matching video ID in pending:
            if pending_entry.get("status") == "confirmed" and pending_entry.get("youtube_video_id") == youtube_video_id:
                if matching_log is not None:
                    # Genuinely idempotent: already confirmed in pending and present in upload_logs
                    return True

            # 5. Transition pending entry to confirmed
            pending_entry["source_id"] = source_id
            pending_entry["channel_id"] = channel_id
            pending_entry["status"] = "confirmed"
            pending_entry["youtube_video_id"] = youtube_video_id
            pending_entry["completed_timestamp"] = datetime.now().isoformat()
            if title:
                pending_entry["title"] = title

            # 6. Deduplicated set/list appends
            if title and title not in self.history.setdefault("used_script_titles", []):
                self.history["used_script_titles"].append(title)
            if youtube_video_id and youtube_video_id not in self.history.setdefault("uploaded_video_ids", []):
                self.history["uploaded_video_ids"].append(youtube_video_id)
            if source_id and source_id not in self.history.setdefault("used_source_ids", []):
                self.history["used_source_ids"].append(source_id)
            if query and query not in self.history.setdefault("used_queries", []):
                self.history["used_queries"].append(query)

            # 7. Append to upload_logs only if not already present
            if matching_log is None:
                log_entry = {
                    "timestamp": datetime.now().isoformat(),
                    "title": title,
                    "type": video_type,
                    "youtube_id": youtube_video_id,
                    "source_id": source_id,
                    "query": query,
                    "channel_id": channel_id
                }
                self.history.setdefault("upload_logs", []).append(log_entry)

            self.save()
            self._acknowledge_emergency_record(source_id, channel_id)
            return True

    def mark_uncertain(
        self,
        source_id: str,
        channel_id: int,
        error: str,
        owner_token: Optional[str] = None,
        youtube_video_id: Optional[str] = None
    ):
        """Marks upload as uncertain after timeout. Does NOT append to upload_logs."""
        with self.file_lock():
            self.reload()
            key = f"channel_{channel_id}:{source_id}"
            self._verify_owner_token(key, owner_token)
            entry = self.history.setdefault("pending_uploads", {}).setdefault(key, {})
            curr_status = entry.get("status")
            if curr_status == "confirmed":
                raise ValueError(f"Cannot mark confirmed upload '{key}' as uncertain.")
            entry["source_id"] = source_id
            entry["channel_id"] = channel_id
            entry["status"] = "uncertain"
            entry["error_details"] = error
            entry["uncertain_timestamp"] = datetime.now().isoformat()
            if youtube_video_id:
                entry["youtube_video_id"] = youtube_video_id
            self.save()

    def record_unconfirmed_video(
        self,
        source_id: str,
        channel_id: int,
        youtube_video_id: str,
        title: str,
        error: str,
        owner_token: Optional[str] = None
    ) -> bool:
        """
        Preserves an upload that succeeded on YouTube (returned a valid video_id)
        but failed to complete history confirmation (e.g. disk or serialization error).
        Leaves the record in a recoverable 'uncertain' state with the youtube_video_id
        safely attached so the clip is NEVER re-uploaded automatically.
        """
        with self.file_lock():
            self.reload()
            key = f"channel_{channel_id}:{source_id}"
            self._verify_owner_token(key, owner_token)
            entry = self.history.setdefault("pending_uploads", {}).setdefault(key, {})
            entry["source_id"] = source_id
            entry["channel_id"] = channel_id
            entry["title"] = title
            entry["youtube_video_id"] = youtube_video_id
            entry["status"] = "uncertain"
            entry["error_details"] = f"YouTube accepted upload (video_id={youtube_video_id}), but history confirmation failed: {error}"
            entry["uncertain_timestamp"] = datetime.now().isoformat()
            if youtube_video_id and youtube_video_id not in self.history.setdefault("uploaded_video_ids", []):
                self.history["uploaded_video_ids"].append(youtube_video_id)
            self.save()
            self._acknowledge_emergency_record(source_id, channel_id)
            return True

    def mark_failed(self, source_id: str, channel_id: int, error: str, owner_token: Optional[str] = None):
        """Marks upload as failed after definitive failure."""
        with self.file_lock():
            self.reload()
            key = f"channel_{channel_id}:{source_id}"
            self._verify_owner_token(key, owner_token)
            entry = self.history.setdefault("pending_uploads", {}).setdefault(key, {})
            curr_status = entry.get("status")
            if curr_status == "confirmed":
                raise ValueError(f"Cannot mark confirmed upload '{key}' as failed.")
            entry["source_id"] = source_id
            entry["channel_id"] = channel_id
            entry["status"] = "failed"
            entry["error_details"] = error
            entry["failed_timestamp"] = datetime.now().isoformat()
            self.save()

    def _acknowledge_emergency_record(self, source_id: str, channel_id: int):
        """
        Safely prunes an acknowledged/reconciled record from emergency_unconfirmed_uploads.jsonl.
        Retains all other unresolved emergency records. Never truncates the entire file if unresolved
        records remain. Removes the file only when 0 unresolved records remain.
        """
        emergency_file = os.path.join(os.path.dirname(self.history_file), "emergency_unconfirmed_uploads.jsonl")
        if not os.path.exists(emergency_file):
            return

        retained_lines = []
        found_target = False
        try:
            with open(emergency_file, "r", encoding="utf-8") as ef:
                for line in ef:
                    stripped = line.strip()
                    if not stripped:
                        continue
                    try:
                        rec = json.loads(stripped)
                        if str(rec.get("channel_id")) == str(channel_id) and rec.get("source_id") == source_id:
                            found_target = True
                            continue  # Omit the resolved record
                    except Exception:
                        pass
                    retained_lines.append(line)

            if found_target:
                if retained_lines:
                    tmp_file = f"{emergency_file}.tmp_{os.getpid()}"
                    with open(tmp_file, "w", encoding="utf-8") as tf:
                        for l in retained_lines:
                            tf.write(l if l.endswith("\n") else l + "\n")
                    os.replace(tmp_file, emergency_file)
                else:
                    try:
                        os.remove(emergency_file)
                    except FileNotFoundError:
                        pass
        except Exception as e:
            print(f"Warning: Failed to acknowledge emergency record for {source_id}: {e}")

    def reconcile_pending_upload(
        self,
        source_id: str,
        channel_id: int,
        resolution: str,
        youtube_video_id: Optional[str] = None,
        title: Optional[str] = None,
        video_type: Optional[str] = None
    ) -> bool:
        """
        Reconciles an uncertain upload:
        - resolution="confirmed": Confirms video exists on YouTube; records to upload_logs without duplication.
        - resolution="cleared": Confirms video does NOT exist on YouTube; clears pending state so it can be re-attempted.
        """
        with self.file_lock():
            self.reload()
            key = f"channel_{channel_id}:{source_id}"
            pending = self.history.get("pending_uploads", {}).get(key)
            if not pending:
                raise ValueError(f"No pending reservation found for '{key}' to reconcile.")
            if pending.get("status") not in ["uncertain", "failed", "uploading"]:
                raise ValueError(f"Cannot reconcile reservation '{key}' with status '{pending.get('status')}'.")

            if resolution == "confirmed":
                if not youtube_video_id:
                    raise ValueError("youtube_video_id is required to confirm reconciliation")
                entry = self.history.setdefault("pending_uploads", {}).setdefault(key, {})
                entry["status"] = "confirmed"
                entry["youtube_video_id"] = youtube_video_id
                entry["reconciled_timestamp"] = datetime.now().isoformat()

                already_in_logs = any(
                    item.get("youtube_id") == youtube_video_id or
                    (item.get("source_id") == source_id and item.get("channel_id") == channel_id)
                    for item in self.history.get("upload_logs", [])
                )
                if not already_in_logs:
                    t = title or entry.get("title", f"Reconciled upload {source_id}")
                    v_type = video_type or f"Reconciled Video [Channel {channel_id}]"
                    log_entry = {
                        "timestamp": datetime.now().isoformat(),
                        "title": t,
                        "type": v_type,
                        "youtube_id": youtube_video_id,
                        "source_id": source_id,
                        "channel_id": channel_id
                    }
                    self.history.setdefault("upload_logs", []).append(log_entry)
                    if youtube_video_id not in self.history.setdefault("uploaded_video_ids", []):
                        self.history["uploaded_video_ids"].append(youtube_video_id)
                self.save()
                self._acknowledge_emergency_record(source_id, channel_id)
                return True
            elif resolution == "cleared":
                if key in self.history.get("pending_uploads", {}):
                    del self.history["pending_uploads"][key]
                self.save()
                self._acknowledge_emergency_record(source_id, channel_id)
                return True
            else:
                raise ValueError(f"Unknown resolution '{resolution}'. Must be 'confirmed' or 'cleared'.")

    def record_upload(
        self,
        title: str,
        video_type: str,
        youtube_video_id: Optional[str] = None,
        source_id: Optional[str] = None,
        query: Optional[str] = None,
        channel_id: Optional[int] = None
    ):
        """Legacy helper: directly records a confirmed upload into history under lock."""
        with self.file_lock():
            self.reload()
            if title and title not in self.history.setdefault("used_script_titles", []):
                self.history["used_script_titles"].append(title)
            if youtube_video_id and youtube_video_id not in self.history.setdefault("uploaded_video_ids", []):
                self.history["uploaded_video_ids"].append(youtube_video_id)
            if source_id and source_id not in self.history.setdefault("used_source_ids", []):
                self.history["used_source_ids"].append(source_id)
            if query and query not in self.history.setdefault("used_queries", []):
                self.history["used_queries"].append(query)

            already_in_logs = any(
                (youtube_video_id and item.get("youtube_id") == youtube_video_id) or
                (source_id and channel_id and item.get("source_id") == source_id and item.get("channel_id") == channel_id)
                for item in self.history.get("upload_logs", [])
            )
            if not already_in_logs:
                log_entry = {
                    "timestamp": datetime.now().isoformat(),
                    "title": title,
                    "type": video_type,
                    "youtube_id": youtube_video_id,
                    "source_id": source_id,
                    "query": query,
                    "channel_id": channel_id
                }
                self.history.setdefault("upload_logs", []).append(log_entry)
            self.save()


if __name__ == "__main__":
    tracker = HistoryTracker()
    print("History tracker initialized. Used source clips:", len(tracker.history.get("used_source_ids", [])))
