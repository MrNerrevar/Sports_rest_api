from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enums import EventType, EventStatus, SelectionOutcome


@dataclass
class Sport:
    Name: str
    Slug: str = None
    Active: bool = None


@dataclass
class Event:
    Name: str
    Slug: str
    Active: bool
    Type: EventType
    Sport: str
    Status: EventStatus
    ScheduledStart: datetime
    ActualStart: datetime
    Logos: str


@dataclass
class Selection:
    Name: str
    Event: str
    Price: Decimal
    Active: bool
    Outcome: SelectionOutcome
