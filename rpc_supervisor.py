from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import threading
import logging

from pylogic.supervisor_manager import BaseSupervisor
from pylogic.logged_object import LoggedObject
from rpc_post_server import RpcPostServer


class RpcSupervisor(BaseSupervisor):

    def __init__(self, name):
        super().__init__(name)
        self.rpc_server = RpcPostServer()

    def init(self):
        self.rpc_server.set_top_object(self.top_object)
        self.rpc_server.set_tag_server(self.tag_srv)
        self.rpc_server.start()

    def receive_data(self):
        pass

    def send_data(self):
        pass
