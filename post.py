import struct

from pylogic.io_object import IoObject
from pylogic.channel import InChannel
from pylogic.modbus_supervisor import ModbusDataObject
from pylogic.timer import Ton

from func_names import FuncNames


class Post(IoObject, ModbusDataObject):

    _save_attrs = ('foam_frequency_task', 'water_frequency_task', 'pump_timeout')

    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.ai_pressure = InChannel(0.0)
        self.di_flow = InChannel(False)
        self.valve_foam = None
        self.valve_wax = None
        self.valve_shampoo = None
        self.valve_cold_water = None
        self.valve_hot_water = None
        self.valve_osmos = None
        self.valve_intensive = None
        self.valve_out_water = None
        self.valve_out_foam = None
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
        self.func_number = len(FuncNames.all_funcs())
        self.foam_frequency_task = 30.0
        self.water_frequency_task = 50.0
        self.pump_timeout = 3.0
        self.pump_timer = Ton()
        self.alarm = False
        self.mb_cells_idx = None

    def process(self):
        self.func()

    def set_function(self, func_name):
        try:
            new_func = self.func_by_name[func_name]
            if new_func != self.func:
                self.func = new_func
                self.func_number = FuncNames.all_funcs().index(func_name)
                self.logger.info(f'set function {func_name}')
        except KeyError:
            self.logger.error(f'func for `{func_name}` not exists')

    def set_alarm(self):
        self.alarm = True
        self.func = self.func_by_name[FuncNames.STOP]

    def _open_valve(self, valve):
        valves = [
            self.valve_foam,
            self.valve_wax,
            self.valve_shampoo,
            self.valve_osmos,
            self.valve_cold_water,
            self.valve_hot_water,
            self.valve_intensive]
        if isinstance(valve, (list, tuple)):
            for v in valve:
                valves.remove(v)
                v.open()
        else:
            valves.remove(valve)
            valve.open()
        for v in valves:
            v.close()

    def _func_idle(self):
        self._open_valve([])
        self.pump.stop()
        self.pump.set_frequency(0.0)

    def _func_foam(self):
        self._open_valve(self.valve_foam)
        self.valve_out_foam.open()
        self.valve_out_water.close()
        self.pump.start()
        self.pump.set_frequency(self.foam_frequency_task)
        if self.pump_timer.process(run=self.pump.is_run and not self.di_flow.val, timeout=self.pump_timeout):
            self.logger.info(f'Foam programm -> alarm pump run but no flow')
            self.set_alarm()

    def _func_shampoo(self):
        self._open_valve(self.valve_shampoo)
        self.valve_out_foam.close()
        self.valve_out_water.open()
        self.pump.start()
        self.pump.set_frequency(self.water_frequency_task)
        if self.pump_timer.process(run=self.pump.is_run and not self.di_flow.val, timeout=self.pump_timeout):
            self.logger.info(f'Shampoo programm -> alarm pump run but no flow')
            self.set_alarm()

    def _func_wax(self):
        self._open_valve(self.valve_wax)
        self.valve_out_foam.close()
        self.valve_out_water.open()
        self.pump.start()
        self.pump.set_frequency(self.water_frequency_task)
        if self.pump_timer.process(run=self.pump.is_run and not self.di_flow.val, timeout=self.pump_timeout):
            self.logger.info(f'Wax programm -> alarm pump run but no flow')
            self.set_alarm()

    def _func_hot_water(self):
        self._open_valve(self.valve_hot_water)
        self.valve_out_foam.close()
        self.valve_out_water.open()
        self.pump.start()
        self.pump.set_frequency(self.water_frequency_task)
        if self.pump_timer.process(run=self.pump.is_run and not self.di_flow.val, timeout=self.pump_timeout):
            self.logger.info(f'Hot water programm -> alarm pump run but no flow')
            self.set_alarm()

    def _func_cold_water(self):
        self._open_valve(self.valve_cold_water)
        self.valve_out_foam.close()
        self.valve_out_water.open()
        self.pump.start()
        self.pump.set_frequency(self.water_frequency_task)
        if self.pump_timer.process(run=self.pump.is_run and not self.di_flow.val, timeout=self.pump_timeout):
            self.logger.info(f'Cold water programm -> alarm pump run but no flow')
            self.set_alarm()

    def _func_osmosis(self):
        self._open_valve(self.valve_osmos)
        self.valve_out_foam.close()
        self.valve_out_water.open()
        self.pump.start()
        self.pump.set_frequency(self.water_frequency_task)
        if self.pump_timer.process(run=self.pump.is_run and not self.di_flow.val, timeout=self.pump_timeout):
            self.logger.info(f'Osmosis programm -> alarm pump run but no flow')
            self.set_alarm()

    def _func_intensive(self):
        self._open_valve(self.valve_intensive)
        self.valve_out_foam.close()
        self.valve_out_water.close()
        self.pump.stop()
        self.pump.set_frequency(0.0)

    def mb_cells(self):
        return self.mb_output(0).keys()

    def mb_input(self, start_addr, data):
        pass

    def mb_output(self, start_addr):
        if self.mb_cells_idx is not None:
            status = 0
            data = struct.pack('>f', self.ai_pressure.val)
            p1, p2 = struct.unpack('>HH', data)
            return {
                self.mb_cells_idx - start_addr: 0,
                self.mb_cells_idx - start_addr + 1: status,
                self.mb_cells_idx - start_addr + 2: self.func_number,
                self.mb_cells_idx - start_addr + 3: p1,
                self.mb_cells_idx - start_addr + 4: p2,
            }
        else:
            return {}


