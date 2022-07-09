"""
A series of utility functions for the application.
"""
from dataclasses import dataclass
from enum import Enum
import datetime
from datetime import timedelta
from pytz import timezone


@dataclass
class Timeslot:
    """
    A class to represent a timeslot.
    """

    day: str
    time: str
    count: int

    def to_string(self) -> str:
        """
        Returns a string representation of the timeslot.
        """
        return f"{self.day} from {self.time}"

    def convert_datetime(self) -> datetime:
        """
        Convering the index of a timeslot to a datetime representation.
        """
        days_to_int = {
            "Monday": 0,
            "Tuesday": 1,
            "Wednesday": 2,
            "Thursday": 3,
            "Friday": 4,
            "Saturday": 5,
            "Sunday": 6,
        }
        now = datetime.datetime.now(timezone("US/Eastern"))
        needed_day = days_to_int[self.day]
        time = (now + timedelta(days=abs(now.weekday() - needed_day))).replace(
            hour=int(self.time[:2]), minute=0, second=0
        )
        return time if time > now else time + timedelta(days=7)


class Availability(Enum):
    """
    Enum to represent the availability of a timeslot.
    """

    BUSY = 0
    FREE = 1


def convert_idx_time(start_idx: int) -> str:
    """
    Convering the index of a timeslot to a string representation.
    """
    end_idx = start_idx + 1 if start_idx != 23 else 0
    start_str = f"{start_idx}:00" if start_idx > 10 else f"0{start_idx}:00"
    end_str = f"{end_idx}:00" if end_idx > 10 else f"0{end_idx}:00"
    return f"{start_str} to {end_str}"
