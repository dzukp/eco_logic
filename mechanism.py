from pylogic.io_object import IoObject


class Mechanism(IoObject):
    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.manual = False

    def set_manual(self, manual=True):
        if self.manual != manual:
            self.manual = manual
            self.logger.info(f'{"manual" if manual else "automate"} command')

    def set_automate(self):
        self.set_manual(manual=False)
