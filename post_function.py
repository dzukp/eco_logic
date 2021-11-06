from pylogic.timer import Ton
from pylogic.steps import Steps
from func_names import FuncNames


class BaseSteps(Steps):

    def get_opened_valves(self):
        raise Exception('need implemets')

    def is_pump_started(self):
        raise Exception('need implemets')


class MultiValveSteps(BaseSteps):

    def __init__(self, name):
        super().__init__(name)
        self.valve = None
        self.pump = False
        self.need_stop = False
        self.ton = Ton()
        self.valve_off_timeout = 1.0
        self.valves_link = []

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
        return self.step_open_valve

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
        if self.valve:
            res += self.valves_link
        return res

    def is_pump_started(self):
        return False


class MultiValvePumpSteps(MultiValveSteps):

    def __init__(self, name):
        super().__init__(name)
        self.pump = False

    def idle(self):
        self.pump = False
        super(MultiValvePumpSteps, self).idle()

    def step_first(self):
        return self.step_open_valve

    def step_open_valve(self):
        self.pump = True
        return super(MultiValvePumpSteps, self).step_open_valve()

    def step_close_valve(self):
        self.pump = False
        return super(MultiValvePumpSteps, self).step_close_valve()

    def is_pump_started(self):
        return self.pump
