from pylogic.io_object import IoObject
from pylogic.logged_object import LoggedObject
from pylogic.modbus_supervisor import ModbusDataObject
from pylogic.timer import Timer, Ton
from pylogic.utils import Hysteresis
from simple_pid import PID
from pylogic.channel import InChannel

import struct


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
        # self.di_pressure = None
        self.enough_pressure = 2.0
        self.pump_on_press = 3.0
        self.pump_off_press = 4.0
        self.hysteresis = Hysteresis(low=self.pump_on_press, hi=self.pump_off_press)
        self.last_can_supply = False

    def process(self):
        if self.started and self.external_enable and self.need_pump() and not self.tank.is_empty():
            self.pump.start()
        else:
            self.pump.stop()
        is_can_supply = self.is_can_supply()
        if self.last_can_supply != is_can_supply:
            self.last_can_supply = is_can_supply
            self.logger.debug('Can supply' if is_can_supply else 'Can\'t supply')

    def need_pump(self):
        self.hysteresis.low = self.pump_on_press
        self.hysteresis.hi = self.pump_off_press
        return not self.hysteresis.process(self.ai_pressure.val)

    def is_can_supply(self):
        return self.ai_pressure.val > self.enough_pressure or self.enough_pressure < 0.1


class TwoPumpWaterSupplier(WaterSupplier):

    def __init__(self, name):
        super(TwoPumpWaterSupplier, self).__init__(name)
        self.pump2 = None
        self.hysteresis2 = Hysteresis(low=self.pump_on_press, hi=self.pump_off_press)

    def process(self):
        super(TwoPumpWaterSupplier, self).process()
        need_extra_pump = self.need_pump_2()
        if self.started and self.external_enable and need_extra_pump and not self.tank.is_empty():
            self.pump2.start()
        else:
            self.pump2.stop()

    def need_pump_2(self):
        self.hysteresis2.low = self.pump_on_press + (self.pump_off_press - self.pump_on_press) * 0.5
        self.hysteresis2.hi = self.pump_off_press
        return not self.hysteresis2.process(self.ai_pressure.val)


class TankFiller(Subsystem):
    """  """

    def __init__(self, name):
        super().__init__(name)
        self.valve = None
        self.tank = None

    def process(self):
        if self.started and self.external_enable and self.need_fill():
            self.valve.open()
        else:
            self.valve.close()

    def need_fill(self):
        return self.tank.is_want_water()


class B1TankFiller(Subsystem):

    def __init__(self, name):
        super().__init__(name)
        self.valve_1 = None
        self.valve_2 = None
        self.pump = None
        self.source_tank = None
        self.tank = None
        self.no_v1_ton = Ton()
        self.no_v1_ton.set_timeout(15)

    def process(self):
        valve_1 = False
        valve_2 = False
        pump = False
        if self.started and self.external_enable:
            if self.no_v1_ton.process(run=not self.tank.is_full()):
                if not self.source_tank or not self.source_tank.is_empty():
                    pump = True
                else:
                    valve_1 = True
            if self.tank.is_want_water():
                valve_2 = True
                valve_1 = True
                pump = True
        if valve_1:
            self.valve_1.open()
        else:
            self.valve_1.close()
        if valve_2:
            self.valve_2.open()
        else:
            self.valve_2.close()
        if pump:
            self.pump.start()
        else:
            self.pump.stop()


