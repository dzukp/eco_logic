from pylogic.io_object import IoObject
from pylogic.channel import InChannel
from pylogic.modbus_supervisor import ModbusDataObject
from pylogic.timer import Ton


class BottomWash(IoObject, ModbusDataObject):

    def __init__(self, *args):
        super().__init__(*args)
        self.di_in_sens = InChannel(False)
        self.di_out_sens = InChannel(False)
        self.valve_wash = None
        self.func_state = self.__state_wait
        self.enabled = False
        self.mb_cells_idx = None

    def process(self):
        if self.enabled:
            self.func_state()
        else:
            self.valve_wash.close()
            self.func_state = self.__state_wait

    def enable(self):
        if not self.enabled:
            self.enabled = True
            self.logger.info('Enabled')

    def disable(self):
        if self.enabled:
            self.enabled = False
            self.logger.info('Disabled')

    def __state_wait(self):
        self.valve_wash.close()
        if self.di_in_sens.val:
            self.logger.info('sens 1 on')
            self.func_state = self.__state_wash_1

    def __state_wash_1(self):
        self.valve_wash.open()
        if self.di_out_sens.val and self.di_out_sens.val:
            self.logger.info('sens 1 off and sens 2 on')
            self.func_state = self.__state_wash_2

    def __state_wash_2(self):
        self.valve_wash.open()
        if not self.di_out_sens.val:
            self.logger.info('sens 2 off')
            self.func_state = self.__state_wait

    def mb_input(self, start_addr, data):
        if self.mb_cells_idx is not None:
            mb_cell_addr = self.mb_cells_idx - start_addr
            cmd = data[mb_cell_addr]
            if cmd & 0x0001:
                self.enable()
            if cmd & 0x0002:
                self.disable()

    def mb_output(self, start_addr):
        if self.mb_cells_idx is not None:
            mb_cell_addr = self.mb_cells_idx - start_addr
            status = int(self.enabled) * (1 << 0) | \
                     int(self.func_state != self.__state_wait) * (1 << 1) | \
                     int(self.di_in_sens.val) * (1 << 2) | \
                     int(self.di_out_sens.val) * (1 << 3)
            return {
                mb_cell_addr: 0xFF00,
                mb_cell_addr + 1: status
            }
        else:
            return {}
