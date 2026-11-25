"""End-to-end 3-channel dry-run verification (1 video + 1 unique thumbnail per channel, NO YouTube upload)."""
import os
import sys

sys.path.insert(0, os.path.abspath("."))

from src.channel_generator import generate_channel_batch
from src.thumbnail_generator import hamming_distance


def main():
    out_dir = "output/test_3_channels_dryrun"
    dhashes = {}
    for ch_id in (1, 2, 3):
        res = generate_channel_batch(ch_id, base_output_dir=out_dir, force_render=True, target_count=1)
        assert len(res) == 1, f"Channel {ch_id} failed to produce 1 video!"
        item = res[0]
        assert os.path.exists(item["video_path"]) and os.path.getsize(item["video_path"]) > 200000, f"Ch{ch_id} video missing/small"
        assert os.path.exists(item["thumbnail_path"]) and os.path.getsize(item["thumbnail_path"]) > 10000, f"Ch{ch_id} thumb missing"
        dh = item.get("thumbnail_dhash", "")
        assert dh, f"Ch{ch_id} missing thumbnail dhash"
        for prev_ch, prev_dh in dhashes.items():
            dist = hamming_distance(dh, prev_dh)
            assert dist > 8, f"Thumbnail collision between Ch{ch_id} and Ch{prev_ch}: dist={dist}"
        dhashes[ch_id] = dh
        print(f"VERIFIED Ch{ch_id}: title={item['title']} | source={item['source_id']} | dHash={dh} | dur={item['duration']:.2f}s")

    print("\nALL 3 CHANNELS DRY-RUN PASSED WITH UNIQUE VIDEOS AND UNIQUE THUMBNAILS!")


if __name__ == "__main__":
    main()
