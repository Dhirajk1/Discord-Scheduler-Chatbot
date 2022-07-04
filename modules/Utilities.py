'''
A series of utility functions for the application.
'''
from dataclasses import dataclass
from enum import Enum


@dataclass
class Timeslot:
    '''
    A class to represent a timeslot.
    '''
    day: str
    time: str
    count: int

    def to_string(self) -> str:
        '''
        Returns a string representation of the timeslot.
        '''
        return f'{self.day} from {self.time}'


class Availability(Enum):
    '''
    Enum to represent the availability of a timeslot.
    '''
    BUSY = 0
    FREE = 1


def convert_idx_time(start_idx: int) -> str:
    '''
    Convering the index of a timeslot to a string representation.
    '''
    end_idx = start_idx + 1 if start_idx != 23 else 0
    start_str = f'{start_idx}:00' if start_idx > 10 else f'0{start_idx}:00'
    end_str = f'{end_idx}:00' if end_idx > 10 else f'0{end_idx}:00'
    return f'{start_str} to {end_str}'
