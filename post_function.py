from pylogic.timer import Ton
from pylogic.steps import Steps
from func_names import FuncNames


class BaseSteps(Steps):

    def get_opened_valves(self):
        raise Exception('need implemets')

    def is_pump_started(self):
        raise Exception('need implemets')


class MultiValveSteps(BaseSteps):

    def __init__(self, name, owner, *args, **kwargs):
        super().__init__(name)
        self.owner = owner
        self.valve = None
        self.pump = 0
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
        self.pump = 0
        self.valve = False
        self.need_stop = False

    def step_first(self):
        return self.step_open_valve

    def step_open_valve(self):
        self.pump = 0
        self.valve = True
        if self.need_stop:
            self.ton.reset()
            return self.step_close_valve

    def step_close_valve(self):
        self.pump = 0
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
        return self.pump


class MultiValvePumpSteps(MultiValveSteps):

    def __init__(self, *args, **kwargs):
        super(MultiValvePumpSteps, self).__init__(*args, **kwargs)
        self.no_flow_press = 0

    def step_open_valve(self):
        res = super(MultiValvePumpSteps, self).step_open_valve()
        if res:
            return res
        self.pump = 1
        return self.wait_press

    def wait_press(self):
        res = super(MultiValvePumpSteps, self).step_open_valve()
        if res:
            return res
        self.pump = 1
        if self.owner.di_flow.val:
            self.ton.reset()
            return self.full_work
        if self.owner.ai_pressure.val > 50:
            return self.wait_flow

    def wait_flow(self):
        res = super(MultiValvePumpSteps, self).step_open_valve()
        if res:
            return res
        self.pump = 0
        if self.owner.di_flow.val:
            self.logger.info('di_flow')
            self.ton.reset()
            return self.full_work
        if self.no_flow_press - self.owner.ai_pressure.val > 20.0:
            self.logger.info(f'self.owner.ai_pressure.val - self.no_flow_press ({round(self.owner.ai_pressure.val - self.no_flow_press, 2)}) > 20.0')
            self.ton.reset()
            return self.full_work
        if self.owner.ai_pressure.val < 50:
            self.logger.info(f'low pressuer {self.owner.ai_pressure.val} < 50')
            return self.wait_press

    def full_work(self):
        res = super(MultiValvePumpSteps, self).step_open_valve()
        if res:
            return res
        if self.ton.process(run=True, timeout=2.0) and not self.owner.di_flow.val:
            self.no_flow_press = self.owner.ai_pressure.val
            self.logger.info(f'no di_flow, pressure={self.no_flow_press}')
            return self.wait_press
        self.pump = 2


class BrushSteps(MultiValvePumpSteps):

    def is_pump_started(self):
        if not self.owner.di_brush.val:
            return 0
        return super(BrushSteps, self).is_pump_started()

    def get_opened_valves(self):
        if not self.owner.di_brush.val:
            return []
        return super(BrushSteps, self).get_opened_valves()


class HooverSteps(MultiValveSteps):

    def get_opened_valves(self):
        if self.owner.di_hoover.val:
            return []
        return super(HooverSteps, self).get_opened_valves()
