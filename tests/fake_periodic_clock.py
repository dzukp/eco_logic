from pylogic.timer import periodic_clocks


class MyPeriodicClock:
    def __init__(self):
        self.__time = 0.0

    def time(self):
        return self.__time

    def set_time(self, t):
        self.__time = t


clock = MyPeriodicClock()
periodic_clocks['default'] = clock
