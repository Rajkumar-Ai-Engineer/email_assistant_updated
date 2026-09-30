from datetime import datetime

from pydantic import Field, model_validator

from .common import Strict


class CalendarRequest(Strict):
    days_ahead: int = Field(7, ge=1, le=60)
    start_date: str = ""

    @model_validator(mode="after")
    def _date(self):
        if self.start_date:
            datetime.fromisoformat(self.start_date)
        return self


class CalendarEvent(Strict):
    id: str
    title: str
    start: str
    end: str
    attendees: list[str]
    status: str


class TimeRange(Strict):
    start: datetime
    end: datetime

    @model_validator(mode="after")
    def _order(self):
        if self.end <= self.start:
            raise ValueError("end must be after start")
        return self


class FreeBusyRequest(TimeRange):
    pass


class FreeSlot(TimeRange):
    pass


class CalendarReport(Strict):
    events: list[CalendarEvent]
