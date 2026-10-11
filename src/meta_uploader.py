"""
Meta Auto-Uploader Module (Instagram Reels & Facebook Page Reels)
Uses official Meta Graph API v21.0.

Features:
- Direct binary chunk upload for Facebook Page Reels (No public URL required)
- Instagram Reels container publishing
- Cross-posting integration (Posting to Facebook Page with IG cross-posting enabled)
"""

import os
import json
import time
import requests
from typing import Dict, Any, Optional


class MetaUploader:
    """Automates publishing Reels to Facebook Pages and Instagram Professional accounts."""

    def __init__(self, config_path: str = "config/meta_config.json"):
        self.config_path = config_path
        self.page_id = None
        self.ig_user_id = None
        self.access_token = None
        self.load_config()

    def load_config(self):
        """Loads Meta Graph API credentials if present."""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                    self.page_id = cfg.get("facebook_page_id")
                    self.ig_user_id = cfg.get("instagram_user_id")
                    self.access_token = cfg.get("page_access_token")
            except Exception as e:
                print(f"Warning: Could not read Meta config: {e}")

    def upload_facebook_reel(self, video_path: str, caption: str) -> Dict[str, Any]:
        """
        Uploads a vertical reel directly to Facebook Page using official 3-step Resumable Video API.
        Does not require a public video URL!
        """
        if not self.page_id or not self.access_token:
            raise ValueError(
                f"Missing Meta credentials in '{self.config_path}'.\n"
                "Please configure 'facebook_page_id' and 'page_access_token'."
            )

        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found at: {video_path}")

        file_size = os.path.getsize(video_path)
        base_url = "https://graph.facebook.com/v21.0"

        # Step 1: Initialize Reel upload session
        print("Step 1: Initializing Facebook Reel upload session...")
        start_url = f"{base_url}/{self.page_id}/video_reels"
        start_payload = {
            "upload_phase": "start",
            "access_token": self.access_token
        }
        resp = requests.post(start_url, data=start_payload)
        start_data = resp.json()

        if "video_id" not in start_data:
            raise RuntimeError(f"Facebook API Error on start: {start_data}")

        video_id = start_data["video_id"]
        upload_url = start_data["upload_url"]

        # Step 2: Upload raw video binary
        print(f"Step 2: Uploading video data ({file_size / (1024*1024):.2f} MB)...")
        headers = {
            "Authorization": f"OAuth {self.access_token}",
            "offset": "0",
            "file_size": str(file_size)
        }
        with open(video_path, "rb") as video_file:
            upload_resp = requests.post(upload_url, headers=headers, data=video_file)

        if upload_resp.status_code not in (200, 201):
            raise RuntimeError(f"Video binary upload failed: {upload_resp.text}")

        # Step 3: Finish and Publish
        print("Step 3: Publishing Reel on Facebook Page...")
        finish_url = f"{base_url}/{self.page_id}/video_reels"
        finish_payload = {
            "upload_phase": "finish",
            "access_token": self.access_token,
            "video_id": video_id,
            "video_state": "PUBLISHED",
            "description": caption
        }
        publish_resp = requests.post(finish_url, data=finish_payload)
        publish_data = publish_resp.json()

        if publish_data.get("success") is True:
            post_url = f"https://www.facebook.com/reel/{video_id}"
            print(f"Facebook Reel published successfully! URL: {post_url}")
            return {
                "platform": "Facebook Reels",
                "video_id": video_id,
                "url": post_url,
                "status": "success"
            }
        else:
            raise RuntimeError(f"Failed to publish Facebook Reel: {publish_data}")

    def upload_instagram_reel(self, video_url: str, caption: str) -> Dict[str, Any]:
        """
        Publishes a Reel to Instagram Business/Creator account via public URL container.
        """
        if not self.ig_user_id or not self.access_token:
            raise ValueError(f"Missing Instagram credentials in '{self.config_path}'.")

        base_url = "https://graph.facebook.com/v21.0"

        # Step 1: Create Container
        print("Step 1: Creating Instagram Reel container...")
        container_url = f"{base_url}/{self.ig_user_id}/media"
        payload = {
            "media_type": "REELS",
            "video_url": video_url,
            "caption": caption,
            "access_token": self.access_token
        }
        resp = requests.post(container_url, data=payload).json()
        if "id" not in resp:
            raise RuntimeError(f"Instagram Container creation failed: {resp}")

        creation_id = resp["id"]

        # Step 2: Poll container status until ready
        print("Step 2: Processing video on Instagram...")
        status_url = f"{base_url}/{creation_id}?fields=status_code&access_token={self.access_token}"
        for _ in range(30):
            status_resp = requests.get(status_url).json()
            code = status_resp.get("status_code")
            if code == "FINISHED":
                break
            elif code == "ERROR":
                raise RuntimeError("Instagram processing failed.")
            time.sleep(3)

        # Step 3: Publish container
        print("Step 3: Publishing Instagram Reel...")
        publish_url = f"{base_url}/{self.ig_user_id}/media_publish"
        pub_resp = requests.post(publish_url, data={"creation_id": creation_id, "access_token": self.access_token}).json()

        if "id" in pub_resp:
            print(f"Instagram Reel published! Media ID: {pub_resp['id']}")
            return {
                "platform": "Instagram Reels",
                "media_id": pub_resp["id"],
                "status": "success"
            }
        else:
            raise RuntimeError(f"Instagram publication failed: {pub_resp}")


if __name__ == "__main__":
    uploader = MetaUploader()
    print("Meta Uploader module initialized.")
