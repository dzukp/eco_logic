from pylogic.io_object import IoObject


class Mechanism(IoObject):
    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.manual = False

    def set_manual(self, manual=True):
        self.manual = manual

    def set_automate(self):
        self.manual = False
