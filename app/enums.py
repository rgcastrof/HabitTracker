from enum import Enum

class Frequence(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"

class Status(str, Enum):
    FINISHED = "completed"
    PARTIALLY = "partially"
    UNFINISHED = "unfinished"
