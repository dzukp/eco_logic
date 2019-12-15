from pylogic.io_object import IoObject
from pylogic.channel import InChannel, OutChannel
from pylogic.utils import Hysteresis


class Nofrost(IoObject):
    """ Antifrost system """

    def __init__(self, *args):
        super().__init__(*args)
        self.ai_temp_1 = InChannel(0.0)
        self.ai_temp_2 = InChannel(0.0)
        self.valve_nc = None
        self.valve_no = None
        self.open_temp = 1.0
        self.close_temp = 2.0
        self.hysteresis = Hysteresis(self.open_temp, self.close_temp)
        self.started = False

    def process(self):
        self.valve_no.close()
        if self.started:
            min_temp = min(self.ai_temp_1.val, self.ai_temp_2.val)
            if self.hysteresis.process(min_temp):
                self.valve_nc.close()
            else:
                self.valve_nc.open()
            if self.hysteresis.isSwitchToOn():
                self.logger.info('Hi temperature')
            elif self.hysteresis.isSwitchToOff():
                self.logger.info('Low temperature')

    def load(self):
        super().load()
        self.hysteresis.hi = self.close_temp
        self.hysteresis.low = self.open_temp

    def start(self):
        if not self.started:
            self.started = True
            self.logger.info('Start')

    def stop(self):
        if self.started:
            self.started = False
            self.logger.info('Stop')
