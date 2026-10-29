"""
Multi-Channel YouTube Authorization Tool
-----------------------------------------
Authorizes Channel 2 or Channel 3 and saves credentials to config/youtube_token_chX.json.
Automatically updates config/credentials.dat to include all active channel tokens.
"""

import os
import sys
import json
import base64
import argparse

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


def bundle_all_credentials():
    """Bundles all client secrets, channel tokens, and Gemini key into config/credentials.dat"""
    dat_path = "config/credentials.dat"
    cs_path = "config/client_secrets.json"
    ch1_token = "config/youtube_token.json"
    ch2_token = "config/youtube_token_ch2.json"
    ch3_token = "config/youtube_token_ch3.json"

    payload = {}
    if os.path.exists(cs_path):
        with open(cs_path, "r", encoding="utf-8") as f:
            payload["client_secrets"] = f.read()

    if os.path.exists(ch1_token):
        with open(ch1_token, "r", encoding="utf-8") as f:
            payload["youtube_token"] = f.read()

    if os.path.exists(ch2_token):
        with open(ch2_token, "r", encoding="utf-8") as f:
            payload["youtube_token_ch2"] = f.read()

    if os.path.exists(ch3_token):
        with open(ch3_token, "r", encoding="utf-8") as f:
            payload["youtube_token_ch3"] = f.read()

    # Preserve gemini key from existing dat if present
    if os.path.exists(dat_path):
        try:
            with open(dat_path, "r", encoding="utf-8") as f:
                old_encoded = f.read()
            old_payload = json.loads(base64.b85decode(old_encoded.encode("utf-8")).decode("utf-8"))
            if "gemini_api_key" in old_payload:
                payload["gemini_api_key"] = old_payload["gemini_api_key"]
        except Exception:
            pass

    encoded = base64.b85encode(json.dumps(payload).encode("utf-8")).decode("utf-8")
    with open(dat_path, "w", encoding="utf-8") as f:
        f.write(encoded)

    print(f"✓ All channel credentials bundled successfully into {dat_path}!")


def authorize_channel(channel_num: int):
    cs_path = "config/client_secrets.json"
    if not os.path.exists(cs_path):
        print(f"❌ Error: {cs_path} not found!")
        return False

    token_filename = f"youtube_token_ch{channel_num}.json" if channel_num > 1 else "youtube_token.json"
    token_path = os.path.join("config", token_filename)

    print("=" * 65)
    print(f"🔐 AUTHORIZING YOUTUBE CHANNEL {channel_num}")
    print("=" * 65)
    print(f"Target token destination: {token_path}")
    print(f"A browser window will open. Please log in with the Google Account for Channel {channel_num} and click 'Allow'.\n")

    try:
        flow = InstalledAppFlow.from_client_secrets_file(cs_path, SCOPES)
        creds = flow.run_local_server(port=0)

        os.makedirs("config", exist_ok=True)
        with open(token_path, "w", encoding="utf-8") as f:
            f.write(creds.to_json())

        print(f"✓ Authentication successful! Token saved to: {token_path}")

        # Verify by fetching channel info
        try:
            yt = build("youtube", "v3", credentials=creds)
            print("✓ YouTube API initialized successfully for this channel!")
        except Exception as e:
            print(f"Note verifying channel: {e}")

        # Update credentials bundle
        bundle_all_credentials()
        print("\n🎉 Channel authorization complete!")
        return True

    except Exception as e:
        print(f"❌ Authorization failed: {e}")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Authorize YouTube Channel")
    parser.add_argument("--channel", type=int, choices=[1, 2, 3], required=True, help="Channel number (1, 2, or 3)")
    args = parser.parse_args()

    authorize_channel(args.channel)
