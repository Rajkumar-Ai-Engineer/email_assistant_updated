# Free Slot Finding Instructions

## Inputs
- A scheduling request with:
  - Preferred day, date, or timeframe (e.g., "next Tuesday", "Thursday afternoon", "this week").
  - Optional preferred time (e.g., "10:00", "14:00-15:00").
  - Optional meeting length (default: 30 minutes).
- The user's calendar: list of events with start/end times and timezone.
- Known holidays and all-day closures (e.g., Gandhi Jayanti).

## Algorithm

### Step 1: Resolve the date
- Convert the day/date request into a calendar date in IST.
- If "next week" is requested, search Mon-Fri of the following week.
- If "this week" is requested, search Mon-Fri of the current week.
- If a specific day (e.g., "Thursday") is requested, find the next occurrence of that day.

### Step 2: Exclude non-working time
- Remove weekends (Saturday, Sunday).
- Remove all-day closures and holidays from the calendar.
- Working hours are 09:00-17:00 (IST) on working days.

### Step 3: Find free windows
- For each working day in the range:
  - List all calendar events.
  - Find gaps between events (and between 09:00 and the first event, and between the last event and 17:00).
  - A gap is "free" if it is at least as long as the requested meeting.

### Step 4: Generate suggested slots
- Return up to three suggested free slots.
- Prefer times that align with common meeting patterns (09:00-10:00, 10:00-11:00, 14:00-15:00).
- If a preferred time was requested, check if it is free; if yes, include it first.

### Step 5: Handle conflicts
- If a specific time is proposed and it conflicts with a calendar event:
  - Set `conflicts: [{"proposed_time": "...", "conflict": true}]`.
  - Do NOT reveal the event title (privacy rule).
  - Example: "There is a conflict at that time."

### Step 6: Return
Output as JSON:
```json
{
  "requested_day": "Thursday",
  "working_day_found": true,
  "free_windows": [
    {"start": "2026-10-01T12:00:00+05:30", "end": "2026-10-01T13:00:00+05:30"},
    {"start": "2026-10-01T14:00:00+05:30", "end": "2026-10-01T17:00:00+05:30"}
  ],
  "suggested_slots": [
    {"start": "2026-10-01T12:00:00+05:30", "end": "2026-10-01T12:30:00+05:30"},
    {"start": "2026-10-01T14:00:00+05:30", "end": "2026-10-01T14:30:00+05:30"}
  ],
  "conflicts": []
}
```

If a proposed time conflicts:
```json
{
  "proposed_time": "2026-10-01T09:00:00+05:30",
  "conflicts": [
    {"start": "2026-10-01T09:00:00+05:30", "conflict": true, "note": "Another commitment at this time"}
  ]
}
```

## What to do if time cannot be found
- If the requested day is a weekend or holiday, say so: "That date is not a working day."
- If no free time exists on the requested day, offer to search other days: "Thursday is fully booked. Would Friday work?"
- If working hours do not apply (e.g., user has set custom hours), use those instead.

## Mistakes to avoid
- Do not confirm a meeting on the user's behalf; suggest times only.
- Do not reveal calendar event titles (privacy).
- Do not propose times outside working hours (09:00-17:00).
- Do not propose meeting times that exceed the length of free windows.
- Do not ignore holidays or all-day events.
