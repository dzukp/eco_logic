from pylogic.io_object import IoObject
from pylogic.channel import InChannel
from pylogic.modbus_supervisor import ModbusDataObject
from pylogic.timer import Ton


class BottomWash(IoObject, ModbusDataObject):

    def __init__(self, *args):
        super().__init__(*args)
        self.di_in_sens = InChannel(False)
        self.di_out_sens = InChannel(False)
        self.pump_wash = None
        self.tank_wash = None
        self.pump_circle_water = None
        self.tank_circle_water = None
        self.valve_circle_water = None
        self.valve_drainage = None
        self.valve_wash_sand_tank = None
        self.func_state = self.__state_wait
        self.need_drainage = False
        self.enabled = True
        self.mb_cells_idx = None

    def process(self):
        self.drainage_check()
        if self.enabled:
            self.process_bottom_wash()
            self.process_circle_water_tank()
            self.process_wash_tank()
            self.process_drainage()
        else:
            self.pump_wash.stop()
            self.valve_circle_water.close()
            self.pump_circle_water.stop()
            self.valve_circle_water.close()
            self.valve_drainage.close()
            self.valve_wash_sand_tank.close()
            self.func_state = self.__state_wait

    def enable(self):
        if not self.enabled:
            self.enabled = True
            self.logger.info('Enabled')

    def disable(self):
        if self.enabled:
            self.enabled = False
            self.logger.info('Disabled')

    def drainage_check(self):
        if self.tank_circle_water.is_full() and self.tank_wash.is_full():
            if not self.need_drainage:
                self.logger.debug('Need drainage')
                self.need_drainage = True
        else:
            if self.need_drainage:
                self.logger.debug('Not need drainage')
                self.need_drainage = False

    def process_bottom_wash(self):
        if self.di_in_sens.val:
            self.pump_wash.start()
        else:
            self.pump_wash.stop()

    def process_circle_water_tank(self):
        if self.tank_circle_water.is_want_water():
            self.valve_circle_water.open()
        else:
            self.valve_circle_water.close()

    def process_wash_tank(self):
        if self.tank_wash.is_want_water() and not self.tank_circle_water.is_empty():
            self.pump_circle_water.start()
        elif not self.need_drainage:
            self.pump_circle_water.stop()

    def process_drainage(self):
        if self.need_drainage:
            self.pump_circle_water.start()
            self.valve_drainage.open()
        else:
            self.valve_drainage.close()

    def __state_wait(self):
        self.pump_wash.stop()
        if self.di_in_sens.val:
            self.logger.info('sens 1 on')
            self.func_state = self.__state_wash_1

    def __state_wash_1(self):
        self.pump_wash.start()
        if self.di_out_sens.val and self.di_out_sens.val:
            self.logger.info('sens 1 off and sens 2 on')
            self.func_state = self.__state_wash_2

    def __state_wash_2(self):
        self.pump_wash.start()
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
