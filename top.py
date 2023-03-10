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
        self.hmi_post_number = 1
        self.supplier = None
        self.nofrost = None
        self.posts = {}
        self.post_function = {}
        self.new_function = {}
        self.mb_cells_idx = None
        self.counter = 0

    def init(self):
        for child in self.children:
            if isinstance(child, Post):
                self.posts[child.name] = child
                self.post_function[child] = FuncNames.STOP
                # self.new_function[child] = FuncNames.STOP

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
                if not post.set_function(func):
                    self.post_function[post] = FuncNames.STOP
                    self.logger.debug(f'Post {post.name} didn\'t start function {func}')
                else:
                    self.supplier.add_function(post.name, func)
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
        # elif not self.get_readiness_functions(post_name)[function]:
        #     self.logger.info(f'Can\'t start function {function} on `{post_name}`. Function not ready.')
        #     return False
        else:
            self.logger.info(f'New function for `{post_name}` is {function}')
            self.new_function[self.posts[post_name]] = function
            return True

    def get_readiness_functions(self, post_name):
        return {
            FuncNames.WAX:
                self.supplier.is_ready_for_wax() and self.posts[post_name].is_func_allowed(FuncNames.WAX),
            FuncNames.SHAMPOO:
                self.supplier.is_ready_for_shampoo() and self.posts[post_name].is_func_allowed(FuncNames.SHAMPOO),
            FuncNames.FOAM:
                self.supplier.is_ready_for_foam() and self.posts[post_name].is_func_allowed(FuncNames.FOAM),
            FuncNames.INTENSIVE:
                self.supplier.is_ready_for_intensive() and self.posts[post_name].is_func_allowed(FuncNames.INTENSIVE),
            FuncNames.OSMOSIS:
                self.supplier.is_ready_for_osmosis() and self.posts[post_name].is_func_allowed(FuncNames.OSMOSIS),
            FuncNames.COLD_WATER:
                self.supplier.is_ready_for_cold_water() and self.posts[post_name].is_func_allowed(FuncNames.COLD_WATER),
            FuncNames.HOT_WATER:
                self.supplier.is_ready_for_hot_water() and self.posts[post_name].is_func_allowed(FuncNames.HOT_WATER)
        }

    def get_post_function(self, post_name):
        if post_name in self.posts:
            post = self.posts[post_name]
            return self.post_function[post]
        else:
            return ''

    def mb_cells(self):
        return [0, self.mb_cells_idx + len(self.mb_output(self.mb_cells_idx))]

    def mb_input(self, start_addr, data):
        if self.mb_cells_idx is not None:
            post = self.posts.get(f'post_{self.hmi_post_number}')
            if post:
                if data[self.mb_cells_idx - start_addr + 1] * 0.001 != post.pump_on_timeout:
                    post.set_pump_on_timeout(float(data[self.mb_cells_idx - start_addr + 1]) * 0.001)
                if post.valve_off_timeout != data[self.mb_cells_idx - start_addr + 2] * 0.001:
                    post.set_valve_off_timeout(float(data[self.mb_cells_idx - start_addr + 2]) * 0.001)
                if data[self.mb_cells_idx - start_addr + 3] != post.func_frequencies[FuncNames.FOAM]:
                    post.set_func_pump_frequency(FuncNames.FOAM, data[self.mb_cells_idx - start_addr + 3])
                if data[self.mb_cells_idx - start_addr + 4] != post.func_frequencies[FuncNames.SHAMPOO]:
                    post.set_func_pump_frequency(FuncNames.SHAMPOO, data[self.mb_cells_idx - start_addr + 4])
                if data[self.mb_cells_idx - start_addr + 5] != post.func_frequencies[FuncNames.WAX]:
                    post.set_func_pump_frequency(FuncNames.WAX, data[self.mb_cells_idx - start_addr + 5])
                if data[self.mb_cells_idx - start_addr + 6] != post.func_frequencies[FuncNames.HOT_WATER]:
                    post.set_func_pump_frequency(FuncNames.HOT_WATER, data[self.mb_cells_idx - start_addr + 6])
                if data[self.mb_cells_idx - start_addr + 7] != post.func_frequencies[FuncNames.COLD_WATER]:
                    post.set_func_pump_frequency(FuncNames.COLD_WATER, data[self.mb_cells_idx - start_addr + 7])
                if data[self.mb_cells_idx - start_addr + 8] != post.func_frequencies[FuncNames.OSMOSIS]:
                    post.set_begin_phase_timeout(FuncNames.OSMOSIS, data[self.mb_cells_idx - start_addr + 8])
                if post.hi_press_valve_off_timeout != data[self.mb_cells_idx - start_addr + 11] * 0.001:
                    post.set_begin_phase_timeout(float(data[self.mb_cells_idx - start_addr + 11]) * 0.001)
                if data[self.mb_cells_idx - start_addr + 12] * 0.001 != post.begin_phase_timeout:
                    post.set_begin_phase_timeout(float(data[self.mb_cells_idx - start_addr + 12]) * 0.001)
                if data[self.mb_cells_idx - start_addr + 13] != post.no_flow_pressure:
                    post.set_no_flow_pressure(data[self.mb_cells_idx - start_addr + 13])
                if -data[self.mb_cells_idx - start_addr + 14] != post.flow_indicator:
                    post.set_flow_indicator(-data[self.mb_cells_idx - start_addr + 14])
            n = data[self.mb_cells_idx - start_addr + 15]
            if f'post_{n}' in self.posts:
                self.hmi_post_number = n

    def mb_output(self, start_addr):
        if self.mb_cells_idx is not None:
            post = self.posts.get(f'post_{self.hmi_post_number}')
            if post:
                post_data = [
                    int(post.pump_on_timeout * 1000),
                    int(post.valve_off_timeout * 1000),
                    int(post.func_frequencies[FuncNames.FOAM]),
                    int(post.func_frequencies[FuncNames.SHAMPOO]),
                    int(post.func_frequencies[FuncNames.WAX]),
                    int(post.func_frequencies[FuncNames.HOT_WATER]),
                    int(post.func_frequencies[FuncNames.COLD_WATER]),
                    int(post.func_frequencies[FuncNames.OSMOSIS]),
                    int(post.pressure_timeout),
                    int(post.min_pressure * 100),
                    int(post.hi_press_valve_off_timeout * 1000),
                    int(post.begin_phase_timeout * 1000),
                    int(post.no_flow_pressure),
                    int(-post.flow_indicator)
                ]
            else:
                post_data = [0] * 14

            data = [
                       self.counter,
                   ] + post_data + [
                       self.hmi_post_number
                   ]
            result = dict([(self.mb_cells_idx - start_addr + i, val) for i, val in zip(range(len(data)), data)])
            return result
        else:
            return {}
