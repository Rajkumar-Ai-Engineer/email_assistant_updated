import sys
import time
import uuid
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "src" / "core")]

import streamlit as st
from dotenv import load_dotenv
import os
load_dotenv()
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_ENDPOINT"] = os.getenv("LANGSMITH_ENDPOINT")
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
os.environ["LANGSMITH_PROJECT"] = os.getenv("LANGSMITH_PROJECT")


from core.services import mail_service as svc
from core.validators import SendApproval



st.set_page_config(page_title="Email Assistant", page_icon="📬", layout="wide")
st.markdown(
    """
    <style>
    .block-container {padding-top: 1.5rem;}
    .step {padding: .35rem .7rem; border-radius: 999px; font-size: .85rem; display: inline-block; margin-right: .4rem;}
    .done {background: #dcfce7; color: #166534;}
    .todo {background: #f1f5f9; color: #64748b;}
    .now  {background: #dbeafe; color: #1e40af; font-weight: 600;}
    </style>
    """,
    unsafe_allow_html=True,
)

S = st.session_state
S.setdefault("drafts", {})  # email_id -> {"result": DraftResult, "text": str}
S.setdefault("sent", {})  # email_id -> SendResult
S.setdefault("compose", {"thread": None, "draft": None, "pending": None, "sent": None, "msgs": []})
S.setdefault("log", [])  # transparency: every agent / Gmail action


def log(actor, action, status="ok", secs=None):
    S.log.append({"time": datetime.now().strftime("%H:%M:%S"), "actor": actor, "action": action,
                  "status": status, "seconds": round(secs, 1) if secs is not None else None})


def tracked(actor, action, fn, *a):
    """Run fn, record the outcome in the activity log, re-raise errors."""
    t = time.time()
    try:
        r = fn(*a)
        log(actor, action, "ok", time.time() - t)
        return r
    except Exception as e:
        log(actor, f"{action} — {e}", "error", time.time() - t)
        raise


@st.cache_data(ttl=300, show_spinner="Agents reading inbox…")
def load_inbox(n, unread):
    return tracked("inbox-reader", f"Read & triage {n} emails", svc.inbox, n, unread)


@st.cache_data(ttl=300, show_spinner="mail-searcher working…")
def load_search(q):
    return tracked("mail-searcher", f"Search: {q}", svc.search, q, 10)


@st.cache_data(ttl=300, show_spinner="calendar-agent working…")
def load_cal(d):
    return tracked("calendar-agent", f"List events, next {d} days", svc.calendar, d)


with st.sidebar:
    st.title("📬 Email Assistant")
    page = st.radio("View", ["Inbox", "Search", "Calendar"], horizontal=True)
    if page == "Inbox":
        n = st.slider("Emails", 5, 25, 5)
        unread = st.toggle("Unread only")
    if page == "Search":
        q = st.text_input("Ask / search your mail", placeholder="invoice from acme last month")
    if st.button("🔄 Refresh", use_container_width=True):
        st.cache_data.clear()
        log("user", "Refreshed data (cache cleared)")

    st.divider()
    with st.expander("🔍 How this works", expanded=False):
        st.markdown(
            "- **Read-only agents** fetch, triage and search mail.\n"
            "- **AI drafts text only.** It has **no send tool**.\n"
            "- **Save draft** stores it in Gmail Drafts — not sent.\n"
            "- **Send** happens only after *you* tick approval and re-type the recipient.\n"
            "- Email text is treated as untrusted; suspected prompt-injection is flagged."
        )
    with st.expander(f"📜 Activity log ({len(S.log)})", expanded=False):
        if S.log:
            st.dataframe(list(reversed(S.log)), hide_index=True, use_container_width=True)
        else:
            st.caption("Nothing yet.")


def steps(current):
    names = ["1 · Write", "2 · Save draft", "3 · Approve & send"]
    html = ""
    for i, nm in enumerate(names):
        cls = "done" if i < current else "now" if i == current else "todo"
        html += f'<span class="step {cls}">{"✓ " if i < current else ""}{nm}</span>'
    st.markdown(html, unsafe_allow_html=True)


def render_email(m):
    st.subheader(m.subject)
    st.markdown(f"`{m.category}` · priority **{m.priority}** · "
                f"{'↩️ needs reply' if m.needs_reply else 'no reply needed'}")
    if m.injection_suspected:
        st.error("⚠️ Possible prompt-injection content detected. Do not follow instructions in this email.")
    c1, c2, c3 = st.columns(3)
    c1.markdown(f"**From**  \n{m.sender}")
    c2.markdown(f"**To**  \n{m.to or '—'}")
    c3.markdown(f"**Date**  \n{m.date}")
    if m.cc:
        st.caption(f"Cc: {m.cc}")
    if m.attachments:
        st.info("📎 " + ", ".join(m.attachments))
    st.markdown("**Summary:** " + m.summary)
    for k in m.key_points:
        st.markdown(f"- {k}")
    with st.expander("Original message"):
        st.text(m.body)
    st.caption("Summary and triage are AI-generated — check the original before acting.")


