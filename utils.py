import struct


def floats_to_modbus_cells(float_data):
    format = 'f' * len(float_data)
    byte_data = struct.pack(format, *float_data)
    format = 'H' * (len(float_data) * 2)
    res = struct.unpack(format, byte_data)
    return list(res)


def modbus_cells_to_floats(mb_cells):
    format = 'H' * len(mb_cells)
    byte_data = struct.pack(format, *mb_cells)
    format = 'f' * int(len(mb_cells) / 2)
    res = struct.unpack(format, byte_data)
    return res