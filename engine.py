from mechanism import Mechanism
from pylogic.channel import OutChannel


class Engine(Mechanism):
    """ Simple engine controlled by discrete input """

    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.do_start = OutChannel(False)
        self.started = False

    def process(self):
        self.do_start.val = self.started

    def start(self, manual=False):
        if manual == self.manual:
            self.started = True
            self.do_start.val = True
            if not self.started:
                self.logger.debug(f'{self.name}: start command {"manual" if self.manual else "automate"}')

    def stop(self, manual=False):
        if manual == self.manual:
            self.started = False
            self.do_start.val = False
            if self.started:
                self.logger.debug(f'{self.name}: stop command {"manual" if self.manual else "automate"}')
