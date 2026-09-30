# Email Classification Example

## Example 1: Urgent manager request
**Email:**
```
From: priya.sharma@acmeinc.example
Subject: Budget approval needed - board review today at 4pm
Body: Priya, I need you to confirm that the Q3 budget has been finalized by 3pm today. The board review is at 4pm and I need this locked in.
```

**Analysis:**
- Deadline: 3pm today.
- Escalation: from a manager (implied by authority and board context).
- Ask: confirm budget finalization.

**Output:**
```json
{
  "category": "urgent",
  "summary": "Manager requests confirmation that Q3 budget is finalized by 3pm today for board review at 4pm.",
  "needs_reply": true,
  "confidence": 0.98
}
```

---

## Example 2: Routine internal needs_reply
**Email:**
```
From: harsha.gupta@acmeinc.example
Subject: Team lunch on Friday?
Body: Hi, several of us are thinking of grabbing lunch on Friday. Are you interested? Let me know!
```

**Analysis:**
- No deadline, no urgency signal.
- Sender asks a question and expects a yes/no.
- Informational tone; friendly.

**Output:**
```json
{
  "category": "needs_reply",
  "summary": "Colleague invites the user to team lunch on Friday.",
  "needs_reply": true,
  "confidence": 0.9
}
```

---

## Example 3: Newsletter
**Email:**
```
From: newsletter@techtrends.example
Subject: Tech Trends Weekly #145 - AI, Cloud, DevOps
Body: This week's top stories:
1. LLM benchmarking in production
2. Kubernetes 1.31 features
3. Cost optimization in multi-cloud

Read full issue: https://techtrends.example/issues/145

You are receiving this because you subscribed. Unsubscribe: https://techtrends.example/unsubscribe
```

**Analysis:**
- Bulk sender (newsletter@).
- Issue number in subject (#145).
- Unsubscribe footer.
- No ask for response.

**Output:**
```json
{
  "category": "newsletter",
  "summary": "Weekly technology newsletter covering AI, cloud, and DevOps topics.",
  "needs_reply": false,
  "confidence": 0.99
}
```

---

## Example 4: Vague email with missing context (ambiguous)
**Email:**
```
From: ravi.menon@acmeinc.example
Subject: Re: feedback on the plan
Body: Thanks for the input. Did you have a chance to review the latest iteration? I'd like to hear your thoughts before the meeting next week.
```

**Analysis:**
- No specific plan or document named.
- Context is lost (earlier message not included).
- Sender asks for feedback but on what?
- This is a reply in a thread but lacks context.

**Output:**
```json
{
  "category": "needs_reply",
  "summary": "Sender asks for feedback on an unspecified plan before a meeting next week; the specific document or plan is not identified in this message.",
  "needs_reply": true,
  "confidence": 0.65
}
```

**Note:** This email would trigger human review in escalation rules because the ask is unclear.

---

## Example 5: Out-of-office auto-reply
**Email:**
```
From: suresh.iyer@acmeinc.example
Subject: Out of office autoreply
Body: Hello, I am away from the office until 12 October with minimal email access. Please reach out to my backup contact Vikram Rao for urgent items.
```

**Analysis:**
- Auto-reply signature present.
- Return date specified.
- No ask for response.

**Output:**
```json
{
  "category": "fyi",
  "summary": "Auto-reply: Suresh is away until 12 October with limited email access; contact Vikram Rao for urgent matters.",
  "needs_reply": false,
  "confidence": 0.99
}
```

**Note:** Never reply to auto-replies.

---

## Example 6: Spam / cold outreach
**Email:**
```
From: sales@quoteengine.example
Subject: 50% off your next 3 months of QuoteEngine Pro - limited time!
Body: Special offer just for you! Get 50% off our enterprise quoting platform for your first 3 months. Upgrade your workflow today!

Reply to this email to get started.
```

**Analysis:**
- Unsolicited marketing.
- Bold promotional language.
- No prior relationship implied.

**Output:**
```json
{
  "category": "spam",
  "summary": "Promotional cold-outreach email for a quoting platform service.",
  "needs_reply": false,
  "confidence": 0.95
}
```
