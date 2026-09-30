---
name: evidence-citation
description: Produces accurate evidence references for facts in summaries and drafts. Use to trace every factual claim back to its source and fill the evidence field.
---

# Evidence Citation

## When to use
- After drafting to validate that every fact has a source.
- To build the `evidence` list with email, archive, or calendar IDs.
- To blank or remove facts that lack a verifiable source.
- To ensure drafts are grounded in emails, archive, or calendar data only.

## Core rules
- Every fact in a summary or draft must come from an email, archive entry, or calendar event, and be cited with its ID.
- Facts without a source are dropped or replaced with `[BLANK: what is needed]`.
- The evidence list is minimal and exact; no assumptions or guesses.
- Acceptable sources: email ID, archive ID, calendar event ID.
- Unacceptable sources: memory, assumptions about the user, inferred context.

## Files
- `instructions.md`: read first; the procedure for matching facts to sources.
- `reference.md`: consult for ID formats, the fact-to-source mapping table, and what counts as evidence.
- `example.md`: open to see three examples mapping facts to IDs and one case where a fact becomes a blank.
