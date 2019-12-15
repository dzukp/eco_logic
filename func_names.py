

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
