from pylogic.logged_object import LoggedObject
from pylogic.io_object import IoObject

from func_names import FuncNames

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import threading
import time
import logging


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


class MyXMLRPCServer(SimpleXMLRPCServer):
    """"
    MyXMLRPCServer

    MyXMLRPCServer Description
    """
    def process_request(self, request, client_address):
        self.client_address = client_address
        return SimpleXMLRPCServer.process_request(
            self, request, client_address)


class RpcPostServer(LoggedObject):
    """RpcPostServer"""
    def __init__(self):
        super().__init__('RpcServer')
        self.set_logger(self.logger.getChild('rpc_post_server'))
        self.top_object = None
        self.tag_srv = None
        self.server_thread = None
        self.host = ('0.0.0.0', 9876)

        self.post_state = LoggedObject('PostState')
        self.post_state.set_logger(self.post_state.logger.getChild('rpc_post_state'))

    def set_top_object(self, top_object: IoObject):
        self.top_object = top_object

    def set_tag_server(self, tag_srv):
        self.tag_srv = tag_srv

    def start(self):
        self.server_thread = threading.Thread(target=self.run, name='PostsRpcServer', daemon=True)
        self.server_thread.start()

    def run(self):
        with MyXMLRPCServer(self.host, requestHandler=RequestHandler) as server:

            server.register_introspection_functions()

            @server.register_function
            def start_function(post_number, function_name):
                """
                Старт с терминала

                :param post_number: номер поста
                :return: 'Ok' если параметры коррекны и функция вызвана успешно,             return 'POST_NOT_FOUND'
                if function_name not in FuncNames.all_funcs():
                return 'FUNC_NOT_FOUND'
                if self.top_object.set_function(post_name, function_name):
                    return 'OK'
                    return 'FAIL'
                """
                try:
                    self.logger.info(f'start function `{function_name}` from post #{post_number} ')
                    return self.start_function(post_number, function_name)
                except:
                    self.logger.exception(f'get_state({post_number})')
                    return 'EXCEPTION'

            @server.register_function
            def stop_function(post_number):
                self.logger.info(f'function stop from post #{post_number} ')
                return self.start_function(post_number, FuncNames.STOP)

            @server.register_function
            def get_state(post_number):
                post_name = f'post_{post_number}'
                self.logger.debug(f'get state from post #{post_number} ')
                self.post_state.logger.info(f'get state from post #{post_number} ')
                try:
                    return {
                        'readiness': self.top_object.get_readiness_functions(post_name),
                        'function': self.top_object.get_post_function(post_name)
                    }
                except:
                    self.logger.exception(f'get_state({post_number})')
                    return 'EXCEPTION'

            @server.register_function
            def get_tagsrv_modules_state():
                modules = []
                for disp in self.tag_srv.dispatchers.values():
                    for m in disp.modules:
                        try:
                            values = m.tag_values()
                        except Exception as ex:
                            values = 'EXC'
                        modules.append({
                            'name': m.name,
                            'ok': m.ok,
                            'last_ok': round(time.time() - m.last_ok, 3),
                            'tags': values
                        })
                return modules

            server.register_multicall_functions()
            server.serve_forever()

    def start_function(self, post_number, function_name):
        post_name = f'post_{post_number}'
        post = self.top_object.find_child_by_name(post_name)
        if not post:
            return 'POST_NOT_FOUND'
        if function_name not in FuncNames.all_funcs():
            return 'FUNC_NOT_FOUND'
        if self.top_object.set_function(post_name, function_name):
            return 'OK'
        return 'FAIL'

