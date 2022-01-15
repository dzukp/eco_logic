import random

from pylogic.io_object import IoObject
from pylogic.channel import InChannel, OutChannel
from pylogic.timer import Ton, Timer


class TopSimulator(IoObject):

    def __init__(self, *args):
        super().__init__(*args)
        self.di_valve_b1 = InChannel(False)
        self.b1 = None
        self.di_n1 = InChannel(False)
        self.ao_p1 = OutChannel(0.0)
        self.ao_p2 = OutChannel(0.0)
        self.do_press1 = OutChannel(False)
        self.di_water_os = InChannel(False)
        self.do_press2 = OutChannel(False)
        self.di_os1 = InChannel(False)
        self.di_os2 = InChannel(False)
        self.di_valve_b2 = InChannel(False)
        self.b2 = None
        self.di_n2 = InChannel(False)
        self.ao_p3 = OutChannel(0.0)
        self.do_press3 = OutChannel(False)
        self.di_n3 = InChannel(False)
        self.do_press4 = OutChannel(False)
        self.n3_timer = Timer()

    def process(self):
        # Water
        self.b1.reset_speed()
        if self.di_valve_b1.val:
            self.b1.add_speed(2.0)
        if self.di_n1.val:
            self.ao_p1.val = min(6.0, self.ao_p1.val + 0.027) + get_about_0_rand(0.01)
        else:
            self.ao_p1.val = max(0.0, self.ao_p1.val - 0.027) + random.random() * 0.01
        self.ao_p2.val = max(0.0, self.ao_p1.val - 0.3 + get_about_0_rand(0.3))
        self.do_press1.val = self.ao_p1.val > 0.5
        if self.di_n1.val:
            self.b1.add_speed(-1.0)
        # Osmosis
        self.do_press2.val = self.di_water_os.val and self.ao_p2.val > 1.0
        self.b2.reset_speed()
        if self.di_valve_b2.val:
            if self.do_press2.val:
                if self.di_os1.val:
                    self.b2.add_speed(1.0)
                if self.di_os2.val:
                    self.b2.add_speed(1.0)
        if self.di_n2.val:
            self.b2.add_speed(-1.0)
        if self.di_n2.val:
            self.ao_p3.val = min(6.0, self.ao_p3.val + 0.027) + get_about_0_rand(0.01)
        else:
            self.ao_p3.val = max(0.0, self.ao_p3.val - 0.027) + random.random() * 0.01
        self.do_press3.val = self.ao_p3.val > 0.5

        if self.di_n3.val:
            self.n3_timer.start(60)
        else:
            self.n3_timer.reset()
        if self.n3_timer.elapsed() > 20.0:
            self.do_press4.val = False
        elif self.n3_timer.elapsed() > 2.0:
            self.do_press4.val = True

        self.ao_p1.val = 3.1
        self.ao_p2.val = 3.3
        self.ao_p3.val = 3.8



def get_about_0_rand(range_):
    return (random.random() - 0.5) * range_
