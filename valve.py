from mechanism import Mechanism
from pylogic.channel import OutChannel


class Valve(Mechanism):

    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.do_open = OutChannel(False)
        self.opened = False

    def process(self):
        self.do_open.val = self.opened

    def open(self, manual=False):
        if manual == self.manual:
            self.do_open.val = True
            self.opened = True
            if not self.opened:
                self.logger.debug(f'{self.name}: open command {"manual" if self.manual else "automate"}')

    def close(self, manual=False):
        if manual == self.manual:
            self.do_open.val = False
            self.opened = False
            if self.opened:
                self.logger.debug(f'{self.name}: close command {"manual" if self.manual else "automate"}')
