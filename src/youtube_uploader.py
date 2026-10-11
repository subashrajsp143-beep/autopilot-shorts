"""
YouTube Auto-Uploader Module
Uses official YouTube Data API v3 to upload Videos & Shorts automatically.
Features:
- Handles OAuth2 browser login once and persists session in token.json
- Automatically formats title & description for YouTube Shorts algorithm (#Shorts)
- Sets Category (Education / Entertainment), Tags, and Privacy status
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

    def upload_short(
        self,
        video_path: str,
        title: str,
        description: str,
        tags: Optional[List[str]] = None,
        privacy_status: str = "public",
        category_id: str = "27"  # 27 = Education, 24 = Entertainment
    ) -> Dict[str, Any]:
        """
        Uploads a video to YouTube as a Short.
        Ensures #Shorts is present in title and description.
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

        body = {
            "snippet": {
                "title": title[:100],  # YouTube title limit 100 chars
                "description": description[:5000],
                "tags": tags,
                "categoryId": category_id
            },
            "status": {
                "privacyStatus": privacy_status,
                "selfDeclaredMadeForKids": False
            }
        }

        media = MediaFileUpload(
            video_path,
            mimetype="video/mp4",
            resumable=True,
            chunksize=1024 * 1024 * 5  # 5MB chunks
        )

        print(f"Uploading '{title}' to YouTube ({privacy_status})...")
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

        return {
            "platform": "YouTube",
            "video_id": video_id,
            "url": video_url,
            "status": "success"
        }


if __name__ == "__main__":
    uploader = YouTubeUploader()
    print("YouTube Uploader module initialized.")
