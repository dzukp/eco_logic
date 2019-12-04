from pylogic.io_object import IoObject
from pylogic.channel import InChannel


class Post(IoObject):

    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.ai_pressure = InChannel(0.0)
        self.valve_foam = None
        self.valve_wax = None
        self.valve_shampoo = None
        self.valve_cold_water = None
        self.valve_hot_water = None
        self.valve_out_1 = None
        self.valve_out_2 = None

    def init(self):
        self.valve_foam = self.find_child_by_name('v_foam')
        self.valve_wax = self.find_child_by_name('v_wax')
        self.valve_shampoo = self.find_child_by_name('v_shampoo')
        self.valve_cold_water = self.find_child_by_name('v_cold_water')
        self.valve_hot_water = self.find_child_by_name('v_hot_water')
        self.valve_out_1 = self.find_child_by_name('v_out_1')
        self.valve_out_2 = self.find_child_by_name('v_out_2')

    def process(self):
        self.logger.debug(self.ai_pressure.val)