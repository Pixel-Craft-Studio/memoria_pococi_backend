import enum
from pydantic import BaseModel
from typing import Optional


class TimelineHistoryCreateModel(BaseModel):
    title: str
    description: str
    timeline_id: int
    event_date: Optional[str] = None


class TimelineHistoryUpdateModel(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    event_date: Optional[str] = None


class HistoryStatus(enum.Enum):
    POSTED = "posted"
    REVIEWING = "reviewing"
    PUBLISHED = "published"
    DELETED = "deleted"
