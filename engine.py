from mechanism import Mechanism
from pylogic.channel import OutChannel
from pylogic.modbus_supervisor import ModbusDataObject


class Engine(Mechanism, ModbusDataObject):
    """ Simple engine controlled by discrete input """

    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.do_start = OutChannel(False)
        self.started = False
        self.mb_cells_idx = None

    def process(self):
        self.do_start.val = self.started

    def start(self, manual=False):
        if manual == self.manual:
            self.do_start.val = True
            if not self.started:
                self.started = True
                self.logger.info(f'{self.name}: start command {"manual" if self.manual else "automate"}')

    def stop(self, manual=False):
        if manual == self.manual:
            self.do_start.val = False
            if self.started:
                self.started = False
                self.logger.info(f'{self.name}: stop command {"manual" if self.manual else "automate"}')

    def mb_cells(self):
        return [self.mb_cells_idx, self.mb_cells_idx + 1]

    def mb_input(self, start_addr, data):
        if self.mb_cells_idx is not None:
            cmd = data[self.mb_cells_idx - start_addr]
            if cmd & 0x0001:
                self.set_manual(True)
            if cmd & 0x0002:
                self.set_manual(False)
            if cmd & 0x0004:
                self.start(manual=True)
            if cmd & 0x0008:
                self.stop(manual=True)

    def mb_output(self, start_addr):
        if self.mb_cells_idx is not None:
            cmd = 0
            status = int(self.manual) * (1 << 0) | \
                     int(self.do_start.val) * (1 << 1) | \
                     0xC000
            #return {self.mb_cells_idx - start_addr: cmd, self.mb_cells_idx + 1 - start_addr: status}
            return {
                #self.mb_cells_idx - start_addr: cmd,
                self.mb_cells_idx + 1 - start_addr: status}
        else:
            return {}
