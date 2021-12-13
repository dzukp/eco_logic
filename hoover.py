import struct

from pylogic.io_object import IoObject
from pylogic.modbus_supervisor import ModbusDataObject
from pylogic.timer import Timer, Ton
from pylogic.utils import Hysteresis
from simple_pid import PID
from pylogic.channel import InChannel

from hoover_steps import CascadeSteps


class Hoover(IoObject, ModbusDataObject):

    _save_attrs = ('pid_k_1', 'pid_i_1', 'pid_d_1', 'pid_k_2', 'pid_i_2', 'pid_d_2',
                   'min_freq_limits', 'max_freq_limits')

    def __init__(self, *args, **kwargs):
        super(Hoover, self).__init__(*args, **kwargs)
        self.started = True
        self.enabled = True
        self.fc_1 = None
        self.fc_2 = None
        self.ai_press_1 = InChannel(0.0)
        self.ai_press_2 = InChannel(0.0)
        self.flap = None
        self.set_point = -150.0
        self.filter_diff_limit = 100.0
        self.pid_k_1 = 0.1
        self.pid_i_1 = 0.2
        self.pid_d_1 = 0.0
        self.pid_k_2 = 0.1
        self.pid_i_2 = 0.2
        self.pid_d_2 = 0.0
        self.min_freq_limits, self.max_freq_limits = (40.0, 60.0)
        self.pid_1 = PID(sample_time=0.5)
        self.pid_2 = PID(sample_time=0.5)
        self.post_count = 0
        self.cascade_steps = None
        self.mb_cells_idx = None

    def init(self):
        self.cascade_steps = CascadeSteps(owner=self)

    def start(self):
        if not self.started:
            self.started = True
            self.logger.info('Start')

    def stop(self):
        if self.started:
            self.started = False
            self.logger.info('Stop')
        self.post_count = 0

    def enable(self, enable):
        if self.enabled != enable:
            self.enabled = enable
            self.logger.info('Enable' if enable else 'Disable')

    def process(self):
        self.pid_1.output_limits = (self.min_freq_limits, self.max_freq_limits)
        self.pid_1.tunings = (self.pid_k_1, self.pid_i_1, self.pid_d_1)
        self.pid_2.output_limits = (self.min_freq_limits, self.max_freq_limits)
        self.pid_2.tunings = (self.pid_k_2, self.pid_i_2, self.pid_d_2)
        if self.started:
            self.cascade_steps.start()
        else:
            self.cascade_steps.stop()
            self.fc_1.stop()
            self.pid_1.reset()
            self.fc_1.set_frequency(0)
            self.fc_2.stop()
            self.pid_2.reset()
            self.fc_2.set_frequency(0)
        self.cascade_steps.process()

    def try_hoover(self, post_count):
        self.post_count = post_count
        if self.is_ready():
            self.start()
            return True

    def is_ready(self):
        return (not self.fc_1.is_alarm_state() or not self.fc_2.is_alarm_state()) and self.enabled

    def mb_cells(self):
        return [self.mb_cells_idx, self.mb_cells_idx + 1]

    def mb_input(self, start_addr, data):
        if self.mb_cells_idx is not None:
            mb_cell_addr = self.mb_cells_idx - start_addr
            cmd = data[mb_cell_addr]
            if cmd & 0x0001:
                self.enable(1)
            if cmd & 0x0002:
                self.enable(0)
            float_cnt = 8
            float_data = struct.unpack('f' * float_cnt,
                                       struct.pack('HH' * float_cnt,
                                                   *tuple(data[mb_cell_addr + 7: mb_cell_addr + 7 + float_cnt * 2])))
            if self.pid_k_1 != float_data[0]:
                self.pid_k_1 = float_data[0]
                self.logger.info(f'Set Pid 1 K = {self.pid_k_1}')
                self.save()
            if self.pid_i_1 != float_data[1]:
                self.pid_i_1 = float_data[1]
                self.logger.info(f'Set Pid 1 I = {self.pid_i_1}')
                self.save()
            if self.pid_d_1 != float_data[2]:
                self.pid_d_1 = float_data[2]
                self.logger.info(f'Set Pid 1 K = {self.pid_d_1}')
                self.save()
            if self.pid_k_2 != float_data[3]:
                self.pid_k_2 = float_data[3]
                self.logger.info(f'Set Pid 2 K = {self.pid_k_2}')
                self.save()
            if self.pid_i_2 != float_data[4]:
                self.pid_i_2 = float_data[4]
                self.logger.info(f'Set Pid 2 I = {self.pid_i_2}')
                self.save()
            if self.pid_d_2 != float_data[5]:
                self.pid_d_2 = float_data[5]
                self.logger.info(f'Set Pid 2 K = {self.pid_d_2}')
                self.save()
            if self.set_point != float_data[6]:
                self.set_point = float_data[6]
                self.logger.info(f'Set pressure task = {self.set_point}')
                self.save()
            if self.filter_diff_limit != float_data[7]:
                self.filter_diff_limit = float_data[7]
                self.logger.info(f'Set filter diff limit = {self.filter_diff_limit}')
                self.save()

    def mb_output(self, start_addr):
        if self.mb_cells_idx is not None:
            mb_cell_addr = self.mb_cells_idx - start_addr
            status = int(self.enabled) * (1 << 0) | \
                     int(self.started) * (1 << 1) | \
                     0xD000
            float_data = (self.ai_press_1.val, self.ai_press_2.val, self.pid_k_1, self.pid_i_1, self.pid_d_1,
                          self.pid_k_2, self.pid_i_2, self.pid_d_2, self.set_point, self.filter_diff_limit)
            float_data = struct.pack('f' * len(float_data), *float_data)
            float_data = struct.unpack('H' * (len(float_data) // 2), float_data)
            float_data = {mb_cell_addr + 3 + i: val for i, val in enumerate(float_data)}
            out_data = {
                mb_cell_addr: 0xFF00,
                mb_cell_addr + 1: status,
                mb_cell_addr + 2: 0,
            }
            out_data.update(float_data)
            return out_data
        else:
            return {}
