"""
YouTube Auto-Uploader Module
Uses official YouTube Data API v3 to upload Videos & Shorts automatically.
Features:
- Handles OAuth2 browser login once and persists session in token.json
- Automatically formats title & description for YouTube Shorts algorithm (#Shorts)
- Sets Category (Education / Entertainment), Tags, and Privacy status
- Sets High-Definition custom thumbnails via YouTube Data API
"""

import os
import sys
import json
from typing import Dict, Any, List, Optional

# Fix Windows console UTF-8 output
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


class YouTubeUploader:
    """Automates uploading shorts to YouTube channel."""

    def __init__(
        self,
        client_secrets_path: str = "config/client_secrets.json",
        token_path: str = "config/youtube_token.json"
    ):
        self.client_secrets_path = client_secrets_path
        self.token_path = token_path
        self.youtube = None

    def authenticate(self):
        """Authenticates with YouTube API. Prompts user in browser on first run."""
        creds = None
        if os.path.exists(self.token_path):
            try:
                creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)
            except Exception as e:
                print(f"Warning: Could not load token file: {e}")

        # If no valid credentials, run OAuth flow
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception:
                    creds = None

            if not creds:
                if not os.path.exists(self.client_secrets_path):
                    raise FileNotFoundError(
                        f"Missing client secrets file at '{self.client_secrets_path}'.\n"
                        "To get this file:\n"
                        "1. Go to Google Cloud Console (console.cloud.google.com)\n"
                        "2. Enable YouTube Data API v3\n"
                        "3. Create OAuth 2.0 Client ID (Desktop app) and download client_secret.json\n"
                        f"4. Save it to '{self.client_secrets_path}'"
                    )

                flow = InstalledAppFlow.from_client_secrets_file(self.client_secrets_path, SCOPES)
                creds = flow.run_local_server(port=0)

            # Save credentials for future silent runs
            os.makedirs(os.path.dirname(self.token_path), exist_ok=True)
            with open(self.token_path, "w", encoding="utf-8") as token_file:
                token_file.write(creds.to_json())

        self.youtube = build("youtube", "v3", credentials=creds)
        print("YouTube authentication successful!")

    def set_thumbnail(self, video_id: str, thumbnail_path: str) -> bool:
        """
        Uploads and sets a high-definition custom thumbnail for a YouTube video.
        """
        if not self.youtube:
            self.authenticate()

        if not thumbnail_path or not os.path.exists(thumbnail_path):
            print(f"Notice: Thumbnail file not found: {thumbnail_path}")
            return False

        try:
            print(f"🖼️ Setting custom HD thumbnail for video {video_id}...")
            thumb_media = MediaFileUpload(thumbnail_path, mimetype="image/jpeg")
            res = self.youtube.thumbnails().set(
                videoId=video_id,
                media_body=thumb_media
            ).execute()
            print(f"✓ Custom HD thumbnail set successfully for {video_id}!")
            return True
        except Exception as e:
            print(f"Notice: Could not set custom thumbnail for {video_id}: {e}")
            return False

    def upload_short(
        self,
        video_path: str,
        title: str,
        description: str,
        tags: Optional[List[str]] = None,
        privacy_status: str = "public",
        category_id: str = "27",  # 27 = Education, 24 = Entertainment
        publish_at: Optional[str] = None,
        thumbnail_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Uploads a video to YouTube as a Short.
        Supports scheduled publishing via publish_at (RFC 3339 formatted ISO UTC timestamp).
        Optionally sets a custom high-definition thumbnail.
        """
        if not self.youtube:
            self.authenticate()

        # Guarantee #Shorts tag in title and description
        if "#Shorts" not in title and "#shorts" not in title:
            title = f"{title} #Shorts"
        if "#Shorts" not in description:
            description = f"{description}\n\n#Shorts #viral #trending"

        tags = tags or ["shorts", "viral", "facts"]
        if "shorts" not in [t.lower() for t in tags]:
            tags.append("shorts")

        # Configure video status (Scheduled release vs Immediate Public)
        status_dict = {
            "selfDeclaredMadeForKids": False
        }
        if publish_at:
            status_dict["privacyStatus"] = "private"
            status_dict["publishAt"] = publish_at
            status_desc = f"Scheduled for {publish_at}"
        else:
            status_dict["privacyStatus"] = privacy_status
            status_desc = privacy_status

        body = {
            "snippet": {
                "title": title[:100],  # YouTube title limit 100 chars
                "description": description[:5000],
                "tags": tags,
                "categoryId": category_id
            },
            "status": status_dict
        }

        media = MediaFileUpload(
            video_path,
            mimetype="video/mp4",
            resumable=True,
            chunksize=1024 * 1024 * 5  # 5MB chunks
        )

        print(f"Uploading '{title}' to YouTube ({status_desc})...")
        request = self.youtube.videos().insert(
            part="snippet,status",
            body=body,
            media_body=media
        )

        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"Upload progress: {int(status.progress() * 100)}%")

        video_id = response.get("id")
        video_url = f"https://youtube.com/shorts/{video_id}"
        print(f"Upload complete! Watch live: {video_url}")

        if thumbnail_path:
            self.set_thumbnail(video_id, thumbnail_path)

        return {
            "platform": "YouTube",
            "video_id": video_id,
            "url": video_url,
            "status": "success"
        }


if __name__ == "__main__":
    uploader = YouTubeUploader()
    print("YouTube Uploader module initialized.")