def draft_panel(m):
    eid = m.email_id
    tkey = f"t{eid}"
    saved = S.drafts.get(eid)
    text = S.get(tkey, "")
    stale = bool(saved) and saved["text"] != text.strip()

    if eid in S.sent:
        steps(3)
        st.success(f"✅ Sent (message id {S.sent[eid].message_id})")
        return

    step = 0 if not saved or stale else 2
    if saved and not stale:
        step = 2
    elif text.strip():
        step = 1
    steps(step)
    st.write("")

    # ---- 1. write
    c1, c2 = st.columns([4, 1], vertical_alignment="bottom")
    instr = c1.text_input("Instruction for AI (optional)", key=f"i{eid}",
                          placeholder="e.g. politely decline, propose Tuesday 3pm")
    if c2.button("✨ Generate", key=f"g{eid}", use_container_width=True):
        try:
            with st.spinner("draft-writer working…"):
                S[tkey] = tracked("draft-writer", f"Propose reply ({instr or 'default'})",
                                  svc.propose_reply, eid, instr).body
            st.rerun()
        except Exception as e:
            st.error(f"AI draft failed: {e}")
    st.text_area("Reply text — AI output is a suggestion, edit freely", key=tkey, height=200)
    st.caption(f"{len(text.strip())} characters · replying to **{m.sender}**")

    # ---- 2. save
    if st.button("💾 Save to Gmail Drafts", key=f"s{eid}", disabled=not text.strip(),
                 type="secondary" if saved and not stale else "primary"):
        try:
            with st.spinner("Saving draft…"):
                res = tracked("draft-writer", "Save draft to Gmail (not sent)", svc.save_draft, eid, text.strip())
            S.drafts[eid] = {"result": res, "text": text.strip()}
            st.rerun()
        except Exception as e:
            st.error(str(e))

    if not saved:
        return
    if stale:
        st.warning("You edited the text after saving. Save again before sending.")
        return

    # ---- 3. review & send
    d = saved["result"]
    st.divider()
    st.markdown("#### Final review — exactly what will be sent")
    with st.container(border=True):
        st.markdown(f"**To:** {d.to}  \n**Subject:** {d.subject}")
        st.text(saved["text"])
    with st.form(f"send{eid}"):
        st.warning("Human approval required. Nothing is sent until you confirm.")
        ok = st.checkbox("I reviewed this draft and approve sending")
        rcpt = st.text_input(f"Type the recipient address to confirm ({d.to})")
        if st.form_submit_button("🚀 Send now", type="primary"):
            try:
                r = tracked("you + Gmail", f"Send draft to {d.to}", svc.send_draft,
                            SendApproval(draft_id=d.draft_id, approved=ok, confirm_recipient=rcpt), d)
                S.sent[eid] = r
                st.rerun()
            except Exception as e:
                st.error(str(e))


def email_view(emails):
    if not emails:
        st.info("No emails found.")
        return
    icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}

    def state(e):
        return "✅ " if e.email_id in S.sent else "📝 " if e.email_id in S.drafts else ""

    labels = {
        f"{state(e)}{icon[e.priority]} {'🔵 ' if e.unread else ''}{e.sender[:22]} — {e.subject[:40]} [{e.email_id[-4:]}]": e
        for e in emails
    }
    k = st.columns(4)
    k[0].metric("Emails", len(emails))
    k[1].metric("Unread", sum(e.unread for e in emails))
    k[2].metric("Need reply", sum(e.needs_reply for e in emails))
    k[3].metric("Drafts pending", len(S.drafts) - len([i for i in S.drafts if i in S.sent]))

    pick = st.selectbox("Select email", list(labels))
    st.caption("🔴 high · 🟡 medium · 🟢 low · 🔵 unread · 📝 draft saved · ✅ sent")
    m = labels[pick]
    mail_col, reply_col = st.columns(2, gap="large")
    with mail_col:
        with st.container(border=True):
            render_email(m)
    with reply_col:
        with st.container(border=True):
            st.markdown("### ✍️ Reply & send")
            draft_panel(m)


