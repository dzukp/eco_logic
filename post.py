from pylogic.io_object import IoObject
from pylogic.channel import InChannel
from pylogic.modbus_supervisor import ModbusDataObject

from func_names import FuncNames


class Post(IoObject, ModbusDataObject):

    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.ai_pressure = InChannel(0.0)
        self.valve_foam = None
        self.valve_wax = None
        self.valve_shampoo = None
        self.valve_cold_water = None
        self.valve_hot_water = None
        self.valve_osmos = None
        self.valve_intensive = None
        self.valve_out_1 = None
        self.valve_out_2 = None
        self.pump = None
        self.func = self._func_idle
        self.func_by_name = {
            FuncNames.FOAM: self._func_foam,
            FuncNames.SHAMPOO: self._func_shampoo,
            FuncNames.WAX: self._func_wax,
            FuncNames.HOT_WATER: self._func_hot_water,
            FuncNames.COLD_WATER: self._func_cold_water,
            FuncNames.OSMOSIS: self._func_osmosis,
            FuncNames.INTENSIVE: self._func_intensive,
            FuncNames.STOP: self._func_idle
        }
        self.mb_cells_idx = None

    def process(self):
        self.func()

    def set_function(self, func_name):
        try:
            new_func = self.func_by_name[func_name]
            if new_func != self.func:
                self.func = new_func
                self.logger.info('set function `func_name`')
        except KeyError:
            self.logger.error(f'func for `{func_name}` not exists')

    def _open_valve(self, valve):
        valves = [
            self.valve_foam,
            self.valve_wax,
            self.valve_shampoo,
            self.valve_cold_water,
            self.valve_hot_water,
            self.valve_intensive]
        if valve:
            valves.remove(valve)
            valve.open()
        for v in valves:
            v.close()

    def _func_idle(self):
        self._open_valve(None)

    def _func_foam(self):
        self._open_valve(self.valve_foam)

    def _func_shampoo(self):
        self._open_valve(self.valve_shampoo)

    def _func_wax(self):
        self._open_valve(self.valve_wax)

    def _func_hot_water(self):
        self._open_valve(self.valve_hot_water)

    def _func_cold_water(self):
        self._open_valve(self.valve_cold_water)

    def _func_osmosis(self):
        self._open_valve(self.valve_osmos)

    def _func_intensive(self):
        self._open_valve(self.valve_intensive)

    def mb_cells(self):
        return self.mb_output(0).keys()

    def mb_input(self, start_addr, data):
        pass

    def mb_output(self, start_addr):
        if self.mb_cells_idx is not None:
            return {
                self.mb_cells_idx - start_addr: 777,
                self.mb_cells_idx - start_addr + 1: 777,
                self.mb_cells_idx - start_addr + 2: 777,
                self.mb_cells_idx - start_addr + 3: 777,
                self.mb_cells_idx - start_addr + 4: 777,
                self.mb_cells_idx - start_addr + 5: 777,
            }
        else:
            return {}


