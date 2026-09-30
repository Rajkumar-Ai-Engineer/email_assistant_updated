"""Service layer: every read/draft goes through the deep agent (main agent -> subagents).

Agent outputs are forced into Pydantic schemas via response_format. There is no send tool
in the agent; sending is done here only after human approval, via Gmail drafts.send.
"""

import uuid
from functools import lru_cache

from pydantic import BaseModel

from langgraph.types import Command

from core.agents.compose_agent import ComposeAgent
from core.agents.email_agent import EmailAgent
from core.prompts.prompt_factory import PromptContext
from core.tools.google_auth import gmail_service
from core.validators import (CalendarReport, DraftProposal, DraftRequest, DraftResult, InboxReport,
                             InboxRequest, SearchAnswer, SearchRequest, SendApproval, SendResult)

CTX = PromptContext(timezone="Asia/Kolkata", timezone_label="IST")


@lru_cache(maxsize=None)
def _agent(schema: type[BaseModel]):
    return EmailAgent(CTX).main_agent(response_format=schema)


def _run(schema: type[BaseModel], prompt: str):
    cfg = {"configurable": {"thread_id": uuid.uuid4().hex}}
    out = _agent(schema).invoke({"messages": [{"role": "user", "content": prompt}]}, cfg)
    return schema.model_validate(out["structured_response"])


def inbox(max_results=10, unread_only=False) -> InboxReport:
    r = InboxRequest(max_results=max_results, unread_only=unread_only)
    return _run(InboxReport, (
        f"Delegate to inbox-reader: fetch the {r.max_results} most recent "
        f"{'unread ' if r.unread_only else ''}inbox emails and triage each one. "
        "Return every email with its original fields (ids, from, to, cc, subject, date, attachments), "
        "triage, 2-4 key_points, and the original body verbatim (max 1500 chars)."))


def search(query: str, max_results=10) -> SearchAnswer:
    r = SearchRequest(query=query, max_results=max_results)
    return _run(SearchAnswer, (
        f"Delegate to mail-searcher: search the mailbox for: {r.query!r} (max {r.max_results} results). "
        "Answer concisely and cite every email used as evidence (id, subject, sender, date, short quote)."))


def calendar(days_ahead=7) -> CalendarReport:
    return _run(CalendarReport, f"Delegate to calendar-agent: list my events for the next {days_ahead} days.")


def propose_reply(email_id: str, instruction: str) -> DraftProposal:
    return _run(DraftProposal, (
        f"Delegate to draft-writer: write a reply to email id {email_id}. "
        f"Instruction: {instruction or 'reply appropriately'}. "
        "Do NOT call save_draft; just return the reply text."))


def save_draft(email_id: str, body: str) -> DraftResult:
    """Deterministic save (no LLM in the loop, so a draft is never silently skipped)."""
    from core.tools.gmail_tools import save_draft as save_draft_tool
    r = DraftRequest(email_id=email_id, body=body)
    d = save_draft_tool.invoke({"email_id": r.email_id, "body": r.body})
    if "draft_id" not in d:
        raise RuntimeError(d.get("error", "Draft was not saved."))
    return DraftResult.model_validate(d)


def send_draft(approval: SendApproval, draft: DraftResult) -> SendResult:
    """HITL gate: recipient must be re-typed to match the draft before anything is sent."""
    if approval.draft_id != draft.draft_id or approval.confirm_recipient.strip().lower() != draft.to.lower():
        raise PermissionError("Recipient confirmation does not match the draft; not sent.")
    res = gmail_service().users().drafts().send(userId="me", body={"id": draft.draft_id}).execute()
    return SendResult(message_id=res["id"], thread_id=res.get("threadId", ""))


# ---------- compose flow: save draft -> user says send -> human approval (LangGraph HITL) ----------

@lru_cache(maxsize=1)
def _compose():
    return ComposeAgent().build()


def _cfg(thread_id: str) -> dict:
    return {"configurable": {"thread_id": thread_id}}


def _last_tool_json(out: dict, name: str) -> dict | None:
    import json
    for m in reversed(out["messages"]):
        if getattr(m, "type", "") == "tool" and getattr(m, "name", "") == name:
            c = m.content
            if isinstance(c, list):  # content blocks -> join text parts
                c = "".join(b.get("text", "") if isinstance(b, dict) else str(b) for b in c)
            try:
                d = json.loads(c) if isinstance(c, str) else c
            except ValueError:
                return {"error": f"{name} returned non-JSON: {str(c)[:200]}"}
            return d if isinstance(d, dict) else {"error": f"{name} returned unexpected: {str(d)[:200]}"}
    return None


def _pending(out: dict) -> dict | None:
    """Return the paused send_draft action request, if the graph is waiting for a human."""
    for it in out.get("__interrupt__", []):
        for req in it.value.get("action_requests", []):
            if req["name"] == "send_draft":
                return req
    return None


def compose_draft(thread_id: str, email_id: str, context: str) -> DraftResult:
    r = DraftRequest(email_id=email_id, body=context)  # validates id / non-empty context
    out = _compose().invoke({"messages": [{"role": "user", "content": (
        f"Email id: {r.email_id}\nMy context for the reply:\n<<<\n{r.body}\n>>>\n"
        "Write the reply and save it as a draft. Do not send.")}]}, _cfg(thread_id))
    d = _last_tool_json(out, "save_draft")
    if not d or "draft_id" not in d:
        reply = out["messages"][-1].text if out["messages"] else ""
        raise RuntimeError((d or {}).get("error") or f"Agent did not save a draft. Agent said: {reply[:300]}")
    return DraftResult.model_validate(d)


def compose_followup(thread_id: str, message: str) -> dict:
    """Send a user message (e.g. 'make it shorter', 'send it'). Returns {'pending': action|None, 'draft': DraftResult|None, 'reply': str}."""
    out = _compose().invoke({"messages": [{"role": "user", "content": message}]}, _cfg(thread_id))
    d = _last_tool_json(out, "save_draft")
    return {"pending": _pending(out),
            "draft": DraftResult.model_validate(d) if d and "draft_id" in d else None,
            "reply": out["messages"][-1].text if out["messages"] else ""}


def compose_decide(thread_id: str, approve: bool, reason: str = "") -> SendResult | None:
    """Resume the paused graph with the human's decision; returns SendResult when sent."""
    decision = {"type": "approve"} if approve else {"type": "reject", "message": reason or "User rejected sending."}
    out = _compose().invoke(Command(resume={"decisions": [decision]}), _cfg(thread_id))
    s = _last_tool_json(out, "send_draft") if approve else None
    if s and "message_id" in s:
        return SendResult(message_id=s["message_id"], thread_id=s.get("thread_id", ""))
    if approve:
        raise RuntimeError((s or {}).get("error", "Send did not complete."))
    return None
