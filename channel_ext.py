from pylogic.channel import InChannel
import time


class InChannelExt(InChannel):

    def __init__(self, *args):
        super(InChannelExt, self).__init__(*args)
        self.values = []
        self.last_time = 0.0
        self.time_limit = 1.0

    def set_value(self, value):
        super(InChannelExt, self).set_value(value)
        self.tick(value)

    def tick(self, value):
        _time = time.time()
        if _time - self.last_time > 0.001:
            self.values.append((value, _time))
            self.values = self.values_filter(_time)
        self.last_time = _time

    def values_filter(self, _time):
        return list(filter(lambda t: _time - t[1] < self.time_limit, self.values))

    def rate(self):
        values = self.values_filter(time.time())
        if len(values) < 3:
            return 0
        dtime = values[-1][1] - values[0][1]
        if dtime < 0.25:
            return 0
        speeds = []
        for v1, v2, in zip(values[:-1], values[1:]):
            speeds.append((v2[0] - v1[0]) / (v2[1] - v1[1]))
        return sum(speeds) / len(speeds)
