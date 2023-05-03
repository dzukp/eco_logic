from pylogic.steps import Steps
from pylogic.timer import Ton


class CascadeSteps(Steps):

    def __init__(self, owner, *args, **kwargs):
        super(CascadeSteps, self).__init__(*args, **kwargs)
        self.owner = owner
        self.ton_max_freq = Ton()
        self.ton_min_freq = Ton()
        self.fc_index = 0
        self.fc = [self.owner.fc_1, self.owner.fc_2]
        self.pid = [self.owner.pid_1, self.owner.pid_2]

    def idle(self):
        for fc, pid in zip(self.fc, self.pid):
            fc.stop()
            pid.reset()

    def step_first(self):
        self.idle()
        if self.owner.post_count > 0:
            self.fc_index = 0
            self.ton_max_freq.reset()
            self.ton_min_freq.reset()
            self.logger.debug('start')
            return self.run

    def run(self):
        self.pid[self.fc_index].setpoint = -self.owner.set_point
        frequency = self.pid[self.fc_index](-self.owner.ai_press_1.val)
        self.fc[self.fc_index].start()
        self.fc[self.fc_index].set_frequency(frequency)
        for fc, pid in zip(self.fc[:self.fc_index], self.pid[:self.fc_index]):
            fc.start()
            fc.set_frequency(self.owner.max_freq_limits)
        for fc, pid in zip(self.fc[self.fc_index + 1:], self.pid[self.fc_index + 1:]):
            fc.stop()
            fc.set_frequency(0)

        is_max_freq = self.owner.max_freq_limits - frequency < 0.1
        if self.ton_max_freq.process(is_max_freq, 3.0):
            if self.fc_index + 1 < min(len(self.fc), len(self.pid)):
                self.fc_index += 1
                self.logger.debug(f'incr fc count, work {self.fc_index + 1}')

        is_min_freq = frequency - self.owner.min_freq_limits < 0.1
        if self.ton_min_freq.process(is_min_freq, 5.0):
            if self.fc_index > 0:
                self.fc_index -= 1
                self.logger.debug(f'decr fc count, work {self.fc_index + 1}')


class StepsV2(Steps):

    def __init__(self, owner, *args, **kwargs):
        super(StepsV2, self).__init__(*args, **kwargs)
        self.owner = owner
        self.ton_max_freq = Ton()
        self.ton_min_freq = Ton()
        self.second_fc_on_timeout = 6.0
        self.second_fc_off_timeout = 6.0
        self.death_zone = 10
        self.fc_primary = self.owner.fc_1
        self.fc_secondary = self.owner.fc_2
        self.pid = self.owner.pid_2

    def idle(self):
        self.fc_primary.stop()
        self.fc_secondary.stop()
        self.pid.reset()

    def step_first(self):
        self.idle()
        if self.owner.post_count > 0:
            self.ton_min_freq.reset()
            self.ton_max_freq.reset()
            self.logger.debug('start')
            return self.work_fc1

    def work_fc1(self):
        self.fc_primary.set_frequency(self.owner.max_freq_limits)
        self.fc_primary.start()
        self.fc_secondary.stop()
        is_low_press = (self.owner.ai_press_1.val - self.owner.set_point) > self.death_zone
        if self.ton_max_freq.process(is_low_press, self.second_fc_on_timeout):
            self.logger.debug(f'work_pid press={self.owner.ai_press_1.val}')
            self.ton_max_freq.reset()
            return self.work_pid

    def work_pid(self):
        self.pid.setpoint = -self.owner.set_point
        frequency = self.pid(-self.owner.ai_press_1.val)
        self.fc_primary.set_frequency(self.owner.max_freq_limits)
        self.fc_primary.start()
        self.fc_secondary.set_frequency(frequency)
        self.fc_secondary.start()
        is_hi_press = (self.owner.ai_press_1.val - self.owner.set_point) < -self.death_zone
        if self.ton_min_freq.process(is_hi_press, self.second_fc_off_timeout):
            self.logger.debug(f'work_fc1 press={self.owner.ai_press_1.val}')
            self.ton_min_freq.reset()
            return self.work_fc1
