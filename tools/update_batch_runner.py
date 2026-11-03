import re

with open("batch_runner.py", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Add import if not present
if "from channel_generator import generate_channel_batch" not in code:
    target = "from hoodie_presenter_engine import HoodiePresenterEngine"
    replacement = "from hoodie_presenter_engine import HoodiePresenterEngine\nfrom channel_generator import generate_channel_batch"
    if target in code:
        code = code.replace(target, replacement)
    else:
        print("Warning: target import not found directly.")

# 2. Replace generate_daily_10_batch
new_function = '''def generate_daily_10_batch(
    output_batch_dir: str = "output/batch_today",
    copy_to_desktop: bool = False,
    upload_yt: bool = False,
    upload_meta: bool = False,
    force: bool = False,
    target_channels: Optional[List[int]] = None
):
    print("=" * 65)
    print("🚀 GENERATING DAILY BATCH OF VIRAL HINDI SHORTS ACROSS CHANNELS")
    print("=" * 65)

    ensure_credentials()

    if upload_yt and check_already_uploaded_today(force=force):
        print("✅ Daily quota safe. Today's videos are already uploaded on schedule.")
        return

    os.makedirs(output_batch_dir, exist_ok=True)
    tracker = HistoryTracker()

    # Channel configuration mapping (Channel 3 -> Channel 1 -> Channel 2)
    channels = [
        {"id": 3, "name": "Channel 3 (Next Level Facts)", "token": "config/youtube_token_ch3.json"},
        {"id": 1, "name": "Channel 1 (MiniTalesWorld)", "token": "config/youtube_token.json"}
    ]
    if os.path.exists("config/youtube_token_ch2.json"):
        channels.append({"id": 2, "name": "Channel 2 (Pawsome Productions)", "token": "config/youtube_token_ch2.json"})

    if target_channels:
        channels = [c for c in channels if c["id"] in target_channels]

    print(f"\\n>> Active Channel Targets: {[c['name'] for c in channels]}")

    all_generated_videos: Dict[int, List[Dict[str, Any]]] = {}
    total_successful_uploads = 0

    for ch in channels:
        ch_id = ch["id"]
        ch_name = ch["name"]
        print("\\n" + "=" * 60)
        print(f"🎬 Processing Batch for {ch_name} (Channel {ch_id})")
        print("=" * 60)

        # 1. Generate 10 unique, channel-specific videos
        ch_videos = generate_channel_batch(ch_id, base_output_dir=output_batch_dir)
        all_generated_videos[ch_id] = ch_videos

        # 2. Copy to desktop if requested
        if copy_to_desktop:
            try:
                onedrive_desktop = os.path.join(os.environ.get("USERPROFILE", ""), "OneDrive", "Desktop")
                local_desktop = os.path.join(os.environ.get("USERPROFILE", ""), "Desktop")
                target_desktops = []
                if os.path.exists(onedrive_desktop):
                    target_desktops.append(onedrive_desktop)
                if os.path.exists(local_desktop) and local_desktop not in target_desktops:
                    target_desktops.append(local_desktop)

                for d_path in target_desktops:
                    ch_clean = re.sub(r'[^\\w\\-_]', '_', ch_name)
                    folder = os.path.join(d_path, "Daily_Shorts", ch_clean)
                    os.makedirs(folder, exist_ok=True)
                    for v in ch_videos:
                        dest = os.path.join(folder, os.path.basename(v["video_path"]))
                        shutil.copy2(v["video_path"], dest)
                        if v.get("thumbnail_path") and os.path.exists(v["thumbnail_path"]):
                            shutil.copy2(v["thumbnail_path"], os.path.join(folder, os.path.basename(v["thumbnail_path"])))
                    meta_dest = os.path.join(folder, "titles_and_tags.json")
                    with open(meta_dest, "w", encoding="utf-8") as f:
                        json.dump(ch_videos, f, ensure_ascii=False, indent=2)
                    print(f"📂 Copied {len(ch_videos)} videos to Desktop -> {folder}")
            except Exception as e:
                print(f"Desktop copy notice: {e}")

        # 3. Upload to YouTube if requested
        if upload_yt:
            print(f"\\n🚀 Auto-Uploading 10 Shorts to {ch_name} with Staggered Indian Peak Schedule...")
            uploader = YouTubeUploader(token_path=ch["token"])
            schedules = get_indian_peak_schedule(len(ch_videos), channel_id=ch_id)
            ch_success = 0

            for idx, v in enumerate(ch_videos):
                slot = schedules[idx]
                try:
                    upload_res = uploader.upload_short(
                        video_path=v["video_path"],
                        title=v["title"],
                        description=v["description"],
                        tags=v["tags"],
                        privacy_status="public",
                        publish_at=slot,
                        thumbnail_path=v.get("thumbnail_path")
                    )
                    ch_success += 1
                    total_successful_uploads += 1
                    tracker.record_upload(
                        title=v["title"],
                        video_type=f"{v['type']} [{ch_name}]",
                        youtube_video_id=upload_res.get("video_id"),
                        source_id=v.get("source_id"),
                        query=v.get("query")
                    )
                    time.sleep(4)
                except Exception as e:
                    print(f"[{ch_name}] Upload failed for '{v['title']}': {e}")
            print(f"✓ {ch_success} / {len(ch_videos)} videos successfully uploaded to {ch_name}!")

    if upload_yt and total_successful_uploads == 0:
        raise RuntimeError("All YouTube uploads across all channels failed.")

    print("\\n" + "=" * 65)
    print("🎉 ALL CHANNEL BATCHES PROCESSED SUCCESSFULLY!")
    print("=" * 65)
'''

# Find function start and main block
start_marker = "def generate_daily_10_batch("
main_marker = 'if __name__ == "__main__":'

idx_start = code.find(start_marker)
idx_end = code.find(main_marker)

if idx_start != -1 and idx_end != -1:
    code = code[:idx_start] + new_function + "\n\n" + code[idx_end:]
    with open("batch_runner.py", "w", encoding="utf-8") as f:
        f.write(code)
    print("✓ Successfully updated batch_runner.py!")
else:
    print(f"Error: Markers not found (start={idx_start}, end={idx_end})")
