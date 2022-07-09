"""
Class representing a schduler.
This will encapulsate teh avialble for ONE user
"""
from typing import List
from .utilities import Availability, convert_idx_time


class Schedule:
    """
    Class for scheduling a user
    """

    def __init__(self):
        self.schedule = {}
        for day in [
            "Monday",
            "Tuesday",
            "Wednesay",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]:
            self.schedule[day] = [Availability.BUSY] * 24

    def data(self) -> dict[str, Availability]:
        """
        Return schedule data as a map
        """
        return self.schedule

    def reset(self, day):
        """
        Clears the schedule for the day (sets every time to busy)
        """
        self.schedule[day] = [Availability.BUSY] * 24

    def days_done(self) -> str:
        """
        Will output a string of the days that the user has completed
        """
        res = "Days With At Least One Available Slot:\n"
        for day, status in self.schedule.items():
            if Availability.FREE in status:
                res += f" | {day}: ✅ | "
        return res

    def update(self, day: str, times: List[str]):
        """
        Will update the schedule with the given times
        that the user is available for
        """
        self.reset(day)
        for time in times:
            self.schedule[day][int(time)] = Availability.FREE

    def get_schedule(self) -> str:
        """
        Will return the schedule as a string
        """
        res = ""
        for day, status in self.schedule.items():
            if Availability.FREE in status:
                res += f"Day: {day} \n"
                for time, avail in enumerate(status):
                    if avail == Availability.FREE:
                        res += f"[{convert_idx_time(time)}], "
                res += "\n"

        return res if res else "No Times Found"