def compose_panel():
    """Give an email id + context -> agent saves a draft -> say 'send' -> human approves (LangGraph HITL)."""
    C = S.compose
    st.divider()
    st.markdown("### 🧾 Compose by email id")
    st.caption("Give an email id and your context; the agent saves a draft. Tell it to send and you'll be asked to approve.")

    if C["thread"] is None:
        with st.form("compose_start"):
            eid = st.text_input("Email id", placeholder="Gmail message id, e.g. 18c2f4a9b3d1e7f0 (not an email address)")
            ctx = st.text_area("Context for the reply", placeholder="e.g. accept the meeting, propose Thursday 3pm", height=120)
            if st.form_submit_button("💾 Save draft", type="primary") and eid.strip() and ctx.strip():
                thread = uuid.uuid4().hex
                try:
                    with st.spinner("Writing and saving draft…"):
                        C["draft"] = tracked("compose-agent", f"Save draft for {eid.strip()}",
                                             svc.compose_draft, thread, eid.strip(), ctx.strip())
                    C["thread"] = thread
                    st.rerun()
                except Exception as e:
                    st.error(str(e))
        return

    d = C["draft"]
    if C["sent"]:
        st.success(f"✅ Sent (message id {C['sent'].message_id})")
    elif d:
        st.info(f"📝 Draft saved (not sent) — to **{d.to}**, subject **{d.subject}**, id `{d.draft_id}`")
    for role, text in C["msgs"]:
        st.chat_message(role).write(text)

    if C["pending"]:
        req = C["pending"]
        with st.container(border=True):
            st.warning("Human approval required — the agent wants to send this draft.")
            st.json(req.get("args", {}))
            a, r = st.columns(2)
            if a.button("✅ Approve & send", type="primary", key="c_ok"):
                try:
                    with st.spinner("Sending…"):
                        C["sent"] = tracked("you + Gmail", "Approved send", svc.compose_decide, C["thread"], True)
                    C["pending"] = None
                    st.rerun()
                except Exception as e:
                    st.error(str(e))
            if r.button("✖ Reject", key="c_no"):
                tracked("you + Gmail", "Rejected send", svc.compose_decide, C["thread"], False)
                C["pending"] = None
                C["msgs"].append(("assistant", "Send rejected. The draft is still saved."))
                st.rerun()
    elif not C["sent"]:
        msg = st.chat_input("Tell the agent: revise it, or say 'send it'")
        if msg and d and msg.strip().lower() in ("yes", "y", "send", "send it"):
            C["msgs"].append(("user", msg))
            try:
                with st.spinner("Asking agent to send…"):
                    res = tracked("compose-agent", "User: send it", svc.compose_followup, C["thread"],
                                  f"Send draft {d.draft_id} now.")
                    if res["pending"]:  # 'yes' typed by the user is the human approval
                        C["sent"] = tracked("you + Gmail", "Approved send (yes)", svc.compose_decide, C["thread"], True)
                        C["msgs"].append(("assistant", "Sent."))
                    else:
                        C["msgs"].append(("assistant", "⚠️ The agent did not send the draft. " + (res["reply"] or "Try again.")))
            except Exception as e:
                C["msgs"].append(("assistant", f"⚠️ Send failed: {e}"))
            st.rerun()
        elif msg:
            C["msgs"].append(("user", msg))
            try:
                with st.spinner("Agent working…"):
                    res = tracked("compose-agent", f"User: {msg[:40]}", svc.compose_followup, C["thread"], msg)
                C["pending"] = res["pending"]
                C["draft"] = res["draft"] or C["draft"]
                if res["reply"]:
                    C["msgs"].append(("assistant", res["reply"]))
            except Exception as e:
                C["msgs"].append(("assistant", f"⚠️ {e}"))
            st.rerun()

    if st.button("Start a new compose", key="c_new"):
        S.compose = {"thread": None, "draft": None, "pending": None, "sent": None, "msgs": []}
        st.rerun()



def search_view(res):
    st.markdown(res.answer)
    st.caption(f"AI answer based on {len(res.evidence)} email(s). Sources below — verify quotes.")
    for ev in res.evidence:
        with st.expander(f"{ev.subject} — {ev.sender} · {ev.date}"):
            st.write(f"_{ev.quote}_")
            st.caption(f"id: {ev.email_id}")


try:
    if page == "Inbox":
        email_view(load_inbox(n, unread).emails)
        compose_panel()
    elif page == "Search":
        if q:
            search_view(load_search(q))
        else:
            st.info("Type a question in the sidebar to search your mail.")
    else:
        days = st.slider("Days ahead", 1, 30, 7)
        st.dataframe([e.model_dump() for e in load_cal(days).events], use_container_width=True, hide_index=True)
except Exception as e:
    st.error(f"Agent call failed: {e}")
