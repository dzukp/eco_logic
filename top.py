from pylogic.io_object import IoObject
from pylogic.modbus_supervisor import ModbusDataObject
from post import Post
from func_names import FuncNames
from rpc_post_server import RpcPostServer

from threading import Lock
from queue import Queue


class Top(IoObject, ModbusDataObject):

    def __init__(self, *args):
        super().__init__(*args)
        self.supplier = None
        self.nofrost = None
        self.posts = {}
        self.post_function = {}
        self.new_function = {}
        self.rpc_server = RpcPostServer()
        self.mb_cells_idx = None
        self.counter = 0

    def init(self):
        for child in self.children:
            if isinstance(child, Post):
                self.posts[child.name] = child
                self.post_function[child] = FuncNames.STOP
                # self.new_function[child] = FuncNames.STOP
        self.rpc_server.set_top_object(self)
        self.rpc_server.start()

    def process(self):
        for post, func in self.new_function.items():
            self.post_function[post] = func
        self.function_process()
        # for post, func in self.post_function.items():
        #     self.new_function[post] = func
        self.new_function.clear()
        self.counter = (self.counter + 1) % 30000

    def function_process(self):
        wished_funcs = set()
        for post, func in self.post_function.items():
            if not post.alarm:
                wished_funcs.add(func)
            elif func != FuncNames.STOP:
                self.logger.debug(f'Stop function `{post.name}` because it is alarm')

        prepared_funcs = wished_funcs.copy()

        if FuncNames.WAX in wished_funcs:
            if not self.supplier.try_wax():
                prepared_funcs.remove(FuncNames.WAX)
                self.logger.debug(f'It not ready for function `{FuncNames.WAX}`')
        else:
            self.supplier.stop_wax()

        if FuncNames.SHAMPOO in wished_funcs:
            if not self.supplier.try_shampoo():
                prepared_funcs.remove(FuncNames.SHAMPOO)
                self.logger.debug(f'It not ready for function `{FuncNames.SHAMPOO}`')
        else:
            self.supplier.stop_shampoo()

        if FuncNames.FOAM in wished_funcs:
            if not self.supplier.try_foam():
                prepared_funcs.remove(FuncNames.FOAM)
                self.logger.debug(f'It not ready for function `{FuncNames.FOAM}`')
        else:
            self.supplier.stop_foam()

        if FuncNames.INTENSIVE in wished_funcs:
            if not self.supplier.try_intensive():
                prepared_funcs.remove(FuncNames.INTENSIVE)
                self.logger.debug(f'It not ready for function `{FuncNames.INTENSIVE}`')
        else:
            self.supplier.stop_intensive()

        if FuncNames.HOT_WATER in wished_funcs:
            if not self.supplier.try_hot_water():
                prepared_funcs.remove(FuncNames.HOT_WATER)
                self.logger.debug(f'It not ready for function `{FuncNames.HOT_WATER}`')
        else:
            self.supplier.stop_hot_water()

        if FuncNames.COLD_WATER in wished_funcs:
            if not self.supplier.try_cold_water():
                prepared_funcs.remove(FuncNames.COLD_WATER)
                self.logger.debug(f'It not ready for function `{FuncNames.COLD_WATER}`')
        else:
            self.supplier.stop_cold_water()

        if FuncNames.OSMOSIS in wished_funcs:
            if not self.supplier.try_osmosis():
                prepared_funcs.remove(FuncNames.OSMOSIS)
                self.logger.debug(f'It not ready for function `{FuncNames.OSMOSIS}`')
        else:
            self.supplier.stop_osmosis()

        for post, func in self.post_function.items():
            if func in prepared_funcs:
                post.set_function(func)
            else:
                post.set_function(FuncNames.STOP)
                self.post_function[post] = FuncNames.STOP

    # def prepared_functions(self):
    #     readed_funcs = set(FuncNames.all_funcs())
    #     for func in FuncNames.all_funcs():
    #         if FuncNames.WAX == func:
    #             if not self.supplier.is_ready_for_wax():
    #                 readed_funcs.remove(func)
    #         elif FuncNames.SHAMPOO == func:
    #             if not self.supplier.is_ready_for_shampoo():
    #                 readed_funcs.remove(func)
    #         elif FuncNames.FOAM == func:
    #             if not self.supplier.is_ready_for_foam():
    #                 readed_funcs.remove(func)
    #         elif FuncNames.INTENSIVE == func:
    #             if not self.supplier.is_ready_for_intensive():
    #                 readed_funcs.remove(func)
    #     return readed_funcs

    def set_function(self, post_name, function):
        if function not in FuncNames.all_funcs():
            self.logger.error(f'Hasn\'t function `{function}`')
            return False
        elif post_name not in self.posts:
            self.logger.error(f'Hasn\'t post `{post_name}`')
            return False
        else:
            self.logger.info(f'New function for `{post_name}` is {function}')
            self.new_function[self.posts[post_name]] = function
            return True

    def get_readiness_functions(self):
        return {
            FuncNames.WAX: self.supplier.is_ready_for_wax(),
            FuncNames.SHAMPOO: self.supplier.is_ready_for_shampoo(),
            FuncNames.FOAM: self.supplier.is_ready_for_foam(),
            FuncNames.INTENSIVE: self.supplier.is_ready_for_intensive(),
            FuncNames.OSMOSIS: self.supplier.is_ready_for_osmosis(),
            FuncNames.COLD_WATER: self.supplier.is_ready_for_cold_water(),
            FuncNames.HOT_WATER: self.supplier.is_ready_for_hot_water()
        }

    def get_post_function(self, post_name):
        if post_name in self.posts:
            post = self.posts[post_name]
            return self.post_function[post]
        else:
            return ''

    def mb_cells(self):
        return [0, 400]

    def mb_input(self, start_addr, data):
        if self.mb_cells_idx is not None:
            for p in self.posts.values():
                if data[self.mb_cells_idx - start_addr + 1] != p.pump_on_timeout:
                    p.set_pump_on_timeout(float(data[self.mb_cells_idx - start_addr + 1]) * 0.001)
                if p.valve_off_timeout != data[self.mb_cells_idx - start_addr + 2]:
                    p.set_valve_off_timeout(float(data[self.mb_cells_idx - start_addr + 2]) * 0.001)
                if data[self.mb_cells_idx - start_addr + 3] != p.func_frequencies[FuncNames.FOAM]:
                    p.set_func_pump_frequency(FuncNames.FOAM, data[self.mb_cells_idx - start_addr + 3])
                if data[self.mb_cells_idx - start_addr + 4] != p.func_frequencies[FuncNames.SHAMPOO]:
                    p.set_func_pump_frequency(FuncNames.SHAMPOO, data[self.mb_cells_idx - start_addr + 4])
                if data[self.mb_cells_idx - start_addr + 5] != p.func_frequencies[FuncNames.WAX]:
                    p.set_func_pump_frequency(FuncNames.WAX, data[self.mb_cells_idx - start_addr + 5])
                if data[self.mb_cells_idx - start_addr + 6] != p.func_frequencies[FuncNames.HOT_WATER]:
                    p.set_func_pump_frequency(FuncNames.HOT_WATER, data[self.mb_cells_idx - start_addr + 6])
                if data[self.mb_cells_idx - start_addr + 7] != p.func_frequencies[FuncNames.COLD_WATER]:
                    p.set_func_pump_frequency(FuncNames.COLD_WATER, data[self.mb_cells_idx - start_addr + 7])
                if data[self.mb_cells_idx - start_addr + 8] != p.func_frequencies[FuncNames.OSMOSIS]:
                    p.set_func_pump_frequency(FuncNames.OSMOSIS, data[self.mb_cells_idx - start_addr + 8])

    def mb_output(self, start_addr):
        if self.mb_cells_idx is not None:
            data = [
                self.counter,
                int(self.posts['post_1'].pump_on_timeout * 1000),
                int(self.posts['post_1'].valve_off_timeout * 1000),
                int(self.posts['post_1'].func_frequencies[FuncNames.FOAM]),
                int(self.posts['post_1'].func_frequencies[FuncNames.SHAMPOO]),
                int(self.posts['post_1'].func_frequencies[FuncNames.WAX]),
                int(self.posts['post_1'].func_frequencies[FuncNames.HOT_WATER]),
                int(self.posts['post_1'].func_frequencies[FuncNames.COLD_WATER]),
                int(self.posts['post_1'].func_frequencies[FuncNames.OSMOSIS]),
                int(self.posts['post_1'].pressure_timeout),
                int(self.posts['post_1'].min_pressure * 100),
            ]
            result = dict([(self.mb_cells_idx - start_addr + i, val) for i, val in zip(range(len(data)), data)])
            return result
        else:
            return {}

