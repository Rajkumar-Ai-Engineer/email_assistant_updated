from pydantic import Field

from .common import Strict


class SearchRequest(Strict):
    query: str = Field(min_length=1, max_length=300)
    max_results: int = Field(10, ge=1, le=25)


class Evidence(Strict):
    email_id: str
    subject: str
    sender: str
    date: str
    quote: str


class SearchAnswer(Strict):
    """Answer that must cite the emails it relies on."""

    answer: str
    evidence: list[Evidence] = Field(min_length=1)
