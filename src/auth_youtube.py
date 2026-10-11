"""
Interactive YouTube OAuth Authorization Helper
Single-call flow to avoid state mismatch.
"""

import os
import sys

# Fix Windows console UTF-8 output
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
CLIENT_SECRETS = "config/client_secrets.json"
TOKEN_PATH = "config/youtube_token.json"

flow = InstalledAppFlow.from_client_secrets_file(
    CLIENT_SECRETS,
    scopes=SCOPES
)

print("Starting local OAuth server on port 8080...", flush=True)
print("A browser window will open automatically. Please click Allow.", flush=True)

# run_local_server opens browser automatically with matching state
creds = flow.run_local_server(host="localhost", port=8080, open_browser=True)

# Save token permanently
os.makedirs(os.path.dirname(TOKEN_PATH), exist_ok=True)
with open(TOKEN_PATH, "w", encoding="utf-8") as f:
    f.write(creds.to_json())

print("\n" + "=" * 65, flush=True)
print("🎉 SUCCESS: YouTube account connected permanently!", flush=True)
print(f"Token saved to: {TOKEN_PATH}", flush=True)
print("=" * 65, flush=True)
