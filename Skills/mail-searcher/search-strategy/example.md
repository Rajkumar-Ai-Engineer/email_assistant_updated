# Search Strategy Example

## Example 1: Finding a shared document link
**Request:** "Draft to Sneha needs to include the Q3 planning document link. Find it in the archive."

**Procedure:**
1. Fact needed: "Q3 planning document link".
2. Query: sender: "ananya" OR subject: "Q3 planning".
3. Archive search returns email a01 from Ananya with the link.

**Result:**
```json
{
  "fact_needed": "Q3 planning document link",
  "queries": ["sender: ananya", "subject: Q3 planning"],
  "results": [
    {
      "id": "a01",
      "snippet": "Q3 planning doc is here: https://docs.northwind-analytics.example/q3-planning"
    }
  ],
  "not_found": false
}
```

**Use in draft:** "Here is the Q3 planning doc: https://docs.northwind-analytics.example/q3-planning"

---

## Example 2: Finding an earlier commitment (no result)
**Request:** "Draft to Finance needs to reference the approved vendor cost. Search for the earlier vendor agreement."

**Procedure:**
1. Fact needed: "Vendor agreement and cost".
2. Query 1: sender: "vendor" subject: "agreement".
3. Query 2: subject: "cost" OR "pricing" AND vendor.
4. No results in archive.

**Result:**
```json
{
  "fact_needed": "Vendor agreement and approved cost",
  "queries": ["sender: vendor subject: agreement", "subject: cost pricing vendor"],
  "results": [],
  "not_found": true
}
```

**Use in draft:** Draft will use `[BLANK: vendor agreement cost]` placeholder.

---

## Example 3: Conflicting information in thread
**Request:** "Vendor demo time changed in the latest email. Confirm the new time and check for calendar conflict."

**Procedure:**
1. Fact needed: "Vendor demo meeting time and location".
2. Thread shows two different times:
   - Earlier message: "Wednesday 30 Sept at 14:00".
   - Latest message: "Thursday 1 Oct at 09:00".

**Result:**
```json
{
  "fact_needed": "Vendor demo meeting time",
  "queries": ["subject: vendor demo", "sender: karthik"],
  "results": [
    {
      "id": "email_thread_latest",
      "date": "2026-09-29",
      "snippet": "Vendor asked to move demo to Thursday 1 Oct at 09:00"
    },
    {
      "id": "email_thread_prior",
      "date": "2026-09-27",
      "snippet": "Vendor demo is Wednesday 30 Sept at 14:00"
    }
  ],
  "not_found": false,
  "note": "Two times in thread; latest (Thursday 09:00) supersedes earlier (Wednesday 14:00)"
}
```

**Use in draft:** Draft will reference the latest time and note the conflict with calendar.

---

## Example 4: Search with multiple relevant results
**Request:** "Find any earlier mentions of the data-labeling vendor project."

**Procedure:**
1. Fact needed: "Data-labeling vendor project history".
2. Query: subject: "data-labeling" OR "vendor".
3. Archive returns multiple messages from Karthik and Finance team over several days.
4. Prefer the most recent for the current status.

**Result:**
```json
{
  "fact_needed": "Data-labeling vendor project status and cost",
  "queries": ["subject: data-labeling", "sender: karthik OR meera"],
  "results": [
    {
      "id": "a10",
      "date": "2026-09-28",
      "snippet": "Vendor revised quote to INR 3.95 lakh for 6-month option"
    },
    {
      "id": "a09",
      "date": "2026-09-25",
      "snippet": "Initial quote INR 4.2 lakh for Q4; above limit without CFO approval"
    }
  ],
  "not_found": false,
  "note": "Use a10 (most recent) for current status; a09 shows history"
}
```

**Use in draft:** "Based on the latest vendor proposal, the 6-month option is INR 3.95 lakh."
