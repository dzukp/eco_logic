import time

from pylogic.io_object import IoObject
from pylogic.channel import InChannel
from pylogic.modbus_supervisor import ModbusDataObject
from pylogic.timer import Ton

from post_function import SimplePostFunctionSteps, PostIntensiveSteps
from utils import floats_to_modbus_cells
from func_names import FuncNames


class Post(IoObject, ModbusDataObject):

    _save_attrs = ('func_frequencies', 'pressure_timeout', 'min_pressure', 'pump_on_timeout', 'valve_off_timeout',
                   'disabled_funcs')

    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.ai_pressure = InChannel(0.0)

        # self.ai_pressure.set_trans(simulate_pressure)

        self.di_flow = InChannel(False)
        self.valve_foam = None
        self.valve_wax = None
        self.valve_shampoo = None
        self.valve_cold_water = None
        self.valve_hot_water = None
        self.valve_osmos = None
        self.valve_intensive = None
        self.valve_out_water = None
        self.valve_out_foam = None
        self.valve_hoover = None
        self.pump = None
        self.current_func = FuncNames.STOP
        self.func_number = len(FuncNames.all_funcs())
        self.func_frequencies = {
            FuncNames.FOAM: 25.0,
            FuncNames.SHAMPOO: 40.0,
            FuncNames.WAX: 40.0,
            FuncNames.HOT_WATER: 40.0,
            FuncNames.COLD_WATER: 40.0,
            FuncNames.OSMOSIS: 40.0,
        }
        self.pump_on_timeout = 1.0
        self.valve_off_timeout = 1.0
        self.hi_press_valve_off_timeout = 2.0
        self.pressure_timeout = 5.0
        self.pressure_timer = Ton()
        self.min_pressure = 10.0
        self.alarm_reset_timeout = 10.0
        self.alarm_reset_timer = Ton()
        self.alarm = False
        self.mb_cells_idx = None
        self.func_steps = dict([(name, SimplePostFunctionSteps(f'{name}_steps'))
                                for name in FuncNames.all_funcs() if name not in (FuncNames.STOP,)])
        self.func_steps[FuncNames.INTENSIVE] = PostIntensiveSteps('intensive_steps')
        self.func_steps[FuncNames.HOOVER] = PostIntensiveSteps('hoover_steps')
        self.disabled_funcs = []

    def init(self):
        config = {'pump_on_timeout': self.pump_on_timeout, 'valve_off_timeout': self.valve_off_timeout,
                  'hi_press_valve_off_timeout': self.hi_press_valve_off_timeout}
        valves = {
            FuncNames.FOAM: self.valve_foam,
            FuncNames.SHAMPOO: self.valve_shampoo,
            FuncNames.WAX: self.valve_wax,
            FuncNames.HOT_WATER: self.valve_hot_water,
            FuncNames.COLD_WATER: self.valve_cold_water,
            FuncNames.OSMOSIS: self.valve_osmos,
            FuncNames.INTENSIVE: self.valve_intensive,
            FuncNames.HOOVER: self.valve_hoover,
        }
        for func_name, step in self.func_steps.items():
            step.valve = valves[func_name]
            if func_name not in (FuncNames.INTENSIVE, FuncNames.HOOVER):
                step.set_config(config)

        self.pump.reset()

    def process(self):
        for func_name, step in self.func_steps.items():
            if func_name == self.current_func:
                if not step.is_active():
                    step.start()
            else:
                step.stop()
        pump = False
        freq = 0.0
        water_out_valve = False
        foam_out_valve = False
        for func_name, step in self.func_steps.items():
            step.process()
            if step.pump:
                pump = True
                try:
                    freq = self.func_frequencies[func_name]
                except KeyError:
                    self.logger.error(f'No frequency task for function `{func_name}`')
            if step.out_valve:
                if func_name == FuncNames.FOAM:
                    foam_out_valve = True
                else:
                    water_out_valve = True
        if pump:
            self.pump.start()
            self.pump.set_frequency(freq)
        else:
            self.pump.stop()
            self.pump.set_frequency(0.0)
        if foam_out_valve:
            self.valve_out_foam.open()
        else:
            self.valve_out_foam.close()
        if water_out_valve:
            self.valve_out_water.open()
        else:
            self.valve_out_water.close()
        no_pressure = self.pressure_timer.process(run=self.pump.is_run and self.ai_pressure.val < self.min_pressure,
                                           timeout=self.pressure_timeout)
        if not self.alarm:
            if self.pump.is_alarm_state():
                self.set_alarm()
                self.logger.info('Set alarm because pump alarm')
            if no_pressure:
                self.set_alarm()
                self.logger.info(f'Set alarm because no pressure ({self.ai_pressure.val})')
        # Alarm auto reset by timeout
        if self.alarm_reset_timer.process(run=self.alarm, timeout=self.alarm_reset_timeout):
            self.logger.debug('Alarm reset by time')
            self.reset_alarm()

    def set_function(self, func_name):
        if not self.alarm and func_name in FuncNames.all_funcs() and self.is_func_allowed(func_name):
            if self.current_func != func_name:
                self.logger.debug(f'New function {func_name}')
            self.current_func = func_name
        else:
            self.current_func = FuncNames.STOP
        self.func_number = FuncNames.all_funcs().index(self.current_func)
        return self.current_func == func_name

    def set_alarm(self):
        self.alarm = True
        self.current_func = FuncNames.STOP

    def reset_alarm(self):
        self.alarm = False
        self.logger.info('Reset alarm')

    def set_func_pump_frequency(self, func_name, task):
        if func_name in self.func_frequencies:
            if self.func_frequencies[func_name] != float(task):
                self.func_frequencies[func_name] = float(task)
                self.logger.info(f'Set pump frequency for function `{func_name}` = {task}')
                self.save()

    def set_pump_on_timeout(self, timeout):
        if self.pump_on_timeout != timeout:
            self.pump_on_timeout = timeout
            self.logger.info(f'Set pump on timeout {timeout}s')
            self.save()

    def set_valve_off_timeout(self, timeout):
        if self.valve_off_timeout != timeout:
            self.valve_off_timeout = timeout
            self.logger.info(f'Set value off timeout {timeout}s')
            self.save()

    def set_hi_press_valve_off_timeout(self, timeout):
        if self.hi_press_valve_off_timeout != timeout:
            self.hi_press_valve_off_timeout = timeout
            self.logger.info(f'Set hi pressure value off timeout {timeout}s')
            self.save()

    def is_func_allowed(self, func_name):
        return func_name not in self.disabled_funcs

    def is_need_hoover(self):
        return self.current_func == FuncNames.HOOVER

    def mb_cells(self):
        return self.mb_output(0).keys()

    def mb_input(self, start_addr, data):
        if self.mb_cells_idx is not None:
            cmd = data[self.mb_cells_idx - start_addr]
            if cmd & 0x0001:
                self.reset_alarm()

    def mb_output(self, start_addr):
        if self.mb_cells_idx is not None:
            status = int(self.alarm) * (1 << 0)
            p1, p2 = floats_to_modbus_cells((self.ai_pressure.val,))
            return {
                self.mb_cells_idx - start_addr: 0xFF00,
                self.mb_cells_idx - start_addr + 1: status,
                self.mb_cells_idx - start_addr + 2: self.func_number,
                self.mb_cells_idx - start_addr + 3: p1,
                self.mb_cells_idx - start_addr + 4: p2,
            }
        else:
            return {}

def simulate_pressure(value):
    return 50.0