from pylogic.io_object import IoObject
from pylogic.channel import InChannel, OutChannel

import time


class TankSimulator(IoObject):

    def __init__(self, *args):
        super().__init__(*args)
        self.level = 0.0
        self.speed = 0.0
        self.last_time = time.time()
        self.do_low = OutChannel(False)
        self.do_mid = OutChannel(False)
        self.do_hi = OutChannel(False)

    def process(self):
        time_ = time.time()
        self.level = max(0.0, min(100.0, (time_ - self.last_time) * self.speed + self.level))
        self.do_low.val = self.level > 10.0
        self.do_mid.val = self.level > 60.0
        self.do_hi.val = self.level > 90.0
        self.last_time = time_

    def add_speed(self, val):
        self.speed += val

    def reset_speed(self):
        self.speed = 0.0
