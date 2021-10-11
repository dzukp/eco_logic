from pylogic.io_object import IoObject
from pylogic.channel import InChannel, OutChannel
from pylogic.modbus_supervisor import ModbusDataObject
from subsystems import TankFiller, PumpTankFiller, OsmosisTankFiller, WaterSupplier, TwoPumpWaterSupplier
from func_names import FuncNames
from utils import floats_to_modbus_cells, modbus_cells_to_floats


class WaterPreparing(IoObject, ModbusDataObject):
    """ Water preparing """

    _save_attrs = ('water_enough_press', 'water_pump_on_press', 'water_pump_off_press',
                   'osmosis_enough_press', 'osmosis_pump_on_press', 'osmosis_pump_off_press')

    def __init__(self, *args):
        super().__init__(*args)
        # self.di_press_1 = InChannel(False)  # дискретный датчик давления после насоса p1
        self.ai_pe_1 = InChannel(0.0)  # аналоговый датчик давления после насоса П1
        # self.di_press_2 = InChannel(False)  # дискретный датчик давления после П2
        self.ai_pe_2 = InChannel(0.0)  # аналоговый датчик давления после фильтра
        self.ai_pe_3 = InChannel(0.0)  # аналоговый датчик давления после насоса П2
        # self.di_press_3 = InChannel(False)
        self.di_press_4 = InChannel(True)
        self.do_no_n3_press_signal = OutChannel(False)
        self.pump_n1 = None
        self.pump_n1_2 = None
        # self.pump_n1_3 = None
        self.pump_n2 = None
        self.pump_n3 = None
        self.pump_os1 = None
        self.pump_os2 = None
        self.pump_os = None
        self.pump_i1 = None
        self.tank_b1 = None
        self.tank_b2 = None
        self.valve_b1 = None
        self.valve_b2 = None
        self.valve_water_os = None
        # self.valve_dose_wax = None
        # self.valve_dose_shampoo = None
        # self.valve_dose_foam = None
        # self.valve_dose_intensive = None
        self.water_enough_press = 2.0
        self.water_pump_on_press = 3.0
        self.water_pump_off_press = 4.0
        self.osmosis_enough_press = 2.0
        self.osmosis_pump_on_press = 3.0
        self.osmosis_pump_off_press = 4.0
        self.b1_filler = PumpTankFiller('b1_filler')
        self.b2_filler = OsmosisTankFiller('b2_filler')
        self.water_supplier = WaterSupplier('cold_water')
        self.pre_filter_supplier = WaterSupplier('pre_filter')
        self.osmos_supplier = WaterSupplier('osmosis')
        self.start_b1 = True
        self.start_b2 = True
        self.start_water_press = True
        self.start_osmos_press = True
        self.mb_cells_idx = None
        self.active_functions = set()

    def init(self):
        self.b1_filler.tank = self.tank_b1
        self.b1_filler.valve = self.valve_b1
        self.b1_filler.pump = self.pump_n3
        self.b1_filler.di_press = self.di_press_4
        self.b1_filler.do_no_press_signal = self.do_no_n3_press_signal
        self.b2_filler.tank = self.tank_b2
        self.b2_filler.valve = self.valve_b2
        self.b2_filler.pump1 = self.pump_os1
        self.b2_filler.pump2 = self.pump_os2
        self.b2_filler.pid_pump = self.pump_os
        self.b2_filler.valve_inlet = self.valve_water_os
        # self.b2_filler.di_pressure = self.di_press_2
        self.water_supplier.tank = self.tank_b1
        self.water_supplier.ai_pressure = self.ai_pe_2
        # self.water_supplier.di_pressure = self.di_press_1
        self.water_supplier.pump = self.pump_n1
        self.pre_filter_supplier.ai_pressure = self.ai_pe_1
        self.pre_filter_supplier.tank = self.tank_b1
        self.pre_filter_supplier.pump = self.pump_n1_2
        self.osmos_supplier.tank = self.tank_b2
        self.osmos_supplier.ai_pressure = self.ai_pe_3
        # self.osmos_supplier.di_pressure = self.di_press_2
        self.osmos_supplier.pump = self.pump_n2
        self.b1_filler.set_logger(self.logger.getChild(self.b1_filler.name))
        self.b2_filler.set_logger(self.logger.getChild(self.b2_filler.name))
        self.water_supplier.set_logger(self.logger.getChild(self.water_supplier.name))
        self.osmos_supplier.set_logger(self.logger.getChild(self.osmos_supplier.name))

    def process(self):
        # Filling Water Tank
        if self.start_b1:
            self.b1_filler.start()
        else:
            self.b1_filler.stop()
        self.b1_filler.process()

        # Filling Osmosis Tank
        if self.start_b2:
            self.b2_filler.start()
        else:
            self.b2_filler.stop()
        if self.tank_b1.is_empty():
            self.b2_filler.disable()
        # elif not self.di_press_1.val:
        #     self.b2_filler.disable()
        elif not self.water_supplier.is_can_supply():
            self.b2_filler.disable()
        else:
            self.b2_filler.enable()
        self.b2_filler.process()

        # Supplying water
        self.water_supplier.enough_pressure = self.water_enough_press
        self.water_supplier.pump_on_press = self.water_pump_on_press
        self.water_supplier.pump_off_press = self.water_pump_off_press
        if self.start_water_press:
            self.water_supplier.start()
        else:
            self.water_supplier.stop()
        self.water_supplier.process()

        # Supplying pressure before filter
        self.pre_filter_supplier.enough_pressure = self.water_enough_press
        self.pre_filter_supplier.pump_on_press = self.water_pump_on_press
        self.pre_filter_supplier.pump_off_press = self.water_pump_off_press
        if self.start_water_press:
            self.pre_filter_supplier.start()
        else:
            self.pre_filter_supplier.stop()
        self.pre_filter_supplier.process()

        # Supplying osmos
        self.osmos_supplier.enough_pressure = self.osmosis_enough_press
        self.osmos_supplier.pump_on_press = self.osmosis_pump_on_press
        self.osmos_supplier.pump_off_press = self.osmosis_pump_off_press
        if self.start_osmos_press:
            self.osmos_supplier.start()
        else:
            self.osmos_supplier.stop()
        self.osmos_supplier.process()

        # Functions
        # if FuncNames.WAX in self.active_functions:
        #     self.valve_dose_wax.open()
        # else:
        #     self.valve_dose_wax.close()
        # if FuncNames.SHAMPOO in self.active_functions:
        #     self.valve_dose_shampoo.open()
        # else:
        #     self.valve_dose_shampoo.close()
        # if FuncNames.FOAM in self.active_functions:
        #     self.valve_dose_foam.open()
        # else:
        #     self.valve_dose_foam.close()
        # if FuncNames.INTENSIVE in self.active_functions:
        #     self.valve_dose_intensive.open()
        #     self.pump_i1.start()
        # else:
        #     self.valve_dose_intensive.close()
        #     self.pump_i1.stop()

    def is_ready_for_foam(self):
        return self.osmos_supplier.is_can_supply() or self.water_supplier.is_can_supply()

    def is_ready_for_wax(self):
        return self.water_supplier.is_can_supply()

    def is_ready_for_shampoo(self):
        return self.water_supplier.is_can_supply()

    def is_ready_for_cold_water(self):
        return self.water_supplier.is_can_supply()

    def is_ready_for_brush(self):
        return self.water_supplier.is_can_supply()

    def is_ready_for_osmosis(self):
        return self.osmos_supplier.is_can_supply()

    def try_wax(self):
        if self.is_ready_for_wax():
            # self.valve_dose_wax.open()
            self.active_functions.add(FuncNames.WAX)
            return True
        else:
            self.stop_wax()
            return False

    def try_shampoo(self):
        if self.is_ready_for_shampoo():
            # self.valve_dose_shampoo.open()
            self.active_functions.add(FuncNames.SHAMPOO)
            return True
        else:
            self.stop_shampoo()
            return False

    def try_foam(self):
        if self.is_ready_for_foam():
            # self.valve_dose_foam.open()
            self.active_functions.add(FuncNames.FOAM)
            return True
        else:
            self.stop_foam()
            return False

    def try_brush(self):
        if self.is_ready_for_brush():
            self.active_functions.add(FuncNames.BRUSH)
            return True
        else:
            self.stop_brush()
            return False

    def try_cold_water(self):
        if self.is_ready_for_cold_water():
            self.active_functions.add(FuncNames.COLD_WATER)
            return True
        else:
            self.stop_cold_water()
            return False

    def try_osmosis(self):
        if self.is_ready_for_osmosis():
            self.active_functions.add(FuncNames.OSMOSIS)
            return True
        else:
            self.stop_osmosis()
            return False

    def stop_wax(self):
        self.active_functions.discard(FuncNames.WAX)
        # self.valve_dose_wax.close()

    def stop_shampoo(self):
        self.active_functions.discard(FuncNames.SHAMPOO)
        # self.valve_dose_shampoo.close()

    def stop_foam(self):
        self.active_functions.discard(FuncNames.FOAM)
        # self.valve_dose_foam.close()

    def stop_brush(self):
        self.active_functions.discard(FuncNames.BRUSH)

    def stop_cold_water(self):
        self.active_functions.discard(FuncNames.COLD_WATER)

    def stop_osmosis(self):
        self.active_functions.discard(FuncNames.OSMOSIS)

    def mb_input(self, start_addr, data):
        if self.mb_cells_idx is not None:
            addr = self.mb_cells_idx - start_addr
            cmd = data[addr]
            if cmd & 0x0001:
                self.start_b1 = True
            if cmd & 0x0002:
                self.start_water_press = True
            if cmd & 0x0004:
                self.start_b2 = True
            if cmd & 0x0008:
                self.start_osmos_press = True
            if cmd & 0x0010:
                self.start_b1 = False
            if cmd & 0x0020:
                self.start_water_press = False
            if cmd & 0x0040:
                self.start_b2 = False
            if cmd & 0x0080:
                self.start_osmos_press = False
            floats = modbus_cells_to_floats(data[addr + 12:addr + 24])
            last_floats = self.water_pump_off_press, self.water_pump_on_press, self.water_enough_press, \
                          self.osmosis_pump_off_press, self.osmosis_pump_on_press, self.osmosis_enough_press
            if last_floats != floats:
                self.logger.debug(f'New press settings {floats}')
                self.water_pump_off_press, self.water_pump_on_press, self.water_enough_press, self.osmosis_pump_off_press, \
                self.osmosis_pump_on_press, self.osmosis_enough_press = floats
                self.save()

    def mb_output(self, start_addr):
        if self.mb_cells_idx is not None:
            cmd = 0
            status = int(False) * (1 << 0) | \
                     int(self.start_b1) * (1 << 4) | \
                     int(self.start_water_press) * (1 << 5) | \
                     int(self.start_b2) * (1 << 6) | \
                     int(self.start_osmos_press) * (1 << 7) | \
                     int(self.di_press_4.val) * (1 << 8)
            tmp_data = floats_to_modbus_cells((self.ai_pe_1.val, self.ai_pe_2.val, self.ai_pe_3.val))
            water_suppl_status = 0
            osmos_suppl_status = 0
            tmp_data_2 = floats_to_modbus_cells((self.water_pump_off_press, self.water_pump_on_press,
                                                 self.water_enough_press, self.osmosis_pump_off_press,
                                                 self.osmosis_pump_on_press, self.osmosis_enough_press))
            data = [cmd, status] + tmp_data + [water_suppl_status, 0, osmos_suppl_status, 0] + tmp_data_2
            result = dict([(self.mb_cells_idx - start_addr + i, val) for i, val in zip(range(len(data)), data)])
            return result
        else:
            return {}


def simulate_pressure(value):
    return 3.0