class PumpTankFiller(TankFiller):
    """  """

    def __init__(self, name):
        super().__init__(name)
        self.pump = None
        self.pump2 = None
        self.di_press = None
        self.do_no_press_signal = None
        self.no_pump_timer = Timer()
        self.wait_after_no_press_timer = Timer()
        self.no_press_timer = Timer()
        self.mid_level_ton = Ton()
        self.pump_state = 0

    def process(self):
        pump_start = False
        if self.started and self.external_enable and not self.tank.di_hi_level.val and \
                not self.mid_level_ton.process(self.tank.di_mid_level.val, 10.0):
            self.no_pump_timer.start(5.0)
            pump_start = True
            self.valve.open()
        elif self.started and self.external_enable and self.need_fill():
            self.no_pump_timer.start(5.0)
            if self.no_pump_timer.is_end():
                pump_start = True
            self.valve.close()
        else:
            self.valve.close()
            self.no_pump_timer.reset()
            self.wait_after_no_press_timer.reset()

        self.pump_process(pump_start)

        if self.do_no_press_signal is not None:
            self.do_no_press_signal.val = self.pump_state == -1 and self.wait_after_no_press_timer.elapsed() < 10.0

    def pump_process(self, start):
        if not start:
            self.pump_state = 0
        if self.pump_state == -1:
            # Ожидание после отключения из-за давления
            self.pump.stop()
            if self.pump2:
                self.pump2.stop()
            self.wait_after_no_press_timer.start(30.0)
            if self.wait_after_no_press_timer.is_end():
                self.pump_state = 0
        elif self.pump_state == 0:
            # Бездействие
            self.pump.stop()
            if self.pump2:
                self.pump2.stop()
            if start:
                self.pump_state = 1
                self.no_press_timer.reset()
        elif self.pump_state == 1:
            # Работа
            self.pump.start()
            self.no_press_timer.start(5.0)
            if not self.di_press or self.di_press.val:
                self.no_press_timer.restart()
                if self.pump2:
                    self.pump2.start()
            elif self.no_press_timer.is_end():
                self.logger.info('no pressure after pump start')
                self.wait_after_no_press_timer.reset()
                self.pump_state = -1


class PumpsTankFiller(Subsystem):
    """  """

    def __init__(self, name):
        super().__init__(name)
        self.pumps = []
        self.valves = []
        self.tank = None
        self.source_tank = None
        self.di_press = None

    def process(self):
        no_source_water = self.source_tank and self.source_tank.is_empty()
        if self.started and self.external_enable and self.need_fill() and not no_source_water:
            for pump in self.pumps:
                if not self.di_press or self.di_press.val:
                    pump.start()
                else:
                    pump.stop()
            for valve in self.valves:
                valve.open()
        else:
            for pump in self.pumps:
                pump.stop()
            for valve in self.valves:
                valve.close()

    def need_fill(self):
        return self.tank.is_want_water()


class OsmosisTankFiller(TankFiller):

    def __init__(self, name):
        super().__init__(name)
        self.valve_inlet = None
        self.di_pressure = None
        self.timer = Timer()
        self.pid_pump = None
        self._state = 0

    def process(self):
        if not self.started or not self.external_enable:
            self.set_state(0)
        # no filling
        if self._state == 0:
            self.valve_inlet.close()
            self.pid_pump.stop()
            self.valve.close()
            if self.started and self.external_enable and self.need_fill():
                self.set_state(1)
                self.logger.info('need fill osmosis tank, go to open inlet valve')
        # open inlet valve
        elif self._state == 1:
            self.valve_inlet.open()
            self.pid_pump.stop()
            self.valve.close()
            self.timer.start(5.0)
            # if self.di_pressure.val and self.timer.is_end():
            if self.timer.is_end():
                self.logger.info('water, go start pumps and open valve')
                self.set_state(2)
            if not self.need_fill():
                self.logger.info('osmosis tank is full, stop osmosis filler')
                self.set_state(0)
        # start 1 pump and open valve
        elif self._state == 2:
            self.valve_inlet.open()
            self.pid_pump.start()
            self.valve.open()
            self.timer.start(2.0)
            if self.timer.is_end():
                self.set_state(3)
                self.logger.info('timer end, start os2')
            # if not self.di_pressure.val:
            #     self.logger.info('no pressure, stop osmosis filler')
            #     self.set_state(0)
            if not self.need_fill():
                self.logger.info('osmosis tank is full, stop osmosis filler')
                self.set_state(0)
        # start 2 pump
        elif self._state == 3:
            self.valve_inlet.open()
            self.pid_pump.start()
            self.valve.open()
            # if not self.di_pressure.val:
            #     self.logger.info('no pressure, stop osmosis filler')
            #     self.set_state(0)
            if not self.need_fill():
                self.logger.info('osmosis tank is full, stop osmosis filler')
                self.set_state(0)

    def set_state(self, new_state):
        self._state = new_state
        self.timer.reset()


