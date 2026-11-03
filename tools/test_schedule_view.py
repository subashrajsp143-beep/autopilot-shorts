import sys, os
sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath("src"))
from datetime import datetime, timezone, timedelta
from batch_runner import get_indian_peak_schedule

ist = timezone(timedelta(hours=5, minutes=30))

for ch, name in [(3, "Channel 3 (Next Level Facts)"), (1, "Channel 1 (MiniTalesWorld)"), (2, "Channel 2 (Pawsome Productions)")]:
    print(f"\n{'='*20} {name} {'='*20}")
    slots = get_indian_peak_schedule(10, channel_id=ch)
    for i, s in enumerate(slots, 1):
        if s is None:
            print(f"  Slot {i:02d}: LIVE IMMEDIATELY 🚀")
        else:
            dt = datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone(ist)
            print(f"  Slot {i:02d}: {dt.strftime('%I:%M %p IST')}")
