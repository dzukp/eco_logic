from pylogic.io_object import IoObject
from pylogic.channel import InChannel


class WaterPreparing(IoObject):
    """ Water preparing """

    def __init__(self, *args):
        super().__init__(args)
        self.di_press_1 = InChannel(False)
        self.ai_pe_1 = InChannel(0.0)
        self.di_press_2 = InChannel(False)
        self.ai_pe_2 = InChannel(0.0)
        self.di_press_3 = InChannel(False)
        self.pump_n1 = None
        self.pump_n2 = None
        self.pump_os1 = None
        self.pump_os2 = None
        self.pump_i1 = None
        self.tank_b1 = None
        self.tank_b2 = None
        self.valve_b1 = None
        self.valve_b2 = None
        self.valve_osmosis = None

