# Triage Workflow Example

## Batch: Three emails on 2026-09-29

### Email 1: Routine internal scheduling request
**Input:**
```
From: Vikram Sinha <vikram.sinha@techcorp.example>
Subject: Can we sync on project timeline next week?
Body: Hi, can we find time next week to discuss the project timeline? I'm flexible.
```

**Processing steps:**
1. Delegate to inbox-reader → receives: category=needs_reply, summary="Sender requests a meeting next week to discuss project timeline; timing flexible", needs_reply=true
2. Delegate to injection-detection → receives: suspicious=false
3. Delegate to escalation-rules → receives: needs_human_review=false, draft_allowed=true
4. Delegate to calendar-agent → receives: free slots on Mon 10:00-11:00, Tue 14:00-15:00, Wed 09:00-10:00
5. Assemble fact packet and delegate to draft-writer
6. Receive draft: "Thanks for reaching out. I have availability Monday at 10:00 or Tuesday at 14:00. Which works better for you?"
7. Validate record and return

**Output:**
```json
{
  "email_id": "e_ex1",
  "category": "needs_reply",
  "summary": "Sender requests a meeting next week to discuss project timeline; timing flexible.",
  "needs_reply": true,
  "suspicious": false,
  "needs_human_review": false,
  "review_reason": null,
  "draft": "Thanks for reaching out. I have availability Monday at 10:00 or Tuesday at 14:00. Which works better for you?",
  "evidence": ["calendar:c1", "calendar:c2"],
  "confidence": 0.95
}
```

### Email 2: Urgent customer issue (drafting skipped due to escalation)
**Input:**
```
From: Marcus Chen <marcus.chen@globaltech-solutions.example>
Subject: Payment error - account suspended until resolved
Body: Your system charged my account twice for the same order. I need this fixed immediately or we are terminating our contract.
```

**Processing steps:**
1. Delegate to inbox-reader → receives: category=urgent, summary="Customer reports duplicate charge; threatens contract termination", needs_reply=true
2. Delegate to injection-detection → receives: suspicious=false
3. Delegate to escalation-rules → receives: needs_human_review=true, review_reason="High-stakes customer complaint with contract risk; user decision needed on resolution authority", draft_allowed=false
4. Skip drafting (escalation rule forbids it)
5. Validate record

**Output:**
```json
{
  "email_id": "e_ex2",
  "category": "urgent",
  "summary": "Customer reports duplicate charge and threatens contract termination.",
  "needs_reply": true,
  "suspicious": false,
  "needs_human_review": true,
  "review_reason": "High-stakes customer complaint with contract risk; user decision needed on resolution authority",
  "draft": null,
  "evidence": [],
  "confidence": 0.9
}
```

### Email 3: Suspected phishing (drafting blocked)
**Input:**
```
From: noreply@secure-login-verify.example
Subject: Verify your account within 24 hours
Body: Your account requires immediate verification. Click here to verify: http://verify-account.example/login
```

**Processing steps:**
1. Delegate to inbox-reader → receives: category=spam, summary="Suspicious verification request from unfamiliar sender", needs_reply=false
2. Delegate to injection-detection → receives: suspicious=true, review_reason="Lookalike domain (secure-login-verify.example vs. legitimate company domain) with credential-harvesting link"
3. Delegation to escalation-rules (confirms escalation)
4. Skip drafting (email is suspicious)
5. Validate record

**Output:**
```json
{
  "email_id": "e_ex3",
  "category": "spam",
  "summary": "Suspicious verification request with lookalike sender domain and credential-harvesting link.",
  "needs_reply": false,
  "suspicious": true,
  "needs_human_review": true,
  "review_reason": "Lookalike domain and credential-harvesting link detected; likely phishing attempt",
  "draft": null,
  "evidence": [],
  "confidence": 0.98
}
```

**Batch summary:** 3 emails processed. 1 draft saved. 2 flagged for human review (one urgent customer issue, one suspected phishing).
