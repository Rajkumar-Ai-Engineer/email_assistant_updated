from typing import Literal

from pydantic import Field, field_validator

from .common import Strict


class DraftRequest(Strict):
    email_id: str = Field(min_length=1)
    body: str = Field(min_length=1, max_length=10000)

    @field_validator("email_id")
    @classmethod
    def _looks_like_message_id(cls, v):
        v = v.strip()
        if "@" in v or " " in v:
            raise ValueError("That looks like an email address. Enter the Gmail message id "
                             "(a hex string like 18c2f4a9b3d1e7f0), not an address.")
        return v

    @field_validator("body")
    @classmethod
    def _no_placeholders(cls, v):
        if any(p in v for p in ("[Your Name]", "[INSERT", "{{")):
            raise ValueError("draft contains unfilled placeholders")
        return v


class DraftResult(Strict):
    draft_id: str
    to: str
    subject: str
    status: Literal["saved_as_draft_not_sent"] = "saved_as_draft_not_sent"


class SendApproval(Strict):
    """Human-in-the-loop gate: sending requires explicit confirmation of this exact draft."""

    draft_id: str
    approved: bool
    confirm_recipient: str

    @field_validator("approved")
    @classmethod
    def _must_approve(cls, v):
        if not v:
            raise ValueError("Tick the approval checkbox to send.")
        return v


class SendResult(Strict):
    message_id: str
    thread_id: str = ""


class DraftProposal(Strict):
    """Reply text proposed by draft-writer; NOT saved yet."""

    email_id: str
    body: str = Field(min_length=1, max_length=10000)
