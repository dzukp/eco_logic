from func_names import FuncNames
from pylogic.io_object import IoObject
from pylogic.modbus_supervisor import ModbusDataObject
from subsystems import WaterSupplier


class SideSupplier(IoObject, ModbusDataObject):

    def __init__(self, *args):
        super(SideSupplier, self).__init__(*args)
        self.active_functions = set()
        self.posts = []
        self.pump_foam = None
        self.pump_intensive = None
        self.valve_dose_wax = None
        self.valve_dose_shampoo = None
        self.valve_dose_water_shampoo = None
        self.valve_dose_hot_water_shampoo = None
        self.valve_dose_shampoo = None
        self.valve_dose_foam = None
        self.valve_dose_foam_2 = None
        self.valve_dose_intensive = None
        self.valve_dose_water_intensive = None
        self.valve_dose_osmos_intensive = None

    def process(self):
        if FuncNames.WAX in self.active_functions:
            self.valve_dose_wax.open()
        else:
            self.valve_dose_wax.close()

        if FuncNames.SHAMPOO in self.active_functions:
            self.valve_dose_shampoo.open()
            self.valve_dose_water_shampoo.open()
            self.valve_dose_hot_water_shampoo.open()
        else:
            self.valve_dose_shampoo.close()
            self.valve_dose_water_shampoo.close()
            self.valve_dose_hot_water_shampoo.close()

        if FuncNames.FOAM in self.active_functions:
            self.valve_dose_foam.open()
            self.valve_dose_foam_2.open()
            self.pump_foam.start()
        else:
            self.valve_dose_foam.close()
            self.valve_dose_foam_2.close()
            self.pump_foam.stop()

        if FuncNames.INTENSIVE in self.active_functions or FuncNames.FOAM in self.active_functions:
            self.valve_dose_water_intensive.open()
            self.valve_dose_osmos_intensive.open()
        else:
            self.valve_dose_water_intensive.close()
            self.valve_dose_osmos_intensive.close()

        if FuncNames.INTENSIVE in self.active_functions:
            self.valve_dose_intensive.open()
            self.pump_intensive.start()
        else:
            self.valve_dose_intensive.close()
            self.pump_intensive.stop()

        self.active_functions.clear()

    def add_function(self, func):
        self.active_functions.add(func)
