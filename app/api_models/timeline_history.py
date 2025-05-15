import enum
from pydantic import BaseModel
from typing import List, Optional


class TimelineHistoryCreateModel(BaseModel):
    title: str
    description: str
    timeline_id: str
    event_date: Optional[str] = None
    categories: Optional[List[str]]


class TimelineHistoryUpdateModel(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    event_date: Optional[str] = None
    categories: Optional[List[str]]


class HistoryStatus(enum.Enum):
    POSTED = "posted"
    REVIEWING = "reviewing"
    PUBLISHED = "published"
    DELETED = "deleted"
