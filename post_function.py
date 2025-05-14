from pylogic.timer import Ton
from pylogic.steps import Steps
from func_names import FuncNames


class BaseSteps(Steps):

    def get_opened_valves(self):
        raise Exception('need implemets')

    def is_pump_started(self):
        raise Exception('need implemets')


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
        self.need_max_power = True
        self.no_flow_press = 0

    def step_open_valve(self):
        res = super(MultiValvePumpSteps, self).step_open_valve()
        self.pump = 1
        if res:
            return res
        self.no_flow_press = self.owner.ai_pressure.val
        return self.wait_press

    def step_first(self):
        self.need_max_power = True
        return super(MultiValvePumpSteps, self).step_first()

    def wait_press(self):
        res = super(MultiValvePumpSteps, self).step_open_valve()
        self.pump = 1
        if res:
            return res
        if self.owner.ai_pressure.val > 50:
            return self.wait_flow
        if self.ton.process(run=True, timeout=self.owner.begin_phase_timeout) and self.owner.ai_pressure.val < 50.0:
            self.ton.reset()
            if self.need_max_power:
                return self.full_work
            else:
                return self.full_work_2

    def wait_flow(self):
        res = super(MultiValvePumpSteps, self).step_open_valve()
        self.pump = 0
        if res:
            return res
        if self.check_flow():
            self.logger.info(
                f'self.owner.ai_pressure.rate() ({self.owner.ai_pressure.rate()} < {self.owner.flow_indicator})')
            self.ton.reset()
            if self.need_max_power:
                return self.full_work
            else:
                return self.full_work_2
        if self.owner.ai_pressure.val < 30:
            self.logger.info(f'low pressuer {self.owner.ai_pressure.val} < 30')
            return self.wait_press

    def full_work(self):
        res = super(MultiValvePumpSteps, self).step_open_valve()
        self.pump = 3
        if res:
            return res
        if self.ton.process(run=True, timeout=self.owner.begin_phase_timeout):
            self.ton.reset()
            return self.full_work_2

    def full_work_2(self):
        res = super(MultiValvePumpSteps, self).step_open_valve()
        self.pump = 2
        self.need_max_power = False
        if res:
            return res
        if self.ton.process(run=True, timeout=2.0) and self.check_no_flow_pressure():
            self.no_flow_press = self.owner.ai_pressure.val
            self.logger.info(f'no flow, pressure={self.no_flow_press}')
            return self.wait_press

    def check_no_flow_pressure(self):
        return self.owner.ai_pressure.val > self.owner.no_flow_pressure

    def check_flow(self):
        return self.owner.ai_pressure.rate() < self.owner.flow_indicator


class IntensiveMultiValvePumpSteps(MultiValvePumpSteps):
    def check_no_flow_pressure(self):
        return self.owner.ai_pressure.val > 35.0



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