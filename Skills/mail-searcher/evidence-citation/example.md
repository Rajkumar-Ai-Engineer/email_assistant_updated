# Evidence Citation Example

## Example 1: Mapping facts to email sources
**Draft:**
```
Hi Alex,

Thank you for bringing the duplicate charge issue to our attention. I see that both INV-20418 and INV-20431 (INR 2,75,000 each) were charged to your account on the same day.

I am escalating this immediately to our Finance team for investigation. You will hear back from us by end of business tomorrow.

Best,
Priya
```

**Fact analysis:**
- Fact: "duplicate charge issue" → Source: `email:e02` (customer email)
- Fact: "both INV-20418 and INV-20431" → Source: `email:e02` (invoice numbers mentioned)
- Fact: "INR 2,75,000 each" → Source: `email:e02` (amount stated)
- Fact: "same day" → Source: `email:e02` (implied from customer's message)

**Evidence:**
```json
{
  "fact_checked": true,
  "evidence": ["email:e02"],
  "blanks_introduced": []
}
```

---

## Example 2: Calendar scheduling with archive reference
**Draft:**
```
Hi Sneha,

Here is the Q3 planning document link: https://docs.northwind-analytics.example/q3-planning

It was posted by Ananya on 15 September. You should be able to access it directly.

Thanks,
Priya
```

**Fact analysis:**
- Fact: "Q3 planning document" → Source: `archive:a01` (document mentioned)
- Fact: "link https://docs.northwind-analytics.example/q3-planning" → Source: `archive:a01` (exact link)
- Fact: "posted by Ananya" → Source: `archive:a01` (sender)
- Fact: "15 September" → Source: `archive:a01` (date of email)

**Evidence:**
```json
{
  "fact_checked": true,
  "evidence": ["archive:a01"],
  "blanks_introduced": []
}
```

---

## Example 3: Scheduling conflict with calendar reference
**Draft:**
```
Hi Karthik,

Thank you for the update on the vendor demo time. Thursday 1 Oct at 09:00 works in principle, but I have a conflict with a prior commitment at that time.

Can we propose an alternative time on Thursday afternoon (13:00 or later)?

Best,
Priya
```

**Fact analysis:**
- Fact: "vendor demo" → Source: `email:e07` (thread about vendor demo)
- Fact: "Thursday 1 Oct at 09:00" → Source: `email:e07` (latest message in thread)
- Fact: "conflict with a prior commitment" → Source: `calendar:c04` (Design review 09:00-10:00)
- Fact: "cannot reference commitment title to external contact" → Source: N/A (privacy rule)

**Evidence:**
```json
{
  "fact_checked": true,
  "evidence": ["email:e07", "calendar:c04"],
  "blanks_introduced": []
}
```

---

## Example 4: Draft with missing information (blanked)
**Draft (before citation):**
```
Hi Ananya,

I understand the board pre-read goes out tonight and you need the final Q3 metrics deck by 5pm today. I am reviewing the current status of the deck and will get back to you shortly with a confirmation.

[BLANK: deck completion status]

Best,
Priya
```

**Fact analysis:**
- Fact: "board pre-read tonight" → Source: `email:e09` (stated by Ananya)
- Fact: "5pm today" → Source: `email:e09` (deadline stated)
- Fact: "Q3 metrics deck" → Source: `email:e09` (mentioned)
- Fact: "deck status" → Source: NONE (agent has no information about deck completion)

**Evidence (after citation):**
```json
{
  "fact_checked": true,
  "evidence": ["email:e09"],
  "blanks_introduced": [
    {
      "placeholder": "[BLANK: deck completion status]",
      "reason": "Agent has no information about whether the Q3 metrics deck is ready; user must confirm."
    }
  ]
}
```

**Note:** The blank is intentional; the draft asks the user to fill it in before sending.
