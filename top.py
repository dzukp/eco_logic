from pylogic.io_object import IoObject
from pylogic.modbus_supervisor import ModbusDataObject
from post import Post
from brush_washer import BrushWasher
from func_names import FuncNames
from rpc_post_server import RpcPostServer

from threading import Lock
from queue import Queue


class Top(IoObject, ModbusDataObject):

    def __init__(self, *args):
        super().__init__(*args)
        self.supplier = None
        self.hoover = None
        self.posts = {}
        self.post_function = {}
        self.new_function = {}
        self.post_service = {}
        self.mb_cells_idx = None
        self.counter = 0
        self.side_posts = {'1': set(), '2': set()}
        self.side_brush_wash = {}
        self.hmi_post_number = 1

    def init(self):
        for child in self.children:
            if isinstance(child, Post):
                self.posts[child.name] = child
                self.post_function[child] = FuncNames.STOP
                self.post_service[child.name] = False
                # self.new_function[child] = FuncNames.STOP
            elif isinstance(child, BrushWasher):
                if child.name.endswith('1'):
                    self.side_brush_wash['1'] = child
                elif child.name.endswith('2'):
                    self.side_brush_wash['2'] = child
        posts = sorted(self.posts.values(), key=lambda p: int(p.name[5:]))
        self.side_posts['1'].update(posts[:len(posts) // 2])
        self.side_posts['2'].update(posts[len(posts) // 2:])
        for post in self.side_posts['1']:
            self.side_brush_wash['1'].add_post(post)
        for post in self.side_posts['2']:
            self.side_brush_wash['2'].add_post(post)
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
            if post.is_ready(self.post_service[post.name]):
                wished_funcs.add(func)
            elif func != FuncNames.STOP:
                self.logger.debug(f'Stop function `{post.name}` because it is not ready')

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

        if FuncNames.BRUSH in wished_funcs:
            if not self.supplier.try_brush():
                self.supplier.stop_brush()
                prepared_funcs.remove(FuncNames.BRUSH)
                self.logger.debug(f'It not ready for function `{FuncNames.BRUSH}`')
        else:
            self.supplier.stop_brush()

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

        if FuncNames.HOOVER in wished_funcs:
            hoover_cnt = sum([int(func == FuncNames.HOOVER) for func in self.post_function.values()])
            if not self.hoover.try_hoover(hoover_cnt):
                prepared_funcs.remove(FuncNames.HOOVER)
                self.hoover.stop()
                self.logger.debug(f'It not ready for function `{FuncNames.HOOVER}`')

        any_hoover_valve = any([post.is_need_hoover() for post in self.posts.values()])
        if any_hoover_valve:
            self.hoover.start()
        else:
            self.hoover.stop()

        if FuncNames.WHEEL_BLACK in wished_funcs:
            if not self.supplier.try_wheel_black():
                prepared_funcs.remove(FuncNames.WHEEL_BLACK)
                self.logger.debug(f'It not ready for function `{FuncNames.WHEEL_BLACK}`')
        else:
            self.supplier.stop_wheel_black()

        if FuncNames.POLISH in wished_funcs:
            if not self.supplier.try_polish():
                prepared_funcs.remove(FuncNames.POLISH)
                self.logger.debug(f'It not ready for function `{FuncNames.POLISH}`')
        else:
            self.supplier.stop_polish()

        if FuncNames.GLASS in wished_funcs:
            if not self.supplier.try_glass():
                prepared_funcs.remove(FuncNames.GLASS)
                self.logger.debug(f'It not ready for function `{FuncNames.GLASS}`')
        else:
            self.supplier.stop_glass()

        for post, func in self.post_function.items():
            if func in prepared_funcs:
                if not post.set_function(func, self.post_service[post.name]):
                    self.post_function[post] = FuncNames.STOP
                    self.post_service[post.name] = False
                    self.logger.debug(f'Post {post.name} didn\'t start function {func}')
            else:
                post.set_function(FuncNames.STOP)
                self.post_function[post] = FuncNames.STOP
                self.post_service[post.name] = False

    def set_function(self, post_name, function, service=False):
        if function not in FuncNames.all_funcs():
            self.logger.error(f'Hasn\'t function `{function}`')
            return False
        elif post_name not in self.posts:
            self.logger.error(f'Hasn\'t post `{post_name}`')
            return False
        elif not self.posts[post_name].is_ready(service):
            self.logger.debug(f'Post `{post_name}` not ready')
            return False
        # elif not self.get_readiness_functions(post_name)[function]:
        #     self.logger.info(f'Can\'t start function {function} on `{post_name}`. Function not ready.')
        #     return False
        else:
            self.logger.info(f'New function for `{post_name}` is {function}')
            self.new_function[self.posts[post_name]] = function
            self.post_service[post_name] = service
            return True

    def get_readiness_functions(self, post_name):
        return {
            FuncNames.WAX:
                self.supplier.is_ready_for_wax() and self.posts[post_name].is_func_allowed(FuncNames.WAX),
            FuncNames.SHAMPOO:
                self.supplier.is_ready_for_shampoo() and self.posts[post_name].is_func_allowed(FuncNames.SHAMPOO),
            FuncNames.FOAM:
                self.supplier.is_ready_for_foam() and self.posts[post_name].is_func_allowed(FuncNames.FOAM),
            FuncNames.OSMOSIS:
                self.supplier.is_ready_for_osmosis() and self.posts[post_name].is_func_allowed(FuncNames.OSMOSIS),
            FuncNames.COLD_WATER:
                self.supplier.is_ready_for_cold_water() and self.posts[post_name].is_func_allowed(FuncNames.COLD_WATER),
            FuncNames.BRUSH:
                self.supplier.is_ready_for_brush() and self.posts[post_name].is_func_allowed(FuncNames.BRUSH),
            FuncNames.HOOVER:
                self.hoover.is_ready() and self.posts[post_name].is_func_allowed(FuncNames.HOOVER),
            FuncNames.AIR: self.posts[post_name].is_func_allowed(FuncNames.AIR),
            FuncNames.WHEEL_BLACK: self.posts[post_name].is_func_allowed(FuncNames.WHEEL_BLACK),
            FuncNames.POLISH: self.posts[post_name].is_func_allowed(FuncNames.POLISH),
            FuncNames.GLASS: self.posts[post_name].is_func_allowed(FuncNames.GLASS),
        }

    def get_post_function(self, post_name):
        if post_name in self.posts:
            post = self.posts[post_name]
            return self.post_function[post]
        else:
            return ''

    def get_extra_rpc_data(self, post_name):
        if post_name in self.posts:
            post = self.posts[post_name]
            return {
                'brush_on': post.di_brush.val,
                'hoover_on': not post.di_hoover.val,
                'car_inside': post.is_car_inside()
            }
        else:
            return {}

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
                if data[self.mb_cells_idx - start_addr + 6] != post.func_frequencies[FuncNames.BRUSH]:
                    post.set_func_pump_frequency(FuncNames.BRUSH, data[self.mb_cells_idx - start_addr + 6])
                if data[self.mb_cells_idx - start_addr + 7] != post.func_frequencies[FuncNames.COLD_WATER]:
                    post.set_func_pump_frequency(FuncNames.COLD_WATER, data[self.mb_cells_idx - start_addr + 7])
                if data[self.mb_cells_idx - start_addr + 8] != post.func_frequencies[FuncNames.OSMOSIS]:
                    post.set_func_pump_frequency(FuncNames.OSMOSIS, data[self.mb_cells_idx - start_addr + 8])
                if post.hi_press_valve_off_timeout != data[self.mb_cells_idx - start_addr + 11] * 0.001:
                    post.set_hi_press_valve_off_timeout(float(data[self.mb_cells_idx - start_addr + 11]) * 0.001)
            n = data[self.mb_cells_idx - start_addr + 12]
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
                    int(post.func_frequencies[FuncNames.BRUSH]),
                    int(post.func_frequencies[FuncNames.COLD_WATER]),
                    int(post.func_frequencies[FuncNames.OSMOSIS]),
                    int(post.pressure_timeout),
                    int(post.min_pressure * 100),
                    int(post.hi_press_valve_off_timeout * 1000),
                ]
            else:
                post_data = [0] * 11

            data = [
                self.counter,
            ] + post_data + [
                self.hmi_post_number,
                11111
            ]
            result = dict([(self.mb_cells_idx - start_addr + i, val) for i, val in zip(range(len(data)), data)])
            return result
        else:
            return {}
