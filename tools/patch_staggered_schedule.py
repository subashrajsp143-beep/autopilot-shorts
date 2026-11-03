import os

p = r"C:\Users\Subhash Kumar\.gemini\antigravity\scratch\autopilot_shorts\batch_runner.py"
with open(p, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update get_indian_peak_schedule definition
old_def = """def get_indian_peak_schedule(num_videos: int = 10):
    \"\"\"
    Calculates 10 publishing slots strictly aligned to Indian Peak Viewing Hours (11 AM - 10:30 PM IST).
    Guarantees videos are strictly chronological, never out of order, and NEVER posted in the middle of the night!
    \"\"\"
    from datetime import datetime, timedelta, timezone
    ist = timezone(timedelta(hours=5, minutes=30))
    now_ist = datetime.now(ist)

    # 10 Peak Indian audience slots
    target_hours_ist = [
        (11, 15),  # Slot 1: Morning wake-up / tea break
        (12, 30),  # Slot 2: Lunch / College break
        (13, 45),  # Slot 3: Afternoon scroll
        (15, 0),   # Slot 4: Mid-afternoon
        (16, 15),  # Slot 5: Evening tea break
        (17, 30),  # Slot 6: Commute / Free time
        (18, 45),  # Slot 7: Early evening peak
        (20, 0),   # Slot 8: PRIME EVENING SUPER PEAK (8 PM)
        (21, 0),   # Slot 9: PRIME DINNER SUPER PEAK (9 PM)
        (22, 0)    # Slot 10: LATE NIGHT SCROLLING PEAK (10 PM)
    ]

    slots = []
    last_slot_ist = now_ist
    for i in range(num_videos):
        if i == 0:
            slots.append(None)  # First video goes live immediately!
            continue

        idx = min(i, len(target_hours_ist) - 1)
        h, m = target_hours_ist[idx]
        slot_ist = now_ist.replace(hour=h, minute=m, second=0, microsecond=0)

        # If target slot is in past or too close to previous slot, push forward by at least 28 minutes
        min_allowed = last_slot_ist + timedelta(minutes=28)
        if slot_ist < min_allowed:
            slot_ist = min_allowed

        # If pushed beyond 10:45 PM IST, schedule remaining for tomorrow morning starting at 11:15 AM
        if slot_ist.hour >= 23 or (slot_ist.hour < 10 and slot_ist.day == now_ist.day):
            tomorrow_ist = (now_ist + timedelta(days=1)).replace(hour=11, minute=15, second=0, microsecond=0)
            if min_allowed < tomorrow_ist:
                slot_ist = tomorrow_ist + timedelta(minutes=45 * (i - 1))
            else:
                slot_ist = min_allowed

        last_slot_ist = slot_ist
        slot_utc = slot_ist.astimezone(timezone.utc)
        slots.append(slot_utc.strftime("%Y-%m-%dT%H:%M:%S.000Z"))

    return slots"""

new_def = """def get_indian_peak_schedule(num_videos: int = 10, channel_id: int = 1):
    \"\"\"
    Calculates 10 publishing slots strictly aligned to Indian Peak Viewing Hours (11 AM - 10:30 PM IST).
    Staggers upload slots across different channels so they NEVER publish at the same time:
    - Channel 3 (Next Level Facts): Offset 0 mins (Star channel gets top priority on the hour :00/:30)
    - Channel 1 (MiniTalesWorld): Offset +20 mins (Publishes at :20/:50)
    - Channel 2 (Pawsome Productions): Offset +40 mins (Publishes at :10/:40)
    \"\"\"
    from datetime import datetime, timedelta, timezone
    ist = timezone(timedelta(hours=5, minutes=30))
    now_ist = datetime.now(ist)

    # Channel-specific time offsets to completely eliminate cross-channel upload clashes
    channel_offsets = {
        3: 0,   # Channel 3 gets priority (:00 / :30)
        1: 20,  # Channel 1 publishes at :20 / :50
        2: 40   # Channel 2 publishes at :10 / :40
    }
    ch_offset_mins = channel_offsets.get(channel_id, (channel_id - 1) * 20)

    target_hours_ist = [
        (11, 15),  # Slot 1: Morning wake-up / tea break
        (12, 30),  # Slot 2: Lunch / College break
        (13, 45),  # Slot 3: Afternoon scroll
        (15, 0),   # Slot 4: Mid-afternoon
        (16, 15),  # Slot 5: Evening tea break
        (17, 30),  # Slot 6: Commute / Free time
        (18, 45),  # Slot 7: Early evening peak
        (20, 0),   # Slot 8: PRIME EVENING SUPER PEAK (8 PM)
        (21, 0),   # Slot 9: PRIME DINNER SUPER PEAK (9 PM)
        (22, 0)    # Slot 10: LATE NIGHT SCROLLING PEAK (10 PM)
    ]

    slots = []
    last_slot_ist = now_ist
    for i in range(num_videos):
        if i == 0:
            if channel_id == 3:
                slots.append(None)  # Channel 3 first video goes live immediately!
            else:
                first_slot = now_ist + timedelta(minutes=ch_offset_mins)
                slots.append(first_slot.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z"))
            continue

        idx = min(i, len(target_hours_ist) - 1)
        h, m = target_hours_ist[idx]
        slot_ist = now_ist.replace(hour=h, minute=m, second=0, microsecond=0) + timedelta(minutes=ch_offset_mins)

        # Minimum spacing between videos on the same channel
        min_allowed = last_slot_ist + timedelta(minutes=25)
        if slot_ist < min_allowed:
            slot_ist = min_allowed

        # If pushed beyond 11:30 PM IST, schedule for tomorrow morning
        if slot_ist.hour >= 23 and slot_ist.minute > 30:
            tomorrow_ist = (now_ist + timedelta(days=1)).replace(hour=11, minute=15, second=0, microsecond=0) + timedelta(minutes=ch_offset_mins)
            if min_allowed < tomorrow_ist:
                slot_ist = tomorrow_ist + timedelta(minutes=45 * (i - 1))
            else:
                slot_ist = min_allowed

        last_slot_ist = slot_ist
        slot_utc = slot_ist.astimezone(timezone.utc)
        slots.append(slot_utc.strftime("%Y-%m-%dT%H:%M:%S.000Z"))

    return slots"""

if "\r\n" in content:
    old_def = old_def.replace("\n", "\r\n")
    new_def = new_def.replace("\n", "\r\n")

if old_def in content:
    content = content.replace(old_def, new_def, 1)
    print("Replaced get_indian_peak_schedule definition successfully.")
else:
    print("Warning: old_def not found directly, checking normalized...")

# 2. Update caller to pass channel_id
old_call = "schedules = get_indian_peak_schedule(len(generated_videos))"
new_call = "schedules = get_indian_peak_schedule(len(generated_videos), channel_id=ch['id'])"
if old_call in content:
    content = content.replace(old_call, new_call)
    print("Updated caller to pass channel_id=ch['id'].")

with open(p, "w", encoding="utf-8") as f:
    f.write(content)

print("Patch complete.")
