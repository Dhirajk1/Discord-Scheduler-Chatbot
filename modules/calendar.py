'''
A calendar class to represent the availability of ALL users.
'''
from .scheduler import Schedule
from .utilities import Timeslot, convert_idx_time, Availability


class Calendar():
    '''
    Calendar class
    '''

    def __init__(self):
        self.calendar = {}
        self.master = {}
        self.people = 0

        for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
            self.master[day] = [0] * 24

    def reset_master(self):
        '''
        Clear data in the calendar
        '''
        for day in self.master:
            self.master[day] = [0] * 24

    def get_coverage(self, count) -> int:
        '''
        Will returnt the percentage of people available for that timeslot
        '''
        return round((count / self.people) * 100, 2)

    def add_user(self, user: str):
        '''
        Add a new user by create a schedule for them
        '''
        self.calendar[user] = Schedule()
        self.people += 1

    def usr_sched_as_str(self, user: str) -> str:
        '''
        Return the specified user's schedule as a string
        '''
        if user not in self.calendar:
            return 'No Data Found'
        return self.calendar[user].get_schedule()

    def get_avail_days(self, user: str) -> str:
        '''
        Return the days that the user has available
        '''
        if user not in self.calendar:
            return 'Input Availability'
        return self.calendar[user].days_done()

    def get_schedule(self, user: str) -> Schedule:
        '''
        Return the use's Schedule
        '''
        return self.calendar[user]

    def update_master(self):
        '''
        Update the master calendar with the current availability
        based on each individual user's schedule
        '''
        self.reset_master()
        for user in self.calendar:
            for day in self.get_schedule(user).data():
                for i, status in enumerate(self.get_schedule(user).data()[day]):
                    if status == Availability.FREE:
                        self.master[day][i] += 1

    def find_best(self) -> list[Timeslot]:
        '''
        Find the best timeslot to schedule a user
        '''
        rankings = []
        for day, status in self.master.items():
            for time, count in enumerate(status):
                if count > 0:
                    rankings.append(
                        Timeslot(day, convert_idx_time(time), count)
                    )
        rankings.sort(key=lambda t: t.count, reverse=True)
        return rankings

    def best_to_str(self) -> str:
        '''
        Transform available times into a string for output
        '''
        rankings = self.find_best()
        if not rankings:
            return 'No Available Slots'

        res = f'Respones = {self.people}\n'
        current = None
        for timeslot in rankings:
            if current != timeslot.count:
                current = timeslot.count
                res += f'\n__Slots with coverage of **{self.get_coverage(current)}%**:__\n'
                res += f'[{timeslot.to_string()}], \t'
            else:
                res += f'[{timeslot.to_string()}], \t'

        return res[:-3]

    def update(self, user, day, times):
        '''
        Update if a user's wants to change previously inputted data
        '''
        if user not in self.calendar:
            self.add_user(user)
        self.get_schedule(user).update(day, times)
        self.update_master()
