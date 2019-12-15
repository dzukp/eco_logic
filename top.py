from pylogic.io_object import IoObject
from post import Post
from func_names import FuncNames
from rpc_post_server import RpcPostServer

from threading import Lock
from queue import Queue


class Top(IoObject):

    def __init__(self, *args):
        super().__init__(*args)
        self.supplier = None
        self.nofrost = None
        self.posts = {}
        self.post_function = {}
        self.new_function = {}
        self.rpc_server = RpcPostServer()

    def init(self):
        for child in self.children:
            if isinstance(child, Post):
                self.posts[child.name] = child
                self.post_function[child] = FuncNames.STOP
                self.new_function[child] = FuncNames.STOP
        self.rpc_server.set_top_object(self)
        self.rpc_server.start()

    def process(self):
        for post, func in self.new_function.items():
            self.post_function[post] = func
        self.function_process()
        for post, func in self.post_function.items():
            self.new_function[post] = func

    def function_process(self):
        wished_funcs = set()
        for func in self.post_function.values():
            wished_funcs.add(func)

        prepared_funcs = wished_funcs.copy()

        if FuncNames.WAX in wished_funcs:
            if not self.supplier.try_wax():
                prepared_funcs.remove(FuncNames.WAX)
        else:
            self.supplier.stop_wax()

        if FuncNames.SHAMPOO in wished_funcs:
            if not self.supplier.try_shampoo():
                prepared_funcs.remove(FuncNames.SHAMPOO)
        else:
            self.supplier.stop_shampoo()

        if FuncNames.FOAM in wished_funcs:
            if not self.supplier.try_foam():
                prepared_funcs.remove(FuncNames.FOAM)
        else:
            self.supplier.stop_foam()

        if FuncNames.INTENSIVE in wished_funcs:
            if not self.supplier.try_intensive():
                prepared_funcs.remove(FuncNames.INTENSIVE)
        else:
            self.supplier.stop_intensive()

        if FuncNames.HOT_WATER in wished_funcs:
            if not self.supplier.try_hot_water():
                prepared_funcs.remove(FuncNames.HOT_WATER)
        else:
            self.supplier.stop_hot_water()

        if FuncNames.COLD_WATER in wished_funcs:
            if not self.supplier.try_cold_water():
                prepared_funcs.remove(FuncNames.COLD_WATER)
        else:
            self.supplier.stop_cold_water()

        if FuncNames.OSMOSIS in wished_funcs:
            if not self.supplier.try_osmosis():
                prepared_funcs.remove(FuncNames.OSMOSIS)
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
