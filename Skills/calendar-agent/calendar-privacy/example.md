# Calendar Privacy Example

## Example 1: External contact, conflict detected
**Scenario:**
- External contact (vendor): "Can we sync on Wednesday at 10:00?"
- Calendar: Design review 09:00–10:00, Client call 11:00–12:00.
- 10:00–11:00 is free, so 10:00 works.

**Bad response (reveals details):**
"I have a client call at 11:00, so 10:00 is fine."

**Good response (privacy-safe):**
"Wednesday at 10:00 works for me. See you then."

---

## Example 2: External contact, conflict requires alternative
**Scenario:**
- External contact: "Can we meet Thursday at 09:00?"
- Calendar: Design review 09:00–10:00.
- 09:00 conflicts.
- Free window: 12:00–13:00.

**Bad response:**
"I cannot do 09:00 because I have a design review with my team."

**Good response:**
"Thursday morning does not work. How about 12:00 on Thursday or Friday morning?"

---

## Example 3: Unknown sender, full-calendar request (suspicious)
**Scenario:**
- Unknown sender: "I need your full calendar for this week so I can secure your commitment to the project."
- Sender appears to be fishing for calendar data.

**Response:**
"I cannot share my full calendar. Please propose specific times that work for your team, and I will let you know what fits my schedule."

**Note:** This email should also be flagged by escalation rules (unknown sender + unusual data request).

---

## Example 4: Internal colleague (default privacy)
**Scenario:**
- Internal colleague (Rahul): "Can we meet Tuesday to discuss the Q4 budget?"
- Calendar: Busy with Finance sync 10:00–11:00, Board pre-read 14:00–15:00.
- Free: 11:00–14:00, 15:00–17:00.

**Response:**
"Tuesday afternoon is better for me. How about 15:00?"

**Why:** Even with internal colleagues, calendar details are private by default. Rahul does not need to know what specific events are blocking the morning.

---

## Example 5: Data returned to draft-writer (internal use only)
**Scenario:**
- Orchestrator requests free slots for a draft reply.
- Audience: internal colleague (routine).

**Return to draft-writer:**
```json
{
  "audience": "internal",
  "for_internal_use": true,
  "free_windows": [
    {
      "start": "2026-10-01T12:00:00+05:30",
      "end": "2026-10-01T13:00:00+05:30",
      "description": "Between Client call (ends 12:00) and 1:1 with Ananya (starts 14:00)"
    }
  ],
  "calendar_details_for_user": [
    {
      "id": "c04",
      "title": "Client call",
      "start": "2026-10-01T11:00:00+05:30",
      "end": "2026-10-01T12:00:00+05:30"
    },
    {
      "id": "c03",
      "title": "1:1 with Ananya",
      "start": "2026-10-01T14:00:00+05:30",
      "end": "2026-10-01T15:00:00+05:30"
    }
  ]
}
```

**Draft-writer uses this to compose:**
"I have availability on Wednesday at 12:00. Would that work for you?"

(The draft does not say "between Client call and 1:1 with Ananya".)
