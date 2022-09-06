from mechanism import Mechanism
from pylogic.channel import OutChannel, InChannel
from pylogic.timer import Timer, Ton
from pylogic.modbus_supervisor import ModbusDataObject

import struct


class Altivar212(Mechanism, ModbusDataObject):
    """ Frequency converter Altivar 212 controlled by Modbus/RTU """

    CMD_FORWARD_START = 0xC400
    CMD_STOP = 0xC000
    CMD_RESET = 0xF000

    MASK_FORWARD_RUN = 0x0400
    MASK_ALARM = 0x0004

    STATE_IDLE = 0
    STATE_START = 1
    STATE_RUN = 2
    STATE_STOPPING = 3
    STATE_ALARM = 4

    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.ao_command = OutChannel(0)#команда частотнику
        self.ao_frequency = OutChannel(0)
        self.ai_status = InChannel(0)
        self.ai_frequency = InChannel(0)
        self.ai_alarm_code = InChannel(0)
        self.ai_frequency.set_trans(lambda v: v * 0.01)
        self.is_run = False
        self.is_alarm = False
        self.reset_alarm = True
        self.auto_frequency_task = 0.0
        self.man_frequency_task = 0.0
        self.timer = Ton()
        self.timer.set_timeout(5.0)
        self.state = self.STATE_IDLE
        self.func_state = self.state_idle
        self.reset_timer = Ton()
        self.reset_timer.set_timeout(2.0)
        self.alarm_auto_reset_timeout = 5.0
        self.alarm_auto_reset_timer = Ton()
        self.mb_cells_idx = None

    def process(self):
        self.is_alarm = self.check_alarm()
        self.is_run = self.check_run()
        self.func_state()
        reset_alarm_time = self.reset_timer.process(self.reset_alarm)
        if self.is_alarm and self.func_state != self.state_alarm:
            self.func_state = self.state_alarm
            self.logger.info('Alarm signal - alarm state')
        # Alarm auto reset by timeout
        if self.alarm_auto_reset_timer.process(run=self.state_alarm == self.func_state,
                                               timeout=self.alarm_auto_reset_timeout):
            self.logger.debug('Alarm reset by time')
            self.reset_alarm = True
        if self.reset_alarm:
            self.ao_command.val |= self.CMD_RESET
            if reset_alarm_time:
                self.reset_alarm = False

    def state_idle(self):
        self.ao_command.val = self.CMD_STOP
        self.ao_frequency.val = 0.0
        self.timer.reset()

    def state_starting(self):
        self.ao_command.val = self.CMD_FORWARD_START
        self.ao_frequency.val = self.man_frequency_task * 100.0 if self.manual else self.auto_frequency_task * 100.0
        if self.is_run:
            self.func_state = self.state_run
            self.logger.debug(f'{self.name}: run state')
        if self.timer.process(not self.is_run):
            self.func_state = self.state_alarm
            self.timer.reset()
            self.logger.debug(f'{self.name}: alarm state from starting state, don\'t run signal in timeout')

    def state_run(self):
        self.ao_command.val = self.CMD_FORWARD_START
        self.ao_frequency.val = self.man_frequency_task * 100.0 if self.manual else self.auto_frequency_task * 100.0
        if self.timer.process(not self.is_run):
            self.func_state = self.state_alarm
            self.timer.reset()
            self.logger.debug(f'{self.name}: alarm state from run state, don\'t run signal in timeout')

    def state_stopping(self):
        self.ao_command.val = self.CMD_STOP
        self.ao_frequency.val = 0.0
        if not self.is_run:
            self.logger.debug(f'{self.name}: idle state')
            self.func_state = self.state_idle

    def state_alarm(self):
        self.ao_command.val = self.CMD_STOP
        self.ao_frequency.val = 0.0
        if self.reset_alarm and not self.is_alarm:
            self.func_state = self.state_idle

    def start(self, manual=False):
        if manual == self.manual:
            if self.func_state == self.state_idle and not self.func_state == self.state_alarm:
                if self.func_state not in (self.state_starting, self.state_run):
                    self.func_state = self.state_starting
                    self.logger.info(f'{self.name}: start command {"manual" if self.manual else "automate"}')

    def stop(self, manual=False):
        if manual == self.manual:
            if self.func_state in (self.state_run, self.state_starting) and not self.func_state == self.state_alarm:
                if self.func_state not in (self.state_stopping, self.state_idle):
                    self.func_state = self.state_stopping
                    self.logger.info(f'{self.name}: stop command {"manual" if self.manual else "automate"}')

    def reset(self):
        if not self.reset_alarm:
            self.reset_alarm = True
            self.logger.info(f'{self.name}: reset command')

    def set_frequency(self, freq, manual=False, no_log=False):
        if manual:
            if freq != self.man_frequency_task:
                self.man_frequency_task = freq
                if not no_log:
                    self.logger.info(f'set manual frequency task: {freq}')
        else:
            if freq != self.auto_frequency_task:
                self.auto_frequency_task = freq
                if not no_log:
                    self.logger.debug(f'set auto frequency task: {freq}')

    def check_run(self):
        return (self.ai_status.val & self.MASK_FORWARD_RUN) == self.MASK_FORWARD_RUN

    def check_alarm(self):
        return False
        # return (self.ai_status.val & self.MASK_ALARM) == self.MASK_ALARM

    def is_alarm_state(self):
        return self.state_alarm == self.func_state

    def mb_cells(self):
        return self.mb_output(0).keys()

    def mb_input(self, start_addr, data):
        if self.mb_cells_idx is not None:
            cmd = data[- start_addr + self.mb_cells_idx ]
            if cmd & 0x0001:
                self.set_manual(True)
            if cmd & 0x0002:
                self.set_manual(False)
            if cmd & 0x0004:
                self.start(manual=True)
            if cmd & 0x0008:
                self.stop(manual=True)
            if cmd & 0x0010:
                self.reset()
            float_data = struct.unpack('fff', struct.pack('HHHHHH', *tuple(data[self.mb_cells_idx + 2: self.mb_cells_idx + 8])))
            self.set_frequency(float_data[1], manual=True)

    def mb_output(self, start_addr):
        if self.mb_cells_idx is not None:
            cmd = 0
            status = int(self.manual) * (1 << 0) | \
                     int(self.is_run) * (1 << 1) | \
                     int(self.is_alarm) * (1 << 2) | \
                     int(self.state_alarm == self.func_state) * (1 << 3) | \
                     0
            float_data2 = struct.pack('fff', self.ai_frequency.val, self.man_frequency_task, self.auto_frequency_task)
            float_data = struct.unpack('HHHHHH', float_data2)
            return {-start_addr + self.mb_cells_idx: cmd,
                    -start_addr + self.mb_cells_idx + 1: status,
                    -start_addr + self.mb_cells_idx + 2: float_data[0],
                    -start_addr + self.mb_cells_idx + 3: float_data[1],
                    -start_addr + self.mb_cells_idx + 4: float_data[2],
                    -start_addr + self.mb_cells_idx + 5: float_data[3],
                    -start_addr + self.mb_cells_idx + 6: float_data[4],
                    -start_addr + self.mb_cells_idx + 7: float_data[5],
                    -start_addr + self.mb_cells_idx + 8: self.ai_alarm_code.val,
                    -start_addr + self.mb_cells_idx + 9: 888,
                    }
        else:
            return {}


class InovanceMd310(Altivar212):
    CMD_FORWARD_START = 1
    CMD_STOP = 6
    CMD_RESET = 7

    MASK_FORWARD_RUN = 1
    MASK_STOP_RUN = 3
    MASK_ALARM = 0

    def check_run(self):
        return self.ai_status.val == self.MASK_FORWARD_RUN

    def check_alarm(self):
        return self.ai_alarm_code.val != 0


def trans_divide_10(value):
    return value / 10.0