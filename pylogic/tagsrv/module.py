
class BaseModule(object):

    def __init__(self, *args, **kwargs):
        self.name = kwargs.get('name')
        self.ok = False
        self.last_ok = 0

    def process(self):
        pass
