from pylogic.io_object import IoObject
from pylogic.modbus_supervisor import ModbusDataObject
from pylogic.timer import Ton
from func_names import FuncNames


class BrushWasher(IoObject, ModbusDataObject):
    """ Раковина мойки щеток """

    _save_attrs = ('wash_time', 'pause_time')

    def __init__(self, *args):
        super(BrushWasher, self).__init__(*args)
        self.enabled = True
        self.timer = Ton()
        self.wash_time = 60.0
        self.pause_time = 20.0
        self.valve = None
        self.posts = []
        self.state_func = self.state_idle
        self.any_brush = False
        self.need_wash = False
        self.mb_cells_idx = None

    def add_post(self, post):
        self.posts.append(post)

    def process(self):
        self.need_wash_process()
        if self.enabled:
            self.state_func()
        else:
            self.valve.close()
            self.set_state(self.state_idle)

    def need_wash_process(self):
        new_any_brush = False
        for post in self.posts:
            if post.current_func == FuncNames.BRUSH:
                new_any_brush = True
                break
        if not new_any_brush and self.any_brush:
            self.need_wash = True
        self.any_brush = new_any_brush

    def set_state(self, state):
        if self.state_func != state:
            self.state_func = state
            self.timer.reset()
            self.logger.info(f'new state {state.__name__}')

    def state_idle(self):
        self.valve.close()
        if self.need_wash:
            self.set_state(self.state_wash)

    def state_wash(self):
        self.valve.open()
        if self.timer.process(run=True, timeout=self.wash_time):
            self.need_wash = False
            self.set_state(self.state_pause)

    def state_pause(self):
        self.valve.close()
        if self.timer.process(run=True, timeout=self.pause_time):
            self.set_state(self.state_idle)

    def set_wash_time(self, timeout):
        if self.wash_time != timeout:
            self.wash_time = timeout
            self.save()
            self.logger.info(f'Set wash time {timeout}')

    def set_pause_time(self, timeout):
        if self.pause_time != timeout:
            self.pause_time = timeout
            self.save()
            self.logger.info(f'Set pause time {timeout}')

    def mb_cells(self):
        return self.mb_output(0).keys()

    def mb_input(self, start_addr, data):
        if self.mb_cells_idx is not None:
            cmd = data[self.mb_cells_idx - start_addr]
            if cmd & 0x0001:
                if not self.enabled:
                    self.enabled = True
                    self.logger.info('Enabled')
            if cmd & 0x0002:
                if self.enabled:
                    self.enabled = False
                    self.logger.info('Disabled')
            if cmd & 0x0004:
                self.set_state(self.state_wash)
                self.logger.info('external wash command')
            self.set_wash_time(data[self.mb_cells_idx - start_addr + 2])
            self.set_pause_time(data[self.mb_cells_idx - start_addr + 3])

    def mb_output(self, start_addr):
        if self.mb_cells_idx is not None:
            status = int(self.enabled) * (1 << 0) + \
                     int(self.state_func == self.state_idle) * (1 << 1) + \
                     int(self.state_func == self.state_wash) * (1 << 2) + \
                     int(self.state_func == self.state_pause) * (1 << 3)

            return {
                self.mb_cells_idx - start_addr: 0x0,
                self.mb_cells_idx - start_addr + 1: status,
                self.mb_cells_idx - start_addr + 2: int(self.wash_time),
                self.mb_cells_idx - start_addr + 3: int(self.pause_time)
            }
        else:
            return {}
