import struct

from pylogic.io_object import IoObject
from pylogic.modbus_supervisor import ModbusDataObject
from pylogic.timer import Timer, Ton
from pylogic.utils import Hysteresis
from simple_pid import PID
from pylogic.channel import InChannel


class Hoover(IoObject, ModbusDataObject):

    def __init__(self, *args, **kwargs):
        super(Hoover, self).__init__(*args, **kwargs)
        self.started = False
        self.fc_1 = None
        self.fc_2 = None
        self.ai_press_1 = InChannel(0.0)
        self.ai_press_2 = InChannel(0.0)
        self.flap = None
        self.set_point = 0.0
        self.filter_diff_limit = 0.0
        self.pid_k_1 = 1.0
        self.pid_i_1 = 2.0
        self.pid_d_1 = 0.0
        self.pid_k_2 = 1.0
        self.pid_i_2 = 2.0
        self.pid_d_2 = 0.0
        self.freq_limits = [40.0, 60.0]
        self.pid_1 = PID(sample_time=0.5)
        self.pid_2 = PID(sample_time=0.5)
        self.pid_1.output_limits = tuple(self.freq_limits)
        self.pid_1.tunings = (self.pid_k_1, self.pid_i_1, self.pid_d_1)
        self.pid_2.output_limits = tuple(self.freq_limits)
        self.pid_2.tunings = (self.pid_k_2, self.pid_i_2, self.pid_d_2)
        self.min_freq_timer = Timer()
        self.mb_cells_idx = None

    def start(self):
        if not self.started:
            self.started = True
            self.logger.info('Start')

    def stop(self):
        if self.started:
            self.started = False
            self.logger.info('Stop')

    def process(self):
        if self.started:
            pass
        else:
            self.fc_1.stop()
            self.pid_1.reset()
            self.fc_2.stop()
            self.pid_2.reset()

    def mb_cells(self):
        return [self.mb_cells_idx, self.mb_cells_idx + 1]

    def mb_input(self, start_addr, data):
        if self.mb_cells_idx is not None:
            float_data = struct.unpack('ffff',
                                       struct.pack('HHHHHHHH',
                                                   *tuple(data[self.mb_cells_idx + 3: self.mb_cells_idx + 11])))
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
            if self.set_point != float_data[3]:
                self.set_point = float_data[3]
                self.logger.info(f'Set pressure task = {self.set_point}')
                self.save()

    def mb_output(self, start_addr):
        if self.mb_cells_idx is not None:
            status = int(self.started) * (1 << 0) | \
                     0xD000
            float_data = (self.ai_press_1.val, self.ai_press_2.val, self.pid_k_1, self.pid_i_1, self.pid_d_1,
                          self.pid_k_2, self.pid_i_2, self.pid_d_2, self.set_point, self.filter_diff_limit)
            float_data = struct.pack('f' * len(float_data), *float_data)
            float_data = struct.unpack('H' * (len(float_data) // 2), float_data)
            float_data = {self.mb_cells_idx - start_addr + i + 1: val for i, val in enumerate(float_data)}
            out_data = {
                self.mb_cells_idx - start_addr: status
            }
            out_data.update(float_data)
            return out_data
        else:
            return {}
