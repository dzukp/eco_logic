from pylogic.io_object import IoObject
from pylogic.channel import InChannel
from pylogic.modbus_supervisor import ModbusDataObject


class Tank(IoObject, ModbusDataObject):
    """ Water tank with 3 level sensors """

    def __init__(self, *args):
        super().__init__(*args)
        self.di_low_level = InChannel(False)
        self.di_mid_level = InChannel(False)
        self.di_hi_level = InChannel(False)
        self._sens_err = False
        self._state = 0
        self._want_water = False
        self.mb_cells_idx = None

    def process(self):
        if not self.di_low_level.val and (self.di_hi_level.val or self.di_mid_level.val):
            if not self._sens_err:
                self.logger.debug('Sensor error - no low level')
                self._sens_err = True
        elif self.di_hi_level.val and (not self.di_mid_level.val or not self.di_low_level.val):
            if not self._sens_err:
                self.logger.debug('Sensor error - have hi level')
                self._sens_err = True
        elif self._sens_err:
            self.logger.debug('Sensor no error')
            self._sens_err = False

        if not self.di_mid_level.val:
            self._want_water = True
        elif self.di_hi_level.val:
            self._want_water = False

        if self._state == 0:
            if self.di_low_level.val:
                self._state = 1
                self.logger.debug('new level 1')
        elif self._state == 1:
            if self.di_low_level.val and self.di_mid_level.val:
                self._state = 2
                self.logger.debug('new level 2')
            elif not self.di_low_level.val:
                self._state = 0
                self.logger.debug('new level 0')
        elif self._state == 2:
            if self.di_low_level.val and self.di_mid_level.val and self.di_hi_level.val:
                self._state = 3
                self.logger.debug('new level 3')
            elif not self.di_mid_level.val:
                self._state = 1
                self.logger.debug('new level 1')
        elif self._state == 3:
            if not self.di_hi_level.val:
                self._state = 2
                self.logger.debug('new level 2')

    def is_full(self):
        return self.di_hi_level.val

    def is_want_water(self):
        return self._want_water

    def is_empty(self):
        return not self.di_low_level.val

    def sensors_error(self):
        return self._sens_err

    def mb_cells(self):
        return [self.mb_cells_idx, self.mb_cells_idx + 1]

    def mb_output(self, start_addr):
        if self.mb_cells_idx is not None:
            cmd = 0
            status = int(self.di_low_level.val) * (1 << 0) | \
                     int(self.di_mid_level.val) * (1 << 1) | \
                     int(self.di_hi_level.val) * (1 << 2) | \
                     int(self._sens_err) * (1 << 3) | \
                     int(self._want_water) * (1 << 4)
                #return {self.mb_cells_idx - start_addr: cmd, self.mb_cells_idx + 1 - start_addr: status}
            return {self.mb_cells_idx + start_addr: cmd, self.mb_cells_idx + 1 - start_addr: status}
        else:
            return {}


class FakeTank(IoObject, ModbusDataObject):

    def process(self):
        pass

    def is_full(self):
        return True

    def is_want_water(self):
        return False

    def is_empty(self):
        return False

    def sensors_error(self):
        return 0
