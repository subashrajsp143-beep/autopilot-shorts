# 🚀 Autopilot Faceless Video Machine

An end-to-end automated pipeline that generates viral **YouTube Shorts, Instagram Reels, and Facebook Reels** and uploads them automatically on autopilot.

---

## 📁 Project Structure

```
autopilot_shorts/
├── assets/
│   ├── backgrounds/     <- Drop your background video loops here (.mp4)
│   └── music/           <- Drop ambient background music here (.mp3)
├── config/
│   ├── client_secrets.json    <- Google Cloud OAuth client credentials (for YouTube)
│   ├── youtube_token.json     <- Saved token (auto-generated on 1st login)
│   └── meta_config.json       <- Facebook & Instagram API tokens
├── output/              <- Generated videos (.mp4), voiceovers (.mp3), subtitles (.ass)
├── src/
│   ├── script_generator.py    <- Viral hooks and storytelling scripts
│   ├── voice_generator.py     <- Ultra-realistic neural voiceover (Edge-TTS) + ASS subtitles
│   ├── video_maker.py         <- 1080x1920 9:16 FFmpeg video compositor
│   ├── youtube_uploader.py    <- Official YouTube Data API v3 uploader
│   └── meta_uploader.py       <- Official Meta Graph API Reels uploader
└── main.py              <- Main orchestrator & Scheduler
```

---

## ⚡ Quick Start: Generate A Video in 10 Seconds

To generate a ready-to-upload video immediately:

```bash
python main.py
```

Generated video will be saved in `output/` at **1080x1920 (9:16 vertical)** with:
- Natural neural narrator voice
- Bold, high-retention animated subtitles (yellow with black outline)

### Generate by Niche:
```bash
python main.py --niche psychology
python main.py --niche history
python main.py --niche science
python main.py --niche money
```

### Generate for a Custom Topic:
```bash
python main.py --topic "Artificial Intelligence in 2030"
```

---

## 📤 1. YouTube Shorts Auto-Upload Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Create a project and enable **YouTube Data API v3**.
3. Under **Credentials**, create an **OAuth 2.0 Client ID** (Application type: *Desktop app*).
4. Download the JSON file and save it as:
   `config/client_secrets.json`
5. Run the upload command:
   ```bash
   python main.py --upload-yt
   ```
6. On the first run, a browser window will open asking you to sign into your YouTube account. Once you click "Allow", your login is saved in `config/youtube_token.json`. **From that moment on, uploads happen silently in the background!**

---

## 📤 2. Facebook & Instagram Reels Auto-Upload Setup

1. Copy `config/meta_config.example.json` to `config/meta_config.json`.
2. Enter your:
   - `facebook_page_id`: Found on your Facebook Page > About.
   - `page_access_token`: Generated via [Meta for Developers](https://developers.facebook.com/) > Graph API Explorer with permissions `pages_manage_posts`, `pages_read_engagement`, `instagram_content_publish`.
3. In Facebook Page settings, turn ON **"Share Reels to Instagram"**. This automatically publishes your Reel to your Instagram account simultaneously!
4. Run:
   ```bash
   python main.py --upload-meta
   ```

---

## 🤖 3. Full 24/7 Autopilot Mode

To have your system automatically create and upload 1 video every day (e.g., every 24 hours):

```bash
python main.py --schedule 24 --upload-all
```

---

## 🎨 Pro Tips for Viral Views:
- **Add Background Footage:** Download free vertical footage from [Pexels](https://www.pexels.com/video/) (e.g. Minecraft parkour, subway surfers, GTA driving, space/galaxy drones) and drop them into `assets/backgrounds/`. The system will automatically crop, scale, and loop them!
- **Target US/Global Audiences:** Use the default English voice (`en-US-ChristopherNeural`). Global CPM is 10x higher than Indian CPM, earning you ₹1,500–₹2,500 with just 5,000–10,000 views!