class PidEngine(IoObject, ModbusDataObject):

    _save_attrs = ('set_point', 'pid_k', 'pid_i', 'pid_d', 'freq_limits')

    def __init__(self, *args, **kwargs):
        super(PidEngine, self).__init__(*args, **kwargs)
        self.started = False
        self.fc = None
        self.ai_sensor = InChannel(0.0)
        self.set_point = 0.0
        self.pid_k = 1.0
        self.pid_i = 2.0
        self.pid_d = 0.0
        self.freq_limits = [20.0, 50.0]
        self.pid = PID(sample_time=0.5)
        self.pid.output_limits = tuple(self.freq_limits)
        self.pid.tunings = (self.pid_k, self.pid_i, self.pid_d)
        self.min_freq_timer = Timer()
        self.mb_cells_idx = None

    def start(self):
        if not self.started:
            self.started = True
            self.logger.info('Start')

    def stop(self):
        if self.started:
            self.started = False
            self.logger.info('Stop')

    def process(self):
        self.pid.tunings = (self.pid_k, self.pid_i, self.pid_d)
        self.pid.setpoint = self.set_point
        self.pid.output_limits = tuple(self.freq_limits)
        if self.started:
            frequency = self.pid(self.ai_sensor.val)
            self.fc.set_frequency(frequency, no_log=True)
            if frequency <= self.pid.output_limits[0] + 0.1:
                self.min_freq_timer.start(timeout=30.0)
            else:
                self.min_freq_timer.restart()
            if self.min_freq_timer.is_end():
                self.fc.stop()
            else:
                self.fc.start()
        else:
            self.fc.stop()
            self.fc.set_frequency(0)
            self.pid.reset()
            self.min_freq_timer.restart()

    def mb_cells(self):
        return [self.mb_cells_idx, self.mb_cells_idx + 1]

    def mb_input(self, start_addr, data):
        if self.mb_cells_idx is not None:
            float_data = struct.unpack('ffff',
                                       struct.pack('HHHHHHHH',
                                                   *tuple(data[self.mb_cells_idx + 3: self.mb_cells_idx + 11])))
            if self.pid_k != float_data[0]:
                self.pid_k = float_data[0]
                self.logger.info(f'Set Pid K = {self.pid_k}')
                self.save()
            if self.pid_i != float_data[1]:
                self.pid_i = float_data[1]
                self.logger.info(f'Set Pid I = {self.pid_i}')
                self.save()
            if self.pid_d != float_data[2]:
                self.pid_d = float_data[2]
                self.logger.info(f'Set Pid K = {self.pid_d}')
                self.save()
            if self.set_point != float_data[3]:
                self.set_point = float_data[3]
                self.logger.info(f'Set pressure task = {self.set_point}')
                self.save()

    def mb_output(self, start_addr):
        if self.mb_cells_idx is not None:
            status = int(self.started) * (1 << 0) | \
                     0xD000
            float_data = struct.pack('fffff', self.ai_sensor.val, self.pid_k, self.pid_i, self.pid_d, self.set_point)
            float_data = struct.unpack('HHHHHHHHHH', float_data)
            return {
                self.mb_cells_idx - start_addr: status,
                self.mb_cells_idx - start_addr + 1: float_data[0],
                self.mb_cells_idx - start_addr + 2: float_data[1],
                self.mb_cells_idx - start_addr + 3: float_data[2],
                self.mb_cells_idx - start_addr + 4: float_data[3],
                self.mb_cells_idx - start_addr + 5: float_data[4],
                self.mb_cells_idx - start_addr + 6: float_data[5],
                self.mb_cells_idx - start_addr + 7: float_data[6],
                self.mb_cells_idx - start_addr + 8: float_data[7],
                self.mb_cells_idx - start_addr + 9: float_data[8],
                self.mb_cells_idx - start_addr + 10: float_data[9],
            }
        else:
            return {}
