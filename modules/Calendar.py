from modules.Scheduler import Schedule, Timeslot, convert_idx_time, Availability

class Calendar():
  def __init__(self):
    self.calendar = {}
    self.master = {}
    self.people = 0

    for day in ['Monday', "Tuesday", 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
      self.master[day] = [0] * 24

  def reset_master(self):
    for day in self.master:
      self.master[day] = [0] * 24

  def get_coverage(self, count) -> int:
    return round((count / self.people) * 100, 2)

  def add_user(self, user: str):
    self.calendar[user] = Schedule()
    self.people += 1

  def usr_sched_as_str(self, user:str) -> str:
    if user not in self.calendar: return 'No Data Found'
    return self.calendar[user].get_schedule()

  def get_avail_days(self, user:str) ->str:
    if user not in self.calendar: return "Input Availability"
    return self.calendar[user].days_done()

  def get_schedule(self, user: str) -> Schedule:
    return self.calendar[user]

  def update_master(self):
    self.reset_master()
    for user in self.calendar:
      for day in self.get_schedule(user).data():
        for i, status in enumerate(self.get_schedule(user).data()[day]):
          if status == Availability.FREE:
            self.master[day][i] += 1

  def find_best(self) -> str:
    if self.people == 0: return 'No Responses'

    rankings = []
    for day, status in self.master.items():
      for time, count in enumerate(status):
        if count > 0:
          rankings.append(
            Timeslot(day, convert_idx_time(time), count)
          )

    if not rankings: return 'No Available Slots'

    rankings.sort(key=lambda t: t.count, reverse=True)

    res = f"Respones = {self.people}\n"
    current = None
    for timeslot in rankings:
      if current != timeslot.count:
        current = timeslot.count
        res += f"\n__Slots with coverage of **{self.get_coverage(current)}%**:__\n"
        res += f"[{timeslot.to_string()}], \t" 
      else: 
        res += f"[{timeslot.to_string()}], \t"

    return res[:-3]

  def update(self, user, day, times):
    if user not in self.calendar: 
      self.add_user(user)
    self.get_schedule(user).update(day, times)
    self.update_master()