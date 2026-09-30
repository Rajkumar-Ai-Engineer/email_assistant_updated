"""LangChain tools backed by the real Gmail and Google Calendar APIs.

Tool names and return shapes match verify_tool.py (the dummy-data version) so the
Skills work unchanged. Deliberately absent: send, forward, archive, delete.
"""

import base64
import re
from datetime import datetime, timedelta
from email.message import EmailMessage
from email.utils import parseaddr
from html import unescape
from zoneinfo import ZoneInfo

from langchain_core.tools import tool

from core.tools.google_auth import calendar_service, gmail_service

TZ = ZoneInfo("Asia/Kolkata")
MAX_BODY_CHARS = 8000
MAX_RESULTS_CAP = 25


# ---------- helpers ----------

def _header(payload: dict, name: str) -> str:
    for h in payload.get("headers", []):
        if h["name"].lower() == name.lower():
            return h["value"]
    return ""


def _decode(data: str) -> str:
    return base64.urlsafe_b64decode(data + "=" * (-len(data) % 4)).decode("utf-8", errors="replace")


def _html_to_text(html: str) -> str:
    html = re.sub(r"(?is)<(script|style).*?</\1>", "", html)
    html = re.sub(r"(?i)<br\s*/?>|</p>|</div>", "\n", html)
    return re.sub(r"\n{3,}", "\n\n", unescape(re.sub(r"<[^>]+>", "", html))).strip()


def _walk(payload: dict):
    yield payload
    for part in payload.get("parts", []) or []:
        yield from _walk(part)


def _body_and_attachments(payload: dict) -> tuple[str, list[str]]:
    plain, html, attachments = "", "", []
    for part in _walk(payload):
        if part.get("filename"):
            attachments.append(part["filename"])
            continue
        data = part.get("body", {}).get("data")
        if not data:
            continue
        if part.get("mimeType") == "text/plain" and not plain:
            plain = _decode(data)
        elif part.get("mimeType") == "text/html" and not html:
            html = _decode(data)
    return (plain or _html_to_text(html)).strip(), attachments


def _to_email(msg: dict, include_body: bool = True) -> dict:
    payload = msg["payload"]
    out = {
        "id": msg["id"],
        "thread_id": msg["threadId"],
        "from": _header(payload, "From"),
        "to": _header(payload, "To"),
        "cc": _header(payload, "Cc"),
        "subject": _header(payload, "Subject"),
        "date": _header(payload, "Date"),
        "labels": msg.get("labelIds", []),
    }
    if include_body:
        body, attachments = _body_and_attachments(payload)
        out["body"] = body[:MAX_BODY_CHARS] + ("\n[truncated]" if len(body) > MAX_BODY_CHARS else "")
        out["attachments"] = attachments  # names only; contents are never read
    else:
        out["snippet"] = msg.get("snippet", "")
    return out


def _list(query: str, max_results: int, include_body: bool) -> list[dict]:
    svc = gmail_service()
    n = max(1, min(max_results, MAX_RESULTS_CAP))
    refs = svc.users().messages().list(userId="me", q=query, maxResults=n).execute().get("messages", [])
    fmt = "full" if include_body else "metadata"
    return [
        _to_email(svc.users().messages().get(userId="me", id=r["id"], format=fmt).execute(), include_body)
        for r in refs
    ]


# ---------- email tools ----------

@tool
def get_inbox(max_results: int = 10, unread_only: bool = False) -> list[dict]:
    """Return recent inbox emails (newest first) with full bodies.

    Args:
        max_results: How many emails to return (1-25).
        unread_only: Only return unread emails.
    """
    return _list("in:inbox" + (" is:unread" if unread_only else ""), max_results, True)


@tool
def get_email(email_id: str) -> dict:
    """Return a single email by its Gmail message id, including body and attachment names."""
    try:
        msg = gmail_service().users().messages().get(userId="me", id=email_id, format="full").execute()
    except Exception as exc:
        return {"error": f"Email {email_id!r} could not be fetched: {exc}"}
    return _to_email(msg)


@tool
def get_thread(thread_id: str) -> list[dict]:
    """Return every message in a thread, oldest first. The last message is the most recent."""
    try:
        t = gmail_service().users().threads().get(userId="me", id=thread_id, format="full").execute()
    except Exception as exc:
        return [{"error": f"Thread {thread_id!r} could not be fetched: {exc}"}]
    return [_to_email(m) for m in t.get("messages", [])]


@tool
def search_emails(query: str, max_results: int = 10) -> list[dict]:
    """Search the whole mailbox (inbox and archive) using Gmail search syntax.

    Examples: 'invoice from:acme.com', 'subject:offsite after:2026/08/01', 'has:attachment budget'.
    Returns id, thread_id, from, subject, date, and a snippet; call get_email for the full body.

    Args:
        query: Gmail search string.
        max_results: How many results to return (1-25).
    """
    return _list(query, max_results, False)


