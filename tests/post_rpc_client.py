import time
import xmlrpc.client


class FuncNames:
    STOP = 'stop'
    INTENSIVE = 'intensive'
    FOAM = 'foam'
    SHAMPOO = 'shampoo'
    WAX = 'wax'
    OSMOSIS = 'osmosis'
    COLD_WATER = 'cold_water'
    HOT_WATER = 'hot_water'

    @classmethod
    def all_funcs(cls):
        return cls.STOP, cls.INTENSIVE, cls.FOAM, cls.SHAMPOO, cls.WAX, cls.OSMOSIS, cls.COLD_WATER, cls.HOT_WATER


class PostRpcClient(object):

    def __init__(self, host='http://localhost:9876'):
        self.server = xmlrpc.client.ServerProxy(host)

    def start_function(self, post, function):
        if isinstance(function, int):
            func = FuncNames.all_funcs()[function]
        else:
            func = function
        print('>> start_function', post, func)
        # запрос от поста номер {post: int} на запуск функции {func: str}
        # возвращает 'OK' - если команда принята
        # 'POST_NOT_FOUND' - если поста с таким номером нет
        # 'FUNC_NOT_FOUND' - если функции с таким именем нет
        print(self.server.start_function(post, func))

    def get_state(self, post):
        print('>> get_state', post)
        # запрос состояния поста номер {post: int}
        # возвращает json, пример:
        # {
        # 'readiness':
        #   {
        #       'wax': False,
        #       'shampoo': False,
        #       'foam': False,
        #       'intensive': False,
        #       'osmosis': False,
        #       'cold_water': False,
        #       'hot_water': False
        #   },
        #   'function': 'stop'
        # }
        #
        # readiness - отова ли ф-ция к работе
        # function - имя текущей ф-ции
        print(self.server.get_state(post))

    def multi(self, post, function):
        # Одним запросом вызываеи ф-цию start_function и get_state
        multicall = xmlrpc.client.MultiCall(self.server)
        if isinstance(function, int):
            func = FuncNames.all_funcs()[function]
        else:
            func = function
        print('>> start_function', post, func)
        multicall.start_function(post, func)
        print('>> get_state', post)
        multicall.get_state(post)
        for res in enumerate(multicall()):
            print(res)
