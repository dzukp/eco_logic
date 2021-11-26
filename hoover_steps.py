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
            self.logger.debug('start')
            return self.run

    def run(self):
        frequency = self.pid[self.fc_index](-self.owner.set_point)
        self.fc[self.fc_index].start()
        self.fc[self.fc_index].set_frequency(frequency)
        for fc, pid in zip(self.fc[:self.fc_index], self.pid[:self.fc_index]):
            fc.start()
            fc.set_frequency(self.owner.max_freq_limits)

        is_max_freq = self.owner.max_freq_limits - frequency < 0.1
        if self.ton_max_freq.process(is_max_freq, 3.0):
            if self.fc_index + 1 < min(len(self.fc), len(self.pid)):
                self.fc_index += 1
                self.logger.debug(f'incr fc count, work {self.fc_index + 1}')

        is_min_freq = frequency - self.owner.min_freq_limits < 0.1
        if self.ton_max_freq.process(is_min_freq, 5.0):
            if self.fc_index > 0:
                self.fc_index -= 1
                self.logger.debug(f'decr fc count, work {self.fc_index + 1}')
