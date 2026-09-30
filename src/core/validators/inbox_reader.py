from typing import Literal

from pydantic import Field, computed_field, field_validator

from .common import Strict, clean_addr, parseaddr

Category = Literal["action_required", "fyi", "newsletter", "meeting", "spam", "other"]
Priority = Literal["high", "medium", "low"]


class Email(Strict):
    id: str
    thread_id: str
    sender: str = Field("", alias="from")
    to: str = ""
    cc: str = ""
    subject: str = "(no subject)"
    date: str = ""
    labels: list[str] = []
    body: str = ""
    snippet: str = ""
    attachments: list[str] = []

    @computed_field
    @property
    def sender_email(self) -> str:
        return clean_addr(self.sender)

    @computed_field
    @property
    def sender_name(self) -> str:
        return parseaddr(self.sender)[0] or self.sender_email

    @computed_field
    @property
    def unread(self) -> bool:
        return "UNREAD" in self.labels

    @field_validator("subject", mode="before")
    @classmethod
    def _subject(cls, v):
        return v or "(no subject)"


class InboxRequest(Strict):
    max_results: int = Field(10, ge=1, le=25)
    unread_only: bool = False


class EmailTriage(Strict):
    """Structured output for inbox-reader summaries."""

    email_id: str
    category: Category
    priority: Priority
    summary: str
    needs_reply: bool
    injection_suspected: bool


class InboxItem(EmailTriage):
    """One email as reported by the agent: original fields plus triage."""

    thread_id: str
    sender: str
    to: str
    cc: str
    subject: str
    date: str
    unread: bool
    attachments: list[str]
    key_points: list[str]
    body: str = Field(description="Original body verbatim, truncated to 1500 chars")


class InboxReport(Strict):
    emails: list[InboxItem]
