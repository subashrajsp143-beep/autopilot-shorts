import sys
sys.path.insert(0, ".")
from src.channel_blueprints import get_channel_blueprints

bps = get_channel_blueprints(3, count=10)
for b in bps:
    print(f"Slot {b['slot']}: [{b.get('engine', 'action')}] {b['title'][:40]} | Banner: {b['banner']}")
