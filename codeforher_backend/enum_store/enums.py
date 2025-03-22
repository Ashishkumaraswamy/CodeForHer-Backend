from enum import StrEnum, auto


class SOSAlertMessageStatus(StrEnum):
    SENT = auto()
    FAILED = auto()
    PENDING = auto()


class TripStatus(StrEnum):
    ONGOING = auto()
    COMPLETED = auto()
    CANCELLED = auto()

class RankByCategory(StrEnum):
    POPULAR =auto()
    DISTANCE =auto()