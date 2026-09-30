# Evidence Citation Reference

## ID Formats

| Source | Format | Example |
|--------|--------|---------|
| Current email | `email:<id>` | `email:e02` |
| Archived email | `archive:<id>` | `archive:a01` |
| Calendar event | `calendar:<id>` | `calendar:c05` |

## Fact Type to Acceptable Source Mapping

| Fact type | Acceptable source | Notes |
|-----------|------------------|-------|
| Sender name or email | `email:<id>` | From: field of the email |
| Recipient / addressee | `email:<id>` | To: field or body mention |
| Date mentioned in email | `email:<id>` | When sender says "by Friday" or "tomorrow" |
| Calendar date/time | `calendar:<id>` | From calendar system; must be exact |
| Link or URL | `email:<id>` or `archive:<id>` | Must be quoted from email body, not guessed |
| Money amount (INR, USD, etc.) | `email:<id>` | Must be from email text |
| Invoice number | `email:<id>` | From email body |
| Product capability | None (not in scope) | Agent has no product info; leave blank |
| Work status | None (not in scope) | Agent has no project info; leave blank |
| Customer complaint details | `email:<id>` | From customer's email |
| Manager request | `email:<id>` | From manager's email |
| Prior commitment | `archive:<id>` | From earlier email in archive |
| Decision approval | None (not in scope) | Agent cannot make decisions; leave blank |

## What Does NOT Count as Evidence

- **Memory or assumption:** "The user told me last month..." or "I assume the team is working on this."
- **Inference:** "The customer is probably unhappy based on the tone."
- **Guessed capability:** "Excel export probably works" — no source.
- **Common knowledge:** "Priya is a PM" — even if known, needs to come from email or archive.
- **The user's status or plans:** "The user has not replied yet" — not a fact to cite; describe what you see instead.

## Blanking Guidelines

When a fact is missing:

| Situation | Blank template | Example |
|-----------|---|---------|
| Missing date/deadline | `[BLANK: <deadline type>]` | `[BLANK: resolution deadline]` |
| Unknown status | `[BLANK: <status type>]` | `[BLANK: current project status]` |
| Missing link | `[BLANK: <document name> link]` | `[BLANK: Q3 planning doc link]` |
| Unknown approval | `[BLANK: <decision type>]` | `[BLANK: cost center approval]` |
| Missing amount | `[BLANK: <amount type>]` | `[BLANK: refund amount]` |

## Example Evidence Lists

**Scenario 1: Customer complaint with archive reference**
```
Facts: customer name "Alex Johnson", complaint "duplicate charge", amount "INR 2,75,000", escalation
Sources: Alex's email (e02), amount in email (e02), archive of prior complaint (a05)
Evidence: ["email:e02", "archive:a05"]
```

**Scenario 2: Calendar scheduling**
```
Facts: "Thursday 1 Oct", "09:00-10:00", "conflict with Design review"
Sources: email said Thursday 1 Oct 09:00 (e07), calendar shows Design review (c04)
Evidence: ["email:e07", "calendar:c04"]
```

**Scenario 3: Draft with missing info**
```
Facts: "Q3 metrics deck", status missing, "board pre-read tonight"
Sources: email (e09) mentions the deck and deadline but not status
Evidence: ["email:e09"]
Blanks: [{"placeholder": "[BLANK: deck status]", "reason": "No information about whether deck is ready"}]
```
