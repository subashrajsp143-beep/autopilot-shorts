import os
import sys
import json
import base64
import wsgiref.simple_server
from google_auth_oauthlib.flow import InstalledAppFlow, _RedirectWSGIApp, _ExclusiveWSGIServer, _WSGIRequestHandler

# Ensure unbuffered UTF-8 output
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)
        sys.stderr.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)
    except Exception:
        pass

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


def main():
    cs_path = "config/client_secrets.json"
    yt_path = "config/youtube_token.json"
    dat_path = "config/credentials.dat"
    url_file = "config/auth_url.txt"

    if not os.path.exists(cs_path):
        print(f"ERROR: {cs_path} not found!", flush=True)
        sys.exit(1)

    flow = InstalledAppFlow.from_client_secrets_file(cs_path, SCOPES)
    success_message = "MiniTalesWorld YouTube authentication successful! You can close this window now."
    wsgi_app = _RedirectWSGIApp(success_message)
    
    port = 8088
    local_server = wsgiref.simple_server.make_server(
        "localhost",
        port,
        wsgi_app,
        server_class=_ExclusiveWSGIServer,
        handler_class=_WSGIRequestHandler,
    )

    try:
        flow.redirect_uri = f"http://localhost:{port}/"
        auth_url, _ = flow.authorization_url(prompt="consent", access_type="offline")

        # Save URL to file so it's always accessible
        with open(url_file, "w", encoding="utf-8") as f:
            f.write(auth_url)

        print("\n" + "=" * 60, flush=True)
        print("🔑 AUTH_URL_READY", flush=True)
        print(auth_url, flush=True)
        print("=" * 60 + "\n", flush=True)

        # Try to open browser via Windows shell
        try:
            os.system(f'cmd.exe /c start "" "{auth_url}"')
        except Exception as e:
            print(f"Notice: Could not auto-launch browser: {e}", flush=True)

        print("Waiting for you to complete authorization in browser...", flush=True)
        local_server.handle_request()

        auth_response = wsgi_app.last_request_uri.replace("http", "https")
        flow.fetch_token(authorization_response=auth_response)
        creds = flow.credentials

        # Save locally
        with open(yt_path, "w", encoding="utf-8") as f:
            f.write(creds.to_json())
        print(f"✅ Successfully saved token to {yt_path}", flush=True)

        # Update credentials.dat
        if os.path.exists(dat_path):
            with open(dat_path, "r", encoding="utf-8") as f:
                encoded = f.read().strip()
            payload = json.loads(base64.b85decode(encoded.encode("utf-8")).decode("utf-8"))
        else:
            payload = {}

        with open(cs_path, "r", encoding="utf-8") as f:
            payload["client_secrets"] = f.read()

        payload["youtube_token"] = creds.to_json()

        new_encoded = base64.b85encode(json.dumps(payload).encode("utf-8")).decode("utf-8")
        with open(dat_path, "w", encoding="utf-8") as f:
            f.write(new_encoded)
        print(f"✅ Successfully updated {dat_path} bundle with fresh token!", flush=True)

        # Commit and push
        import subprocess
        subprocess.run(["git", "add", "config/credentials.dat"], check=False)
        subprocess.run(["git", "commit", "-m", "fix: refresh YouTube OAuth credentials token [skip ci]"], check=False)
        push_res = subprocess.run(
            ["git", "-c", "credential.helper=", "push", "origin", "main"],
            capture_output=True,
            text=True
        )
        if push_res.returncode == 0:
            print("✅ Successfully pushed updated credentials to GitHub main branch!", flush=True)
        else:
            print(f"Notice: git push output:\n{push_res.stdout}\n{push_res.stderr}", flush=True)

        print("\n🎉 Re-authentication finished completely!", flush=True)

    finally:
        local_server.server_close()
        if os.path.exists(url_file):
            try:
                os.remove(url_file)
            except Exception:
                pass


if __name__ == "__main__":
    main()
