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


class FcSimulator(IoObject):

    def __init__(self, *args):
        super(FcSimulator, self).__init__(*args)
        self.cmd_start_mask = 0xC400
        self.cmd_reset_mask = 0xF000
        self.status_run_mask = 0x0400
        self.status_stop_mask = 0x0000
        self.ai_cmd = InChannel(0)
        self.ai_freq = InChannel(0)
        self.ao_status = OutChannel(0)
        self.ao_freq = OutChannel(0)
        self.ao_pressure = OutChannel(0)

    def process(self):
        if (self.ai_cmd.val & self.cmd_start_mask) == self.cmd_start_mask:
            self.ao_status.val = self.status_run_mask
        elif (self.ai_cmd.val & self.cmd_reset_mask) == self.cmd_reset_mask:
            self.ao_status.val = 0
        else:
            self.ao_status.val = 0
        self.ao_freq.val = self.ai_freq.val if self.ao_status.val == self.status_run_mask else 0.0
        self.ao_pressure.val = self.ao_freq.val * 3.623 / 100

