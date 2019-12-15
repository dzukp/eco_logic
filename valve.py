from mechanism import Mechanism
from pylogic.channel import OutChannel
from pylogic.modbus_supervisor import ModbusDataObject


class Valve(Mechanism, ModbusDataObject):

    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.do_open = OutChannel(False)
        self.opened = False
        self.mb_cells_idx = None

    def process(self):
        self.do_open.val = self.opened

    def open(self, manual=False):
        if manual == self.manual:
            self.do_open.val = True
            if not self.opened:
                self.opened = True
                self.logger.info(f'{self.name}: open command {"manual" if self.manual else "automate"}')

    def close(self, manual=False):
        if manual == self.manual:
            self.do_open.val = False
            if self.opened:
                self.opened = False
                self.logger.info(f'{self.name}: close command {"manual" if self.manual else "automate"}')

    def mb_cells(self):
        return self.mb_output(0).keys()

    def mb_input(self, start_addr, data):
        if self.mb_cells_idx is not None:
            cmd = data[self.mb_cells_idx - start_addr]
            if cmd & 0x0001:
                self.set_manual(True)
            if cmd & 0x0002:
                self.set_manual(False)
            if cmd & 0x0004:
                self.open(manual=True)
            if cmd & 0x0008:
                self.close(manual=True)

    def mb_output(self, start_addr):
        if self.mb_cells_idx is not None:
            cmd = 0
            status = int(self.manual) * (1 << 0) + \
                     int(self.do_open.val) * (1 << 1) + \
                     0x8000
            return {self.mb_cells_idx: cmd, self.mb_cells_idx + 1: status, self.mb_cells_idx + 2: 999}
        else:
            return {}


class NOValve(Valve):
    """ Normal open valve """

    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.do_close = OutChannel(False)
        self.opened = False

    def process(self):
        self.do_close.val = not self.opened

    def open(self, manual=False):
        if manual == self.manual:
            self.do_close.val = False
            if not self.opened:
                self.opened = True
                self.logger.info(f'{self.name}: open command {"manual" if self.manual else "automate"}')

    def close(self, manual=False):
        if manual == self.manual:
            self.do_close.val = True
            if self.opened:
                self.opened = False
                self.logger.info(f'{self.name}: close command {"manual" if self.manual else "automate"}')
