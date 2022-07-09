"""
Helper functions to make selectors in the scheduler bot.
"""
from discord.ui import Select

from modules.utilities import Timeslot


def make_day_selector():
    """
    Creating a selector for each day of the weeks (Monday to Sunday)
    """
    selector = Select(
        min_values=1,
        max_values=1,
        placeholder="Pick Day",
    )

    for day in [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]:
        selector.add_option(label=day)

    return selector


def make_time_selector():
    """
    Creating a selector for each hour increment(00:00 to 23:00)
    """
    selector = Select(
        max_values=24,
        placeholder="Pick Time",
    )

    for i in range(24):
        start_str = str(i)
        if len(start_str) < 2:
            start_str = "0" + start_str
        end_str = str(i + 1) if i != 23 else "0"
        if len(end_str) < 2:
            end_str = "0" + end_str
        selector.add_option(label=f"{start_str}:00 to {end_str}:00", value=i)

    return selector


def make_event_selector(timeslots: list[Timeslot]):
    """
    Generating a selector for each timeslot to make an event.
    """
    selector = Select(
        min_values=1,
        max_values=1,
        placeholder="Schedule your event",
    )
    for i, timeslot in enumerate(timeslots):
        selector.add_option(label=timeslot.to_string(), value=i)

    return selector
