from pylogic.io_object import IoObject
from pylogic.timer import Timer


class OperatingTimer(IoObject):

    _save_attrs = ['limit', 'operating_time']

    def __init__(self, **kwargs):
        super(OperatingTimer, self).__init__(**kwargs)
        self.parent_name = self.parent.full_name.partition('.')[2]
        self.timer = Timer()
        self.running = False
        self.operating_time = 0.0
        self.limit = 3600.0 * 1000
        self.excess = False
        self.next_save = 0.0
        self.save_step = 600

    def process(self):
        if self.operating_time > self.limit:
            self.excess = True
        if self.next_save <= self.operating_time:
            self.next_save = ((self.operating_time + self.save_step) // self.save_step) * self.save_step
            self.save()

    def run(self, run):
        if run:
            self.running = True
            self.timer.start()
        elif self.running:
            self.running = False
            self.operating_time += self.timer.elapsed()
            self.timer.reset()

    def get_operating_hours(self):
        if self.running:
            return (self.operating_time + self.timer.elapsed()) / 3600.0
        else:
            return self.operating_time / 3600.0

    def reset(self):
        self.operating_time = 0.0
        self.next_save = 0.0
        self.excess = False
        self.save()
