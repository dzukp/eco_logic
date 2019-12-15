from pylogic.logged_object import LoggedObject
from pylogic.timer import Ton
from pylogic.utils import Hysteresis


class Subsystem(LoggedObject):

    def __init__(self, name):
        super().__init__(name)
        self.started = False
        self.external_enable = True

    def start(self):
        if not self.started:
            self.started = True
            self.logger.info('Start')

    def stop(self):
        if self.started:
            self.started = False
            self.logger.info('Stop')

    def enable(self, en=True):
        if self.external_enable != en:
            self.external_enable = en
            self.logger.info(f'{"Enable" if self.external_enable else "Disable"}')

    def disable(self):
        self.enable(False)


class WaterSupplier(Subsystem):
    """ Pump, tank, pressure sensor, pressure relay """

    def __init__(self, name):
        super().__init__(name)
        self.pump = None
        self.tank = None
        self.ai_pressure = None
        self.hysteresis = Hysteresis(low=3.0, hi=4.0)
        self.enough_pressure = 2.0

    def process(self):
        if self.need_pump() and not self.tank.is_empty():
            self.pump.start()
        else:
            self.pump.stop()

    def need_pump(self):
        return not self.hysteresis.process(self.ai_pressure.val)

    def is_can_supply(self):
        return self.ai_pressure.val > self.enough_pressure


class TankFiller(Subsystem):
    """  """

    def __init__(self, name):
        super().__init__(name)
        self.valve = None
        self.tank = None

    def process(self):
        if self.need_fill():
            self.valve.open()
        else:
            self.valve.close()

    def need_fill(self):
        self.tank.is_want_water()


class OsmosisTankFiller(TankFiller):

    def __init__(self, name):
        super().__init__(name)
        self.pump1 = None
        self.pump2 = None
        self.valve_inlet = None
        self.di_pressure = None
        self._state = 0

    def process(self):
        # no filling
        if self._state == 0:
            self.valve_inlet.close()
            self.pump1.stop()
            self.pump2.stop()
            self.valve.close()
            if self.need_fill():
                self._state = 1
                self.logger.info('need fill osmosis tank, go to open inlet valve')
        # open inlet valve
        elif self._state == 1:
            self.valve_inlet.open()
            self.pump1.stop()
            self.pump2.stop()
            self.valve.close()
            if self.di_pressure.val:
                self.logger.info('water, go start pumps and open valve')
                self._state = 2
            if not self.need_fill():
                self.logger.info('osmosis tank is full, go stop and close all')
                self._state = 0
        # start pumps and open valve
        elif self._state == 2:
            self.valve_inlet.open()
            self.pump1.start()
            self.pump2.start()
            self.valve.open()
            if not self.di_pressure.val:
                self.logger.info('water, go start pumps and open valve')
                self._state = 0
            if not self.need_fill():
                self.logger.info('osmosis tank is full, go stop and close all')
                self._state = 0


