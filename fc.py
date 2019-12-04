from mechanism import Mechanism
from pylogic.channel import OutChannel, InChannel
from pylogic.timer import Timer, Ton


class Altivar212(Mechanism):
    """ Frequency converter Altivar 212 controlled by Modbus/RTU """

    CMD_FORWARD_START = 0x0400
    CMD_STOP = 0x0000
    CMD_RESET = 0x2000

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
        self.frequency_task = 0.0
        self.timer = Ton()
        self.timer.set_timeout(2.0)
        self.state = self.STATE_IDLE
        self.func_state = self.state_idle
        self.reset_timer = Ton()
        self.reset_timer.set_timeout(2.0)

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
        self.ao_frequency.val = self.frequency_task
        if self.is_run:
            self.func_state = self.state_run
            self.logger.debug(f'{self.name}: run state')
        if self.timer.process(not self.is_run):
            self.func_state = self.state_alarm
            self.timer.reset()
            self.logger.debug(f'{self.name}: alarm state from starting state, don\'t run signal in timeout')

    def state_run(self):
        self.ao_command.val = self.CMD_STOP
        self.ao_frequency.val = self.frequency_task
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
