# No Fabrication Example

## Example 1: Status claim (fabricated)
**Before (BAD):**
```
Hi Ananya,

The Q3 metrics deck is almost done. I will have the final version to you by 4pm today.

Regards,
Priya
```

**Issue:** "Almost done" is a fabricated status claim; the agent has no info on deck completion.

**After (GOOD):**
```
Hi Ananya,

I understand the board pre-read goes out tonight. I am reviewing the current status of the deck and will confirm with you by 4pm whether we can make the deadline.

Regards,
Priya
```

**Why:** Reworded to acknowledge the deadline without claiming status the agent does not know.

---

## Example 2: Approval (prohibited)
**Before (BAD):**
```
Hi Meera,

I approve the data-labeling vendor proposal at INR 3.95 lakh. Please proceed with procurement.

Regards,
Priya
```

**Issue:** Agent cannot approve vendor contracts; only authorized approvers can.

**After (GOOD):**
```
Hi Meera,

Thank you for flagging the INR 3.95 lakh proposal. I have reviewed the details. Please let me know if you would like to move forward, and I will confirm with [BLANK: approval authority] to ensure we proceed.

Regards,
Priya
```

**Why:** Reworded to leave the decision to the user; the blank prompts for clarification on who should approve.

---

## Example 3: Unsubstantiated link
**Before (BAD):**
```
Hi Sneha,

Here is the Q3 planning doc: https://docs.northwind-analytics.example/q3-documents

Please add your section by Friday.

Regards,
Priya
```

**Issue:** Link is guessed; archive shows the correct URL is "/q3-planning", not "/q3-documents".

**After (GOOD):**
```
Hi Sneha,

Here is the Q3 planning doc: https://docs.northwind-analytics.example/q3-planning

Please add your section by Friday.

Regards,
Priya
```

**Evidence:** archive:a01

**Why:** Corrected to the exact URL from the archive; evidence cites the source.

---

## Example 4: Refund promise (prohibited)
**Before (BAD):**
```
Dear Alex,

I sincerely apologize for the duplicate charge. I will credit your account for the full amount (INR 2,75,000) immediately.

Regards,
Priya
```

**Issue:** Agent has no authority to issue refunds; only Finance can.

**After (GOOD):**
```
Dear Alex,

I sincerely apologize that you have experienced this billing error. I understand you were charged twice for INV-20418 and INV-20431.

I am escalating this to our Finance team immediately for investigation and correction. Finance will reach out to you by end of business tomorrow with an update.

Regards,
Priya
```

**Why:** Removed the refund promise; escalates to Finance instead. Acknowledges the specific issue without committing a resolution.

---

## Example 5: Already correct (no fabrication)
**Draft:**
```
Hi Rahul,

Thanks for reaching out. Thursday afternoon works well for me. How about 14:00?

Best,
Priya
```

**Fact check:**
- "Thursday afternoon" → from email (e07 says "Thursday afternoon works best for me").
- "14:00" → from calendar (free slot found on Thursday 14:00–17:00).
- Evidence: email:e07, calendar:c01.

**Pre-save checklist:**
- [ ] Dates/times from email or calendar? ✓ Yes.
- [ ] No approval/denial? ✓ Correct (just proposing a time).
- [ ] No promises? ✓ Correct.
- [ ] No product claims? ✓ Correct.
- [ ] No contract claims? ✓ Correct.
- [ ] Facts cited in evidence? ✓ Yes.
- [ ] Sounds natural? ✓ Yes.

**Verdict:** Ready to save. No corrections needed.
