# Escalation Rules Example

## Case 1: Angry customer with contract risk
**Email:**
```
From: alex.johnson@manufacturingcorp.example
Subject: Payment processing failed - urgent resolution needed
Body: We have been trying to process a payment for the last 3 days with no success. This is unacceptable. If it is not resolved by tomorrow morning, we are canceling our contract.
```

**Analysis:**
- Trigger: "unacceptable", "canceling", deadline tomorrow.
- Sender: known customer.
- High-stakes content: contract termination threat.

**Decision:**
```json
{
  "needs_human_review": true,
  "draft_allowed": true,
  "review_reason": "Customer threatening contract termination over payment issue; user needs to verify resolution authority and escalation path to Finance."
}
```

**Draft example (safe holding reply):**
"Thank you for bringing this to my attention. I understand this is urgent. I am escalating this to our Finance team immediately. You will hear back from us first thing tomorrow morning."

---

## Case 2: Vague internal request
**Email:**
```
From: priya.saha@techcorp.example
Subject: Can you review the proposal?
Body: Hi, can you review the proposal and let me know your thoughts? Thanks, Priya
```

**Analysis:**
- Trigger: no specific proposal named, no context, no deadline.
- Sender: internal colleague.
- Missing information: which proposal?

**Decision:**
```json
{
  "needs_human_review": true,
  "draft_allowed": true,
  "review_reason": "Email does not specify which proposal; draft asks the sender to clarify."
}
```

**Draft example:**
"Hi Priya, I'd be happy to review. Could you share the link or attachment? I want to make sure I'm looking at the right document."

---

## Case 3: External scheduling request from unknown contact
**Email:**
```
From: diana.lee@partnervc.example
Subject: Intro call next Tuesday at 10:00?
Body: Hi, I'm Diana Lee from Partner VC. I'd love to discuss potential opportunities. Would next Tuesday at 10:00 work?
```

**Analysis:**
- Trigger: unknown external sender, scheduling request.
- Sender: external, not a known contact.
- No sensitive data request, no contract risk.
- Reasonable business inquiry.

**Decision:**
```json
{
  "needs_human_review": true,
  "draft_allowed": true,
  "review_reason": "External sender not in known contacts; user should verify legitimacy before confirming meeting."
}
```

**Draft example:**
"Thanks for reaching out, Diana. I'd be interested in learning more. Let me check my calendar and get back to you shortly."

---

## Case 4: Routine internal message (no escalation)
**Email:**
```
From: rahul.kumar@techcorp.example
Subject: Updated sprint schedule for next week
Body: Hi team, the sprint schedule for next week is now finalized. Please update your calendars accordingly. Details are in the attached doc.
```

**Analysis:**
- Trigger: informational, no decision, no deadline, no escalation, no sensitive data.
- Sender: internal colleague.
- Routine message.

**Decision:**
```json
{
  "needs_human_review": false,
  "draft_allowed": false,
  "review_reason": null
}
```

(No draft needed; user can acknowledge directly or ignore as appropriate.)
