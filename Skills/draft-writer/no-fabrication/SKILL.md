---
name: no-fabrication
description: Validates drafts to prevent invented facts and unauthorized commitments. Use to check that every claim is grounded in email, archive, or calendar data before saving.
---

# No Fabrication

## When to use
- Before saving a draft reply to the user.
- To audit every factual claim in the draft.
- To identify and blank or remove unsupported facts.
- To ensure the draft makes no commitments or decisions on the user's behalf.

## Core rules
- Every fact in a draft (date, amount, link, status, promise) must come from an email, archive, or calendar.
- If a fact has no source, drop it or replace with `[BLANK: what is needed]`.
- Never state the user's work status, approve decisions, or promise outcomes without explicit user input.
- Never describe product capabilities unless explicitly mentioned in an email.
- Never claim contract or legal commitments that the user cannot authorize.

## Files
- `instructions.md`: read first; the pre-save self-check procedure.
- `reference.md`: consult for the forbidden-claims table and the checklist.
- `example.md`: open to see before-and-after pairs of fabricated vs. corrected drafts.
