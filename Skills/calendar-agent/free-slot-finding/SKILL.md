---
name: free-slot-finding
description: Computes free time on the user's calendar and detects conflicts for scheduling requests. Use to find available slots within working hours and suggest times for meetings.
---

# Free Slot Finding

## When to use
- When an email requests scheduling (e.g., "Can we meet next Tuesday?").
- To find free windows in the user's calendar for meetings.
- To detect conflicts when a specific time is proposed.
- To suggest alternative times within working hours (Mon-Fri 09:00-17:00 IST).

## Core rules
- Use timezone Asia/Kolkata, working hours Mon-Fri 09:00-17:00.
- Exclude weekends and all-day closures (e.g., holidays).
- Default meeting length is 30 minutes unless otherwise specified.
- Return times in ISO 8601 format.
- Return up to three suggested slots.
- If a proposed time conflicts, report "conflict" without revealing event titles.

## Files
- `instructions.md`: read first; the slot-finding algorithm and handling of conflicts.
- `reference.md`: consult for working hours settings, output format, and common pitfalls.
- `example.md`: open to see examples with hypothetical calendars, conflicts, and edge cases.