@tool
def save_draft(email_id: str, body: str) -> dict:
    """Save a reply to an email as a Gmail DRAFT. This never sends anything.

    Args:
        email_id: Id of the email being replied to; recipient, subject, and threading are derived from it.
        body: Plain-text reply body.
    """
    svc = gmail_service()
    try:
        orig = svc.users().messages().get(userId="me", id=email_id, format="metadata").execute()
    except Exception as exc:
        return {"error": f"Email {email_id!r} could not be fetched: {exc}"}
    p = orig["payload"]
    reply_to = _header(p, "Reply-To") or _header(p, "From")
    subject = _header(p, "Subject")
    msg_id = _header(p, "Message-ID") or _header(p, "Message-Id")

    m = EmailMessage()
    m["To"] = parseaddr(reply_to)[1] or reply_to
    m["Subject"] = subject if subject.lower().startswith("re:") else f"Re: {subject}"
    if msg_id:
        m["In-Reply-To"] = msg_id
        m["References"] = msg_id
    m.set_content(body)

    raw = base64.urlsafe_b64encode(m.as_bytes()).decode()
    draft = svc.users().drafts().create(
        userId="me", body={"message": {"raw": raw, "threadId": orig["threadId"]}}
    ).execute()
    return {"draft_id": draft["id"], "to": m["To"], "subject": m["Subject"], "status": "saved_as_draft_not_sent"}


@tool
def send_draft(draft_id: str) -> dict:
    """Send an existing Gmail draft. Only call when the user explicitly asks to send.

    A human approval step is enforced by middleware before this runs.

    Args:
        draft_id: Id returned by save_draft.
    """
    try:
        res = gmail_service().users().drafts().send(userId="me", body={"id": draft_id}).execute()
    except Exception as exc:
        return {"error": f"Draft {draft_id!r} could not be sent: {exc}"}
    return {"message_id": res["id"], "thread_id": res.get("threadId", ""), "status": "sent"}


# ---------- calendar tools ----------

@tool
def get_calendar(days_ahead: int = 7, start_date: str = "") -> list[dict]:
    """Return the user's primary-calendar events (IST) for a window.

    Args:
        days_ahead: Window length in days (1-60).
        start_date: ISO date 'YYYY-MM-DD' to start from; defaults to today.
    """
    days = max(1, min(days_ahead, 60))
    start = (
        datetime.fromisoformat(start_date).replace(tzinfo=TZ)
        if start_date
        else datetime.now(TZ).replace(hour=0, minute=0, second=0, microsecond=0)
    )
    res = calendar_service().events().list(
        calendarId="primary",
        timeMin=start.isoformat(),
        timeMax=(start + timedelta(days=days)).isoformat(),
        singleEvents=True,
        orderBy="startTime",
        maxResults=100,
    ).execute()
    return [
        {
            "id": e["id"],
            "title": e.get("summary", "(no title)"),
            "start": e["start"].get("dateTime", e["start"].get("date")),
            "end": e["end"].get("dateTime", e["end"].get("date")),
            "attendees": [a.get("email", "") for a in e.get("attendees", [])],
            "status": e.get("status", ""),
        }
        for e in res.get("items", [])
    ]


@tool
def get_free_busy(start: str, end: str) -> list[dict]:
    """Return busy intervals only (no titles or attendees) between two ISO datetimes.

    Prefer this over get_calendar when the result will inform a reply to an external contact.

    Args:
        start: ISO datetime, e.g. '2026-09-30T09:00:00+05:30'.
        end: ISO datetime, e.g. '2026-09-30T17:00:00+05:30'.
    """
    res = calendar_service().freebusy().query(
        body={"timeMin": start, "timeMax": end, "timeZone": "Asia/Kolkata", "items": [{"id": "primary"}]}
    ).execute()
    return res["calendars"]["primary"].get("busy", [])


@tool
def get_user_context() -> dict:
    """Return the mailbox owner's profile, frequent contacts, and the current date/time."""
    prof = gmail_service().users().getProfile(userId="me").execute()
    now = datetime.now(TZ)

    # Known contacts = people the user has emailed recently (Sent folder).
    contacts: dict[str, str] = {}
    for m in _list("in:sent", 25, False):
        name, addr = parseaddr(m["to"].split(",")[0]) if m["to"] else ("", "")
        if addr:
            contacts.setdefault(addr.lower(), name)
    return {
        "user": {"email": prof["emailAddress"], "working_hours": "Mon-Fri 09:00-17:00 IST"},
        "known_contacts": [{"name": n, "email": a} for a, n in contacts.items()],
        "today": now.date().isoformat(),
        "current_time": now.isoformat(timespec="seconds"),
        "timezone": "Asia/Kolkata",
    }


TOOLS = [get_inbox, get_email, get_thread, search_emails, save_draft, get_calendar, get_free_busy, get_user_context]

# Per-subagent subsets (least privilege), mirroring the Skills folders.
INBOX_READER_TOOLS = [get_inbox, get_email, get_thread, get_user_context]
MAIL_SEARCHER_TOOLS = [search_emails, get_email, get_thread]
CALENDAR_TOOLS = [get_calendar, get_free_busy, get_user_context]
DRAFT_WRITER_TOOLS = [get_email, get_thread, save_draft]
# Only the compose agent gets send_draft, and only behind human-in-the-loop approval.
COMPOSE_TOOLS = [get_email, get_thread, save_draft, send_draft]
