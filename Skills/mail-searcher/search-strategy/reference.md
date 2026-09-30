# Search Strategy Reference

## Query Patterns

| Need | Query form | Example |
|------|-----------|---------|
| Shared document link | sender + subject + timeframe | sender: "ananya" subject: "Q3 planning" within:month |
| Earlier commitment | sender + subject keyword | sender: "vendor" subject: "agreement" |
| Budget or approval status | sender (finance/manager) + subject | sender: "meera" OR sender: "finance" subject: "approved" |
| Vendor information | sender domain + subject | domain: "vendor.example" subject: "contract" |
| Customer communication | customer name + subject keyword | sender: "customer_name" subject: "issue" OR "ticket" |
| Scheduling history | subject keyword + date range | subject: "meeting" date:sep-2026 |
| Past decision or approval | sender + subject | sender: "manager" subject: "approved" OR "decision" |

## Result JSON Format

**On success:**
```json
{
  "fact_needed": "What was being searched for",
  "queries": ["query1", "query2", "query3"],
  "results": [
    {
      "id": "email_id_or_archive_id",
      "snippet": "Relevant text from the email (5-20 words)"
    },
    {
      "id": "email_id_or_archive_id_2",
      "snippet": "If multiple results, include all with dates"
    }
  ],
  "not_found": false
}
```

**On no results:**
```json
{
  "fact_needed": "What was being searched for",
  "queries": ["query1", "query2"],
  "results": [],
  "not_found": true
}
```

## Handling Multiple Matches

- If two emails match and both are relevant, return both.
- Mark the newer one first (most recent result preferred).
- If they contain conflicting information, note the dates so the draft-writer can surface the conflict to the user.
- Example:
  ```json
  {
    "results": [
      {
        "id": "a05",
        "date": "2026-09-28",
        "snippet": "New agreement effective October 1"
      },
      {
        "id": "a02",
        "date": "2026-09-15",
        "snippet": "Old agreement effective August 1 (superseded)"
      }
    ],
    "note": "Two results; a05 is most recent and supersedes a02"
  }
  ```

## Do Not Return
- Attachment binary data (return ID and snippet only).
- Full email bodies (summary as snippet).
- Sender passwords, credentials, or sensitive personal data (if found, flag separately).
- Results from private personal emails (if accessible by search, note that results are limited to professional context).
