# Free Slot Finding Example

## Example calendar (all examples use this)

**Today: 2026-09-29 (Monday), Current time: 09:00 IST**

**Calendar:**
- Monday 29 Sept: Team sync 15:00–16:00
- Tuesday 30 Sept: Sprint planning 10:00–11:00, 1:1 with manager 14:00–15:00
- Wednesday 1 Oct: Design review 09:00–10:00, Client call 11:00–12:00
- Thursday 2 Oct: Gandhi Jayanti (all-day closure)
- Friday 3 Oct: No events

---

## Example 1: Request for "next Thursday"
**Request:** "Can we sync on Thursday afternoon?"

**Procedure:**
- Today is Monday 29 Sept.
- Next Thursday = 2 Oct (but it is Gandhi Jayanti, all-day closure).
- No working time available.

**Output:**
```json
{
  "requested_timeframe": "Thursday afternoon",
  "working_day_found": false,
  "free_windows": [],
  "suggested_slots": [],
  "note": "Thursday 2 Oct is a holiday (Gandhi Jayanti). No working hours available. Friday 3 Oct has full availability: 09:00–17:00."
}
```

---

## Example 2: Request with proposed time (conflict detected)
**Request:** "Can we meet Wednesday at 10:00?"

**Procedure:**
- Requested day: Wednesday 1 Oct.
- Proposed time: 10:00–10:30.
- Calendar: Design review 09:00–10:00, Client call 11:00–12:00.
- 10:00–10:30 overlaps with Client call (11:00–12:00)? No, it ends at 10:30, call starts at 11:00.
- Actually, 10:00–10:30 is free (between Design review and Client call).

Wait, let me re-read: Design review ends at 10:00, Client call starts at 11:00. So 10:00–11:00 is free. 10:00–10:30 is within that free window.

Let me reconsider the example. Let me say the request is for 10:00–11:00 (1 hour) instead.

**Revised Request:** "Can we meet Wednesday at 10:00 for an hour?"

**Procedure:**
- Requested day: Wednesday 1 Oct.
- Proposed time: 10:00–11:00.
- Calendar: Design review 09:00–10:00, Client call 11:00–12:00.
- 10:00–11:00 overlaps with Client call (11:00–12:00) at 11:00.
- Conflict found.

**Output:**
```json
{
  "proposed_time": "2026-10-01T10:00:00+05:30",
  "proposed_duration": "PT1H",
  "conflicts": [
    {
      "start": "2026-10-01T11:00:00+05:30",
      "end": "2026-10-01T12:00:00+05:30",
      "conflict": true,
      "note": "Another commitment conflicts at this time"
    }
  ],
  "alternative_suggestion": "Wednesday has free time at 12:00–14:00."
}
```

---

## Example 3: Request for Friday (fully available)
**Request:** "Is Friday completely free?"

**Procedure:**
- Requested day: Friday 3 Oct.
- Calendar: No events.
- Free windows: 09:00–17:00.
- Suggest three 30-minute slots.

**Output:**
```json
{
  "requested_timeframe": "Friday 3 Oct",
  "working_day_found": true,
  "free_windows": [
    {
      "start": "2026-10-03T09:00:00+05:30",
      "end": "2026-10-03T17:00:00+05:30"
    }
  ],
  "suggested_slots": [
    {
      "start": "2026-10-03T09:00:00+05:30",
      "end": "2026-10-03T09:30:00+05:30"
    },
    {
      "start": "2026-10-03T14:00:00+05:30",
      "end": "2026-10-03T14:30:00+05:30"
    },
    {
      "start": "2026-10-03T15:30:00+05:30",
      "end": "2026-10-03T16:00:00+05:30"
    }
  ],
  "conflicts": []
}
```

---

## Example 4: Request outside working hours
**Request:** "Can we meet Wednesday at 08:00?"

**Procedure:**
- Requested day: Wednesday 1 Oct.
- Proposed time: 08:00 (outside working hours 09:00–17:00).
- No free slot at requested time.

**Output:**
```json
{
  "proposed_time": "2026-10-01T08:00:00+05:30",
  "conflicts": [],
  "note": "08:00 is outside working hours (09:00–17:00 IST). Earliest available time on Wednesday is 10:00."
}
```
