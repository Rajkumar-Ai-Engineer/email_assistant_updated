from email.utils import parseaddr

from pydantic import BaseModel, ConfigDict


class Strict(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True, populate_by_name=True)


def clean_addr(v: str) -> str:
    return parseaddr(v)[1].lower()
