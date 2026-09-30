# Free Slot Finding Reference

## Working Hours Settings

| Setting | Value |
|---------|-------|
| Timezone | Asia/Kolkata (IST, UTC+05:30) |
| Working days | Monday–Friday |
| Working hours | 09:00–17:00 IST |
| Default meeting length | 30 minutes |
| Holidays (sample) | Gandhi Jayanti (2 Oct), Diwali (varies), office closures |

## Output JSON Format

**On success:**
```json
{
  "requested_timeframe": "Thursday afternoon",
  "working_day_found": true,
  "free_windows": [
    {
      "start": "2026-10-01T13:00:00+05:30",
      "end": "2026-10-01T17:00:00+05:30"
    }
  ],
  "suggested_slots": [
    {
      "start": "2026-10-01T13:00:00+05:30",
      "end": "2026-10-01T13:30:00+05:30"
    },
    {
      "start": "2026-10-01T14:00:00+05:30",
      "end": "2026-10-01T14:30:00+05:30"
    }
  ],
  "conflicts": []
}
```

**On conflict:**
```json
{
  "proposed_time": "2026-10-01T09:00:00+05:30",
  "proposed_duration": "PT30M",
  "conflicts": [
    {
      "start": "2026-10-01T09:00:00+05:30",
      "end": "2026-10-01T10:00:00+05:30",
      "conflict": true,
      "note": "Another commitment at this time (event title hidden)"
    }
  ]
}
```

**On no availability:**
```json
{
  "requested_timeframe": "Thursday",
  "working_day_found": true,
  "free_windows": [],
  "suggested_slots": [],
  "note": "No free time available on Thursday. Friday has slots at 14:00–15:00."
}
```

## Algorithm Steps (Detailed)

1. **Parse request:**
   - Extract day of week, date, or timeframe.
   - Extract any proposed time (e.g., "10:00").
   - Extract meeting length (default 30 min).

2. **Resolve to calendar date:**
   - Convert "Thursday" → next Thursday's date (e.g., 2026-10-01).
   - Convert "this week" → Monday–Friday of current week.
   - Convert "next week" → Monday–Friday of following week.

3. **Load calendar:**
   - Get all events for the date range.
   - Remove all-day events separately; they block the whole day.

4. **Compute free windows:**
   - For each working day:
     - List events in chronological order.
     - Gap from 09:00 to first event (if > meeting length).
     - Gap between consecutive events (if > meeting length).
     - Gap from last event to 17:00 (if > meeting length).

5. **Suggest slots:**
   - Pick up to 3 slots from free windows.
   - Prefer times that start at whole or half hours (09:00, 14:30, etc.).
   - If proposed time is free, include it first.

6. **Check for conflicts:**
   - If a specific time is proposed, compare against all events.
   - If overlap found, set `conflict=true` and note (no title).

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| All-day event incorrectly handled | Treat all-day as blocking 09:00-17:00 |
| Back-to-back meetings with no gap | No free slot; report empty suggestions |
| Holiday not excluded | Explicitly list holidays in calendar input |
| Time zone mismatch | Always work in IST (Asia/Kolkata, UTC+05:30) |
| Request outside working hours (e.g., "8am") | Note that this is outside working hours; offer alternatives |
| Meeting length longer than free window | Do not suggest the slot; report "no available window" |
| "This afternoon" without knowing current time | Ask for clarification or assume current time is before 12:00 IST |
