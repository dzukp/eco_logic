import struct

from pylogic.tagsrv.modbusrtu import ModbusRTUModule


class CustomInnovanceMbRTUModule(ModbusRTUModule):

    class InTagRequest(ModbusRTUModule.InTagRequest):

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.ans_len = 6 + len(self.tags) * 2

        def ans_process(self, ans):
            quant = len(self.tags)
            data = struct.unpack(f'>{"H" * quant}', ans[4:4 + quant * 2])
            for tag, value in zip(self.tags, data):
                if tag.filter:
                    tag.value = tag.filter.apply(value)
                else:
                    tag.value = value

