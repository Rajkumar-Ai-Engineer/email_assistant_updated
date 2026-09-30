# Email Classification Reference

## Category Definitions

| Category | Definition | Examples |
|----------|-----------|----------|
| **urgent** | Deadline today, escalation from a manager/customer, or contract/security risk. | "I need this by 5pm", customer threat, "issue critical to our SLA", manager approval request. |
| **needs_reply** | Sender asks a question, requests action, or expects acknowledgment from the user. | "Can we meet?", "Please review", "What do you think?", "Let me know." |
| **fyi** | Informational content; sender is not asking for a response. | Announcements, updates, reminders, auto-replies when not replying. |
| **newsletter** | Bulk content, bulk sender address, unsubscribe footer, periodic distribution. | "Data Weekly #212", "Monthly report", newsletter subscription email. |
| **spam** | Unsolicited marketing, cold outreach, scams, phishing, malicious content. | "Guaranteed top Google ranking", phishing links, gift-card requests. |

## Urgency Signals

A message is **urgent** if it includes any of:
- Explicit deadline today (e.g., "by 5pm today", "by end of business").
- Escalation from a manager (e.g., "I need your confirmation", "Please confirm you can make it").
- Escalation from a customer (e.g., complaint, threat to end contract).
- Security or contract risk (e.g., "we have a compliance issue").
- Threat or anger (e.g., "unacceptable", "if not fixed", "we will terminate").

## Newsletter Signals

A message is likely a **newsletter** if it includes:
- Unsubscribe footer (e.g., "You are receiving this because you subscribed. Unsubscribe: [link]").
- Bulk sender address (e.g., "newsletter@", "news@", "digest@", "noreply@").
- Issue or date number in subject (e.g., "#212", "Vol. 47").
- Bulk formatting (list of articles, table of contents).

## Auto-Reply Signals

Detect auto-replies by phrases:
- "I am out of office until [date]".
- "Out of office with limited access".
- "Automatic reply".
- "I will respond when I return".

**Action:** Do not draft a reply to an auto-reply. Set `needs_reply=false`. Note the return date in the summary if useful.

## Tie-Break Order (first match wins)

1. **Is it an auto-reply?** → `fyi`, `needs_reply=false`.
2. **Is it a newsletter?** → `newsletter`, `needs_reply=false`.
3. **Is it urgent?** (deadline today, manager/customer escalation, contract risk) → `urgent`, `needs_reply=true`.
4. **Does it ask for a response?** → `needs_reply`, `needs_reply=true`.
5. **Is it informational only?** → `fyi`, `needs_reply=false`.
6. **Is it spam or unsolicited?** → `spam`, `needs_reply=false`.

## Missing Context

If an email lacks clarity, state it in the summary:
- "Sender mentions 'that thing' but does not specify what."
- "No deadline is mentioned."
- "The email does not say which proposal is being reviewed."
- "Attachment only; body contains no text."

Flag these for human review in escalation rules.
