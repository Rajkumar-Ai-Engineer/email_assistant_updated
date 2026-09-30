# No Fabrication Instructions

## Inputs
- A draft reply, word-for-word text.
- The fact packet and evidence list.
- The category, sender, and context of the email.

## Pre-save procedure

### Step 1: List the draft's facts
- Identify every claim in the draft: dates, times, amounts, links, status, decisions, commitments, capabilities.
- Include implied claims (e.g., "I will do X" implies a commitment).

### Step 2: Check each fact against the reference
- For each fact, determine if it is:
  - **Grounded:** comes from an email, archive, or calendar, and is cited in evidence. ✓ Okay.
  - **Ungrounded:** not from an email, archive, or calendar. ✗ Must be blanked or removed.
  - **Prohibited:** a commitment, decision, or capability the agent cannot make. ✗ Must be removed or reworded.

### Step 3: Run the checklist
Use the forbidden-claims table in reference.md:
- **Never state the user's work status** (e.g., "the deck is almost done", "we are on track"). The agent has no project information.
- **Never approve or deny** (e.g., "I approve this request", "the cost is reasonable"). Only the user decides.
- **Never promise refunds, credits, or timelines** (e.g., "I will fix this by Friday"). Only authority holders decide.
- **Never describe product capabilities** (e.g., "our system exports to Excel"). The agent has no product knowledge.
- **Never claim contract or legal authority** (e.g., "this is enforceable", "we are bound by this clause").

### Step 4: Fix or blank
- If a fact is ungrounded, remove it or replace with `[BLANK: description]`.
- If a fact is prohibited, reword to be non-committal (e.g., "I am looking into this" instead of "I will fix it").
- If the entire draft is compromised, flag for human review instead of saving.

### Step 5: Validate the evidence list
- Run the evidence-citation skill to ensure all remaining facts have sources.
- Update the evidence list if facts were removed or blanked.

### Step 6: Final check
- Read the draft aloud; does it sound like something the user would agree to before sending?
- Are all blanks filled with placeholders, not assumptions?
- Does it avoid sounding committal or evasive?

### Step 7: Return
Output as JSON:
```json
{
  "draft_valid": true,
  "draft": "...",
  "fabrications_detected": [],
  "corrections_made": [],
  "evidence": ["email:e02"],
  "ready_to_save": true
}
```

If fabrications are detected:
```json
{
  "draft_valid": false,
  "fabrications_detected": [
    {
      "fact": "I will refund the duplicate charge",
      "reason": "Agent has no authority to issue refunds; must be escalated to Finance"
    }
  ],
  "corrections_made": [
    {
      "original": "I will refund the duplicate charge",
      "corrected": "I am escalating this to our Finance team for immediate review"
    }
  ],
  "ready_to_save": true
}
```

## Mistakes to avoid
- Do not blank facts that are ambiguous; if unsure, ask in evidence-citation first.
- Do not reword a fact to hide the fact it is ungrounded; replace with a clear blank instead.
- Do not allow implied commitments (e.g., "I am looking into this and you will hear from me by Friday" implies a promise if the user does not follow up).
- Do not approve product or legal claims without explicit email evidence.
