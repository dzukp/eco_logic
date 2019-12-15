from mechanism import Mechanism
from pylogic.channel import OutChannel, InChannel
from pylogic.timer import Timer, Ton
from pylogic.modbus_supervisor import ModbusDataObject


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
        self.ao_command = OutChannel(0)
        self.ao_frequency = OutChannel(0)
        self.ai_status = InChannel(0)
        self.ai_frequency = InChannel(0)
        self.ai_alarm_code = InChannel(0)
        self.is_run = False
        self.is_alarm = False
        self.reset_alarm = False
        self.auto_frequency_task = 0.0
        self.man_frequency_task = 0.0
        self.timer = Ton()
        self.timer.set_timeout(2.0)
        self.state = self.STATE_IDLE
        self.func_state = self.state_idle
        self.reset_timer = Ton()
        self.reset_timer.set_timeout(2.0)
        self.mb_cells_idx = None

    def process(self):
        self.is_alarm = (self.ai_status.val & self.MASK_ALARM) == self.MASK_ALARM
        self.is_run = (self.ai_status.val & self.MASK_FORWARD_RUN) == self.MASK_FORWARD_RUN
        self.func_state()
        reset_alarm_time = self.reset_timer.process(self.reset_alarm)
        if self.is_alarm:
            self.func_state = self.state_alarm
            self.logger.debug('Alarm signal - alarm state')
        if self.reset_alarm:
            self.ao_command.val |= self.CMD_RESET
            if reset_alarm_time:
                self.reset_alarm = False

    def state_idle(self):
        self.ao_command.val = self.CMD_STOP
        self.ao_frequency.val = 0.0
        self.timer.reset()

    def state_starting(self):
        self.ao_command.val = self.CMD_STOP
        self.ao_frequency.val = self.man_frequency_task if self.manual else self.auto_frequency_task
        if self.is_run:
            self.func_state = self.state_run
            self.logger.debug(f'{self.name}: run state')
        if self.timer.process(not self.is_run):
            self.func_state = self.state_alarm
            self.timer.reset()
            self.logger.debug(f'{self.name}: alarm state from starting state, don\'t run signal in timeout')

    def state_run(self):
        self.ao_command.val = self.CMD_STOP
        self.ao_frequency.val = self.man_frequency_task if self.manual else self.auto_frequency_task
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
                    self.logger.debug(f'{self.name}: start command {"manual" if self.manual else "automate"}')

    def stop(self, manual=False):
        if manual == self.manual:
            if self.func_state in (self.state_run, self.state_starting) and not self.func_state == self.state_alarm:
                if self.func_state not in (self.state_stopping, self.state_idle):
                    self.func_state = self.state_stopping
                    self.logger.debug(f'{self.name}: stop command {"manual" if self.manual else "automate"}')

    def mb_cells(self):
        return [self.mb_cells_idx, self.mb_cells_idx + 5]

    def mb_input(self, start_addr, data):
        if self.mb_cells_idx is not None:
            cmd = data[- start_addr + self.mb_cells_idx]
            if cmd & 0x0001:
                self.set_manual(True)
            if cmd & 0x0002:
                self.set_manual(False)
            if cmd & 0x0004:
                self.start(manual=True)
            if cmd & 0x0008:
                self.stop(manual=True)
            self.man_frequency_task = data[-start_addr + self.mb_cells_idx + 1]

    def mb_output(self, start_addr):
        if self.mb_cells_idx is not None:
            cmd = 0
            status = int(self.manual) * (1 << 0) | \
                     int(self.is_run) * (1 << 1) | \
                     int(self.is_alarm) * (1 << 2) | \
                     0x400
            return {-start_addr + self.mb_cells_idx: cmd,
                    -start_addr + self.mb_cells_idx + 1: int(self.ai_frequency.val),
                    -start_addr + self.mb_cells_idx + 2: 0,
                    -start_addr + self.mb_cells_idx + 3: int(self.man_frequency_task),
                    -start_addr + self.mb_cells_idx + 4: 0,
                    -start_addr + self.mb_cells_idx + 5: int(self.auto_frequency_task) * 100,
                    -start_addr + self.mb_cells_idx + 6: 0,
                    -start_addr + self.mb_cells_idx + 7: self.ai_alarm_code.val,
                    -start_addr + self.mb_cells_idx + 7: 888,
                    }
        else:
            return {}
