from pylogic.timer import Ton
from pylogic.steps import Steps
from func_names import FuncNames


class SimplePostFunctionSteps(Steps):
    def __init__(self, name):
        super().__init__(name)
        self.valve = None
        self.out_valve = False
        self.pump = False
        self.ton = Ton()
        self.ton2 = Ton()
        self.pump_on_timeout = 1.0
        self.valve_off_timeout = 1.0
        self.hi_press_valve_off_timeout = 2.0
        self.need_stop = False

    def set_config(self, config):
        self.pump_on_timeout = config['pump_on_timeout']
        self.valve_off_timeout = config['valve_off_timeout']
        self.hi_press_valve_off_timeout = config['hi_press_valve_off_timeout']

    def stop(self):
        self.need_stop = True

    def is_active(self):
        return self.current_step in (self.step_first, self.step_open_valve, self.step_start_pump)

    def idle(self):
        self.out_valve = False
        self.pump = False
        self.valve.close()
        self.need_stop = False
        self.ton.reset()

    def step_first(self):
        return self.step_open_valve()

    def step_open_valve(self):
        self.out_valve = True
        self.valve.open()
        if self.ton.process(run=True, timeout=self.pump_on_timeout):
            self.pump = True
            self.ton.reset()
            return self.step_start_pump

    def step_start_pump(self):
        self.out_valve = True
        self.valve.open()
        self.pump = True
        if self.need_stop:
            self.pump = False
            self.ton.reset()
            self.ton2.reset()
            return self.step_stop

    def step_stop(self):
        self.out_valve = True
        self.pump = False
        v1 = self.ton.process(run=True, timeout=self.valve_off_timeout)
        v2 = self.ton2.process(run=True, timeout=self.hi_press_valve_off_timeout)
        if v1:
            self.valve.close()
        if v2:
            self.out_valve = False
        if v1 and v2:
            self.ton.reset()
            self.ton2.reset()
            return self.idle


class PostIntensiveSteps(Steps):
    def __init__(self, name):
        super().__init__(name)
        self.valve = None
        self.out_valve = False
        self.pump = False
        self.need_stop = False

    def set_config(self, config):
        pass

    def stop(self):
        self.need_stop = True

    def is_active(self):
        return self.current_step in (self.step_first, self.step_open_valve)

    def idle(self):
        self.out_valve = False
        self.pump = False
        self.valve.close()
        self.need_stop = False

    def step_first(self):
        return self.step_open_valve()

    def step_open_valve(self):
        self.pump = False
        self.valve.open()
        if self.need_stop:
            return self.idle


class MultiValveSteps(Steps):

    def __init__(self, name):
        super().__init__(name)
        self.valve = None
        self.pump = False
        self.need_stop = False
        self.ton = Ton()
        self.valve_off_timeout = 1.0
        self.valves_link = []
        self.pump_link = []

    def set_config(self, config):
        self.valve_off_timeout = config['valve_off_timeout']

    def stop(self):
        self.need_stop = True

    def is_active(self):
        return self.current_step in (self.step_first, self.step_open_valve)

    def idle(self):
        self.pump = False
        self.valve = False
        self.need_stop = False

    def step_first(self):
        return self.step_open_valve()

    def step_open_valve(self):
        self.pump = True
        self.valve = True
        if self.need_stop:
            return self.step_close_valve

    def step_close_valve(self):
        self.pump = False
        if self.ton.process(run=True, timeout=self.valve_off_timeout):
            self.valve = False
            self.ton.reset()
            return self.idle

    def get_opened_valves(self):
        res = []
        if self.pump:
            res += self.pump_link
        if self.valve:
            res += self.valves_link
        return res


class MultiValveNoPumpSteps(MultiValveSteps):
    def step_open_valve(self):
        res = super().step_open_valve()
        self.pump = False
        return res


class SharedValveSteps(Steps):

    def __init__(self, name):
        super().__init__(name)
        self.out_valve = False
        self.valves = False
        self.pump = False
        self.need_stop = False
        self.ton = Ton()
        self.valve_off_timeout = 1.0

    def set_config(self, config):
        self.valve_off_timeout = config['valve_off_timeout']

    def stop(self):
        self.need_stop = True

    def is_active(self):
        return self.current_step in (self.step_first, self.step_open_valve)

    def idle(self):
        self.out_valve = False
        self.valves = False
        self.pump = False
        self.need_stop = False

    def step_first(self):
        return self.step_open_valve()

    def step_open_valve(self):
        self.pump = True
        self.out_valve = True
        self.valves = True
        if self.need_stop:
            return self.step_close_valve

    def step_close_valve(self):
        self.out_valve = False
        self.pump = False
        return self.idle
