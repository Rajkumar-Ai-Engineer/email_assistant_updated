# Triage Workflow Instructions

## Inputs
- A batch of emails, each with `id`, `from`, `subject`, `body`, `date`, and optional `thread_history`.
- A list of no more than 30 emails per batch.
- The system's operation budget: 60 seconds per email, total time per batch governed by the batch size.

## Batch setup
1. Create a todo list with one entry per email.
2. Set a step counter (max 30 per batch) and a timer (60 seconds per email).
3. Log the batch size and start time.

## Per-email procedure
For each email in the todo list:

1. **Delegate to inbox-reader for classification**
   - Send the email and thread history to the `email-classification` skill.
   - Receive back: `category`, `summary`, `needs_reply`, and other flags.

2. **Delegate to injection-detection**
   - Send the same email to the `injection-detection` skill.
   - Receive back: updated `suspicious` flag and `review_reason` if triggered.

3. **Check escalation rules**
   - Use the `escalation-rules` skill to decide if the email needs human review.
   - Receive back: confirmed `needs_human_review` flag, `review_reason`, and whether drafting is allowed.

4. **Delegate drafting only if allowed**
   - If `suspicious` is true or escalation rules forbid drafting, skip to validation.
   - If drafting is allowed and `needs_reply` is true:
     - If the email mentions a scheduling request (e.g., "when are you free?"), delegate to `calendar-agent`.
     - If the summary indicates a missing fact (e.g., a shared link, a past commitment), delegate to `mail-searcher`.
     - Assemble a **fact packet** containing: the email summary, the sender, any free slots or search results, and the calendar event names (never titles).
     - Send the fact packet to `draft-writer` for a draft reply.
     - Receive back: `draft` text and `evidence` list.

5. **Validate the record**
   - Check that the record matches the output schema exactly.
   - Verify no fabricated facts are present; every fact has evidence.
   - Verify no commitments or decisions are made on the user's behalf.
   - If validation fails, flag for human review and do not save the draft.

6. **Assemble the final record**
   - Combine all received fields into a single JSON object following the schema in reference.md.
   - Mark the email as completed in the todo list.
   - Advance the step counter.
   - Check the timer; if 60 seconds have elapsed for this email, log a timeout warning and flag for review.

## Budget and error handling
- If the step counter reaches 30, stop processing and flag remaining emails as incomplete.
- If a subagent response is malformed (missing required fields, invalid JSON), retry once with a clearer request.
- If the retry fails, set `needs_human_review=true`, set `review_reason="Subagent response error; email needs manual assessment"`, and continue.
- If the timer exceeds 60 seconds for any email, flag it with `needs_human_review=true` and note the timeout.

## Output
- A list of completed records, each matching the schema in reference.md.
- A summary: number of records generated, number flagged for review, number with drafts saved.
- Any incomplete emails and the reason they were not processed (timeout, step limit, error).
