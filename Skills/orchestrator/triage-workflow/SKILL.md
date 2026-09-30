---
name: triage-workflow
description: End-to-end procedure for processing a batch of emails through classification, drafting, and validation. Use to manage the complete workflow from inbox to output records.
---

# Triage Workflow

## When to use
- Orchestrating a batch of new emails for triage.
- Delegating reading, classification, searching, calendar checks, and drafting to subagents.
- Assembling final records and validating them against the output schema.
- Setting a todo list with max 30 steps per batch and a 60-second budget per email.

## Core rules
- Never call tools directly; delegate all work to subagents.
- Read and classify every email first via `inbox-reader`.
- Skip drafting if the email is flagged `suspicious` or escalation rules forbid it.
- For scheduling requests, delegate to `calendar-agent` to find free slots.
- For missing facts, delegate to `mail-searcher` to find earlier emails or links.
- Retry once on malformed subagent responses, then flag for human review.
- Validate each record against the output schema and standing rules before returning.

## Files
- `instructions.md`: read first; the step-by-step per-email and per-batch procedure.
- `reference.md`: consult for the output schema, delegation templates, and operational limits.
- `example.md`: open when processing a batch to see how subagents are called in order.
