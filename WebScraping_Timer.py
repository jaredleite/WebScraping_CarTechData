from time import sleep
import datetime
from random import choice


class Timer:
    """
    Emulate a human user for webscraping

    Example:
    This code will make N short breaks (T seconds) and then one long break (M minutes),
    then it will repeate the cicle

    N = random between take_long_time_min and take_long_time_max
    T = random between short_break_min and short_break_max
    M = random between short_break_min and short_break_max
    """

    def __init__(self) -> None:

        self.count = 0
        self.take_long_time_max = 20
        self.take_long_time_min = 10
        self.long_break_max = 180  # min
        self.long_break_min = 60  # min
        self.short_break_max = 180  # sec
        self.short_break_min = 60  # sec
        self.take_long_time = self.take_long_time_min

    def take_a_break(self):
        if(self.count > self.take_long_time):
            self.take_long_time = choice(
                range(self.take_long_time_min, self.take_long_time_max))
            self.count = 0
            self.long_break()
        else:
            self.count = self.count + 1
            self.short_break()
        #self.count = self.count + 1
        return

    def long_break(self):
        print('Long break')
        print(f'Start at {datetime.datetime.now()}')
        sleep(choice(range(self.long_break_min, self.long_break_max))*60)
        print(f'End at {datetime.datetime.now()}\n')
        return

    def short_break(self):
        print('Short break')
        print(f'Start at {datetime.datetime.now()}')
        sleep(choice(range(self.short_break_min, self.short_break_max)))
        print(f'End at {datetime.datetime.now()}\n')
        return
