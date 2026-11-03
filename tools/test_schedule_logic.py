import sys
from datetime import datetime, timedelta, timezone

ist = timezone(timedelta(hours=5, minutes=30))
now_ist = datetime.now(ist)
print(f"Current Time IST: {now_ist.strftime('%Y-%m-%d %H:%M:%S IST')}")

# Pre-defined channel schedules strictly fulfilling user's request:
# Channel 1: starts at 11:00 AM IST
# Channel 2: starts at 03:00 PM IST (15:00)
# Channel 3: starts at 08:00 PM IST (20:00)

CHANNEL_TARGET_HOURS = {
    1: [
        (11, 0),   # Slot 1: 11:00 AM (Morning kick-off)
        (11, 50),  # Slot 2: 11:50 AM
        (12, 40),  # Slot 3: 12:40 PM (Lunch peak)
        (13, 30),  # Slot 4: 01:30 PM
        (14, 20),  # Slot 5: 02:20 PM
        (15, 40),  # Slot 6: 03:40 PM
        (16, 30),  # Slot 7: 04:30 PM (Tea break)
        (17, 30),  # Slot 8: 05:30 PM (College/Office commute)
        (18, 30),  # Slot 9: 06:30 PM
        (19, 30),  # Slot 10: 07:30 PM (Evening transition)
    ],
    2: [
        (15, 0),   # Slot 1: 03:00 PM (Afternoon kick-off - exactly 3 PM)
        (15, 55),  # Slot 2: 03:55 PM
        (16, 50),  # Slot 3: 04:50 PM
        (17, 45),  # Slot 4: 05:45 PM
        (18, 40),  # Slot 5: 06:40 PM
        (19, 35),  # Slot 6: 07:35 PM
        (20, 30),  # Slot 7: 08:30 PM (Post-dinner leisure)
        (21, 20),  # Slot 8: 09:20 PM
        (22, 10),  # Slot 9: 10:10 PM (Bedtime scroll)
        (9, 15),   # Slot 10: Next Morning 09:15 AM
    ],
    3: [
        (20, 0),   # Slot 1: 08:00 PM (Super Prime Evening - exactly 8 PM)
        (20, 40),  # Slot 2: 08:40 PM
        (21, 15),  # Slot 3: 09:15 PM (Dinner peak)
        (21, 50),  # Slot 4: 09:50 PM
        (22, 25),  # Slot 5: 10:25 PM
        (23, 0),   # Slot 6: 11:00 PM (Late night viral scroll)
        (23, 35),  # Slot 7: 11:35 PM
        (7, 45),   # Slot 8: Next Morning 07:45 AM (Early morning wake-up)
        (8, 45),   # Slot 9: Next Morning 08:45 AM (Morning commute)
        (10, 0),   # Slot 10: Next Morning 10:00 AM (Tea break / pre-reset)
    ]
}

def get_channel_schedule(channel_id: int, count: int = 10, run_time_ist: datetime = None):
    if run_time_ist is None:
        run_time_ist = datetime.now(ist)

    hours_list = CHANNEL_TARGET_HOURS.get(channel_id, CHANNEL_TARGET_HOURS[1])
    slots = []
    last_dt = run_time_ist

    for idx in range(count):
        h, m = hours_list[idx % len(hours_list)]
        target_dt = run_time_ist.replace(hour=h, minute=m, second=0, microsecond=0)

        # If slot hour is in the morning for late night channels (e.g. Channel 2 slot 10 or Channel 3 slots 8-10)
        # OR if target time is earlier than the first slot of this channel, it belongs to tomorrow!
        anchor_h, anchor_m = hours_list[0]
        if h < anchor_h or (h == anchor_h and m < anchor_m):
            target_dt += timedelta(days=1)
        elif target_dt <= run_time_ist + timedelta(minutes=5):
            # If today's slot time already passed, shift to tomorrow
            target_dt += timedelta(days=1)

        # Ensure minimum 20 mins gap between consecutive videos on the same channel
        if target_dt <= last_dt:
            target_dt = last_dt + timedelta(minutes=25)

        last_dt = target_dt
        utc_str = target_dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
        slots.append({
            "slot": idx + 1,
            "ist": target_dt.strftime("%Y-%m-%d %I:%M %p IST"),
            "utc": utc_str
        })

    return slots

for ch in [1, 2, 3]:
    ch_names = {1: "Channel 1 (MiniTalesWorld - 11 AM Anchor)", 2: "Channel 2 (Pawsome - 3 PM Anchor)", 3: "Channel 3 (Next Level Facts - 8 PM Anchor)"}
    print(f"\n{'='*70}\n{ch_names[ch]}\n{'='*70}")
    # Simulate run at 10:45 AM IST
    sim_time = now_ist.replace(hour=10, minute=45, second=0, microsecond=0)
    res = get_channel_schedule(ch, count=10, run_time_ist=sim_time)
    for s in res:
        print(f"  Slot {s['slot']:02d}: {s['ist']} ({s['utc']})")
