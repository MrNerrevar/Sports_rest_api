from enum import Enum, auto


class EventType(Enum):
    Preplay = "PREPLAY"
    Inplay = "INPLAY"


class EventStatus(Enum):
    Pending = "PENDING"
    Started = "STARTED"
    Ended = "ENDED"
    Cancelled = "CANCELLED"


class SelectionOutcome(Enum):
    Unsettled = "UNSETTLED"
    Void = "VOID"
    Lose = "LOSE"
    Win = "WIN"
