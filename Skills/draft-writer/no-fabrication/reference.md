# No Fabrication Reference

## Forbidden Claims Table

| Claim type | Why forbidden | Example (BAD) | Safe alternative |
|-----------|---|---|---|
| Work status | Agent has no project info | "The deck is 90% done" | "I am reviewing the status and will confirm by [time]" |
| Approval or denial | Agent cannot decide | "I approve the budget request" | "I will review and get back to you" |
| Refund or credit | Agent has no authority | "I will credit your account" | "I am escalating to Finance for review" |
| Deadline promise | Agent cannot commit the user | "I will have this by Friday" | "I will aim for Friday; I will confirm if that is feasible" |
| Product capability | Agent has no product knowledge | "Our system exports to CSV" | "I will check with the team on export formats" |
| Contract authority | Agent cannot bind the company | "This clause is binding" | "I will route this to Legal for review" |
| Legal commitment | Agent has no legal authority | "We are liable for this" | "I will escalate to our Legal team" |
| Advice or decision | Agent should not decide for user | "You should take the job" | "Here are the options to consider" |
| Team commitment | Agent cannot commit others | "The team can deliver by October" | "I will check with the team on timeline" |

## Pre-Save Checklist

Answer "yes" to all before saving:

- [ ] **Every date/time/amount in the draft comes from email, archive, or calendar.**
  - If not: blank it with `[BLANK: ...]` or remove it.

- [ ] **The draft makes no approval or denial on the user's behalf.**
  - If it does: reword to "I will review..." or "Please decide on...".

- [ ] **The draft makes no promises about delivery, refunds, credits, or timeline that the user cannot authorize.**
  - If it does: reword to "I am escalating to [team]..." or "I will check on this...".

- [ ] **The draft states no product capability or feature that is not in an email.**
  - If it does: reword to "I will confirm what the system can do..." or remove it.

- [ ] **The draft states no contract, legal, or compliance fact that is not from an email or archive.**
  - If it does: reword to "I will route to Legal..." or remove it.

- [ ] **The draft states no work status, project timeline, or team commitment that is not in an email.**
  - If it does: reword to "I will check on status with the team..." or remove it.

- [ ] **Every claim in the draft is cited in the evidence list (or is a placeholder or preamble text like "Hi...").**
  - If not: update evidence or blank the fact.

- [ ] **The draft sounds like something the user would want to send without editing (except filling blanks).**
  - If not: revise for tone, clarity, or length.

## Fact-Checking Examples

**Example 1: Ungrounded date**
```
Original draft: "I will have the report ready by Friday."
Issue: No source for Friday deadline.
Evidence list: Only contains email:e09 (which says deadline is 5pm today, not Friday).
Fix: "I will review and confirm the timeline by end of business today."
OR: "[BLANK: confirm Friday deadline with user before sending]"
```

**Example 2: Prohibited status claim**
```
Original draft: "The Q3 metrics deck is nearly complete."
Issue: Agent has no info on deck status.
Evidence list: Empty for this fact.
Fix: "I am reviewing the current status of the deck and will confirm with you shortly."
```

**Example 3: Prohibited approval**
```
Original draft: "I approve the data-labeling vendor contract for INR 3.95 lakh."
Issue: Agent cannot approve contracts; only authorized people can.
Evidence list: Has the cost, but not approval authority.
Fix: "The proposal is INR 3.95 lakh. Please let me know if you would like to proceed, and I will confirm with Meera."
```

**Example 4: Ungrounded link**
```
Original draft: "Here is the Q3 planning doc: https://docs.northwind-analytics.example/q3-planning"
Issue: Link must be from email or archive.
Evidence list: Contains archive:a01, which has the exact link.
Fix: Okay to send; evidence cites a01.
```

**Example 5: Prohibited capability claim**
```
Original draft: "Our dashboards can export to Excel, PDF, and CSV."
Issue: Agent has no product knowledge.
Evidence list: No email mentions these capabilities.
Fix: "I will confirm what export formats our dashboards support and get back to you."
```
