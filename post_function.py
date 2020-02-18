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
        self.pump_on_timeout = 1.0
        self.valve_off_timeout = 1.0
        self.need_stop = False

    def set_config(self, config):
        self.pump_on_timeout = config['pump_on_timeout']
        self.valve_off_timeout = config['valve_off_timeout']

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
            return self.step_stop_pump

    def step_stop_pump(self):
        self.out_valve = True
        self.pump = False
        if self.ton.process(run=True, timeout=self.valve_off_timeout):
            self.valve.close()
            self.ton.reset()
            return self.step_close_valve

    def step_close_valve(self):
        self.out_valve = False
        self.pump = False
        self.valve.close()
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