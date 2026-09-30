# Evidence Citation Instructions

## Inputs
- A summary or draft containing facts.
- The sources from which facts were drawn: email IDs, archive IDs, calendar event IDs, or search results.

## Citation procedure

### Step 1: List the facts
- Identify every factual claim in the summary or draft.
- Facts include: names, dates, amounts, links, decisions, status, events, times.
- Exclude: descriptions of tone, phrasing, logical inference.

Examples of facts:
- "Customer reported duplicate charge of INR 2,75,000."
- "Meeting on Thursday 1 Oct at 09:00."
- "Q3 planning document link is https://docs.northwind-analytics.example/q3-planning."

### Step 2: Match each fact to a source
- For each fact, identify where it came from:
  - An email (use email ID: `email:<id>`).
  - An archived email (use archive ID: `archive:<id>`).
  - A calendar event (use calendar ID: `calendar:<id>`).
  - A search result (use the original email or archive ID).

### Step 3: Check fact-to-source validity
- Use the mapping table in reference.md to ensure the fact type is acceptable for the source.
- Example: a date can come from email or calendar; a customer name should come from email.

### Step 4: Drop or blank facts without a source
- If a fact has no source, remove it from the draft or replace it with `[BLANK: description]`.
- Examples:
  - Original: "I will contact Finance and resolve this by Friday."
  - Corrected: "I am escalating this to Finance. [BLANK: resolution timeline pending your approval]."

### Step 5: Build the evidence list
- List all source IDs in the format: `email:<id>`, `archive:<id>`, `calendar:<id>`.
- Remove duplicates.
- Order by type (emails first, then archive, then calendar), then by ID.

### Step 6: Return
Output as JSON:
```json
{
  "fact_checked": true,
  "evidence": ["email:e02", "archive:a01", "calendar:c05"],
  "blanks_introduced": []
}
```

If blanks were introduced:
```json
{
  "fact_checked": true,
  "evidence": ["email:e09"],
  "blanks_introduced": [
    {
      "placeholder": "[BLANK: deck status]",
      "reason": "No information available about whether Q3 metrics deck is ready"
    }
  ]
}
```

## What to do if a fact has no source
- Do not guess or invent.
- Replace with `[BLANK: description of what is needed]`.
- Note it in `blanks_introduced`.
- The draft-writer will use this to prompt the user to fill in the blank before sending.

## Mistakes to avoid
- Do not include facts without sources in the final evidence list.
- Do not assume facts are "common knowledge" (they still need a source).
- Do not cite the user's prior work or status as a source (no "the user already knows this").
- Do not cite assumptions (e.g., "the budget was probably approved" - no source, no fact).
