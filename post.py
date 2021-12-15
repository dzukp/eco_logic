from pylogic.io_object import IoObject
from pylogic.channel import InChannel, OutChannel
from pylogic.modbus_supervisor import ModbusDataObject
from pylogic.timer import Ton, Timer

from post_function import MultiValveSteps, MultiValvePumpSteps, BrushSteps, HooverSteps
from utils import floats_to_modbus_cells
from func_names import FuncNames


class Post(IoObject, ModbusDataObject):

    _save_attrs = ('func_frequencies', 'pressure_timeout', 'min_pressure', 'pump_on_timeout', 'valve_off_timeout',
                   'disabled_funcs', 'no_flow_frequency')

    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.di_hoover = InChannel(False)
        self.di_brush = InChannel(False)
        self.di_car_inside = InChannel(False)
        self.do_car_inside = OutChannel(False)
        self.ai_pressure = InChannel(0.0)
        self.di_flow = InChannel(False)
        self.valve_foam = None
        self.valve_wax = None
        self.valve_solution = None
        self.valve_cold_water = None
        self.valve_brush = None
        self.valve_osmos = None
        self.valve_wheel_black = None
        self.valve_air = None
        self.valve_polish = None
        self.valve_glass = None
        self.valve_hoover = None
        self.valve_shell = None
        self.pump = None
        self.current_func = FuncNames.STOP
        self.func_number = len(FuncNames.all_funcs())
        self.func_frequencies = {
            FuncNames.FOAM: 25.0,
            FuncNames.SHAMPOO: 40.0,
            FuncNames.WAX: 40.0,
            FuncNames.BRUSH: 40.0,
            FuncNames.COLD_WATER: 40.0,
            FuncNames.OSMOSIS: 40.0,
        }
        self.pump_on_timeout = 1.0
        self.valve_off_timeout = 1.0
        self.hi_press_valve_off_timeout = 2.0
        self.pressure_timeout = 5.0
        self.pressure_timer = Ton()
        self.min_pressure = 10.0
        self.no_flow_frequency = 15.0
        self.alarm_reset_timeout = 10.0
        self.alarm_reset_timer = Ton()
        self.alarm = False
        self.func_timer = Ton()
        self.mb_cells_idx = None
        self.func_steps = {}
        for name in FuncNames.all_funcs():
            if name in (FuncNames.FOAM, FuncNames.SHAMPOO, FuncNames.WAX, FuncNames.COLD_WATER, FuncNames.OSMOSIS):
                self.func_steps[name] = MultiValvePumpSteps(f'{name}_steps', self)
            elif name in (FuncNames.AIR, FuncNames.POLISH, FuncNames.WHEEL_BLACK, FuncNames.GLASS):
                self.func_steps[name] = MultiValveSteps(f'{name}_steps', self)
            elif name == FuncNames.BRUSH:
                self.func_steps[name] = BrushSteps(f'{name}_steps', self)
            elif name == FuncNames.HOOVER:
                self.func_steps[name] = HooverSteps(f'{name}_steps', self)
        self.disabled_funcs = []
        self.all_valves = set()

    def init(self):
        config = {'pump_on_timeout': self.pump_on_timeout, 'valve_off_timeout': self.valve_off_timeout,
                  'hi_press_valve_off_timeout': self.hi_press_valve_off_timeout}
        valves = {
            FuncNames.FOAM: [self.valve_foam],
            FuncNames.SHAMPOO: [self.valve_solution],
            FuncNames.WAX: [self.valve_wax],
            FuncNames.BRUSH: [self.valve_brush],
            FuncNames.COLD_WATER: [self.valve_cold_water],
            FuncNames.OSMOSIS: [self.valve_osmos],
            FuncNames.POLISH: [self.valve_polish],
            FuncNames.GLASS: [self.valve_glass],
            FuncNames.WHEEL_BLACK: [self.valve_wheel_black],
            FuncNames.HOOVER: [self.valve_hoover],
            FuncNames.AIR: [self.valve_air]
        }
        for func_name, step in self.func_steps.items():
            if func_name in valves:
                step.valves_link = valves[func_name]
                if func_name not in (FuncNames.HOOVER, FuncNames.AIR):
                    step.pump_link = [self.pump]
                step.set_config(config)

        for valves in valves.values():
            self.all_valves.update(valves)

        self.pump.reset()

    def process(self):
        self.do_car_inside.val = self.di_car_inside.val
        for func_name, step in self.func_steps.items():
            if func_name == self.current_func:
                if not step.is_active():
                    step.start()
            else:
                step.stop()
        for func_name, step in self.func_steps.items():
            step.process()

        pump = 0
        opened_valves = set()
        for func_name, step in self.func_steps.items():
            opened_valves = opened_valves.union(set(step.get_opened_valves()))
            pump = max(step.is_pump_started(), pump)
        closed_valves = self.all_valves.difference(opened_valves)

        for valve in closed_valves:
            valve.close()
        for valve in opened_valves:
            valve.open()

        if pump == 1:
            self.pump.start()
            self.pump.set_frequency(10.0)
        elif pump == 2:
            self.pump.start()
            self.pump.set_frequency(self.func_frequencies.get(self.current_func, 0.0))
        else:
            self.pump.stop()
            self.pump.set_frequency(0.0)

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
        return not self.di_hoover.val and self.current_func == FuncNames.HOOVER

    def is_brush_ready(self):
        return not self.di_brush.val and self.current_func == FuncNames.BRUSH

    def mb_cells(self):
        return self.mb_output(0).keys()

    def mb_input(self, start_addr, data):
        if self.mb_cells_idx is not None:
            cmd = data[self.mb_cells_idx - start_addr]
            if cmd & 0x0001:
                self.reset_alarm()

    def mb_output(self, start_addr):
        if self.mb_cells_idx is not None:
            status = int(self.alarm) * (1 << 0) + \
                     int(self.di_flow.val) * (1 << 1) + \
                     int(self.di_brush.val) * (1 << 2) + \
                     int(self.di_hoover.val) * (1 << 3) + \
                     int(self.di_car_inside.val) * (1 << 4)
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
