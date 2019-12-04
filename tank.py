from pylogic.io_object import IoObject
from pylogic.channel import InChannel


class Tank(IoObject):
    """ Water tank with 3 level sensors """

    def __init__(self, *args):
        super().__init__(args)
        self.di_low_level = InChannel(False)
        self.di_mid_level = InChannel(False)
        self.di_hi_level = InChannel(False)
        self._sens_err = False
        self._state = 0

    def process(self):
        if not self._sens_err:
            if not self.di_low_level.val and (self.di_hi_level.val or self.di_mid_level.val):
                self.logger.debug('Sensor error - no low level')
                self._sens_err = True
            elif self.di_hi_level.val and (not self.di_mid_level.val or not self.di_low_level.val):
                self.logger.debug('Sensor error - have hi level')
                self._sens_err = True
            else:
                self.logger.debug('Sensor no error')
                self._sens_err = False

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
        return not self.di_mid_level.val

    def is_empty(self):
        return not self.di_low_level.val

    def sensors_error(self):
        return self._sens_err

