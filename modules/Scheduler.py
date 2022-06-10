from modules.Utilities import Availability, convert_idx_time
from typing import List

class Schedule():
  def __init__(self):
    self.schedule = {}
    for day in ['Monday', "Tuesday", 'Wednesay', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
      self.schedule[day] = [Availability.BUSY] * 24

  def data(self):
    return self.schedule

  def reset(self, day):
      self.schedule[day] = [Availability.BUSY] * 24

  def days_done(self) -> str:
    res = "Days With At Least One Available Slot:\n"
    for day, status in self.schedule.items():
      if Availability.FREE in status:
        res += f" | {day}: ✅ | "
    return res

  def update(self, day: str, times: List[str]):
    self.reset(day)
    for time in times:
      self.schedule[day][int(time)] = Availability.FREE

  def get_schedule(self) -> str:
    res = ""
    for day, status in self.schedule.items():
      if Availability.FREE in status:
        res += f"Day: {day} \n"
        for time, avail in enumerate(status):
          if avail == Availability.FREE:
            res += f"[{convert_idx_time(time)}], "
        res += '\n'

    return res if res else "No Times Found"

  def print(self):
    for day in self.schedule:
      print(f'{day}:\n self.schedule[day]\n')


