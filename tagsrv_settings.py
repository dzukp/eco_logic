from pylogic.tagsrv.tagsrv import InTag, OutTag
from pylogic.tagsrv.module_dispatcher import ParallelDispatcher, SerialDispatcher
from pylogic.tagsrv.owen_mx210 import OwenAiMv210, OwenDiMv210, OwenDoMu210_403, OwenDiDoMk210
from pylogic.tagsrv.modbusrtu import ModbusRTUModule
from pylogic.tagsrv.serialsource import SerialSource

import os


def gen_tagsrv_config(post_quantity=(6, 6)):
    tags = {
        'in': {},
        'out': {}
    }

    ai_names = ('ai_1_1_', 'ai_1_2_', 'ai_2_1_', 'ai_2_2_', 'ai_3_')
    do_names = ('do_1_1_', 'do_1_2_', 'do_1_3_', 'do_2_1_', 'do_2_2_', 'do_2_3_')
    di_names = ('di_1_', 'di_2_')
    dio_names = ('dio_1_1_', 'dio_2_1_', 'dio_3_')
    dio_names2 = tuple([f'dio_p_{i}_' for i in range(1, 13)] + ['dio_4_'])
    fc_names = tuple([
        f'fc_1_{i}_' for i in range(1, int(post_quantity[0] + 1))] + [
        f'fc_2_{i}_' for i in range(1, int(post_quantity[1] + 1))] + [
        f'fc_os_', 'fc_hoover_1_', 'fc_hoover_2_']
    )

    # generate ai_1_1 - ai_2_8
    for pref in ai_names:
        tags['in'].update(dict([(pref + str(i), InTag(i)) for i in range(1, 9)]))

    # generate do_1_1_1 - do_2_3_24
    for pref in do_names:
        tags['out'].update(dict([(pref + str(i), OutTag(i)) for i in range(1, 25)]))

    # generate di_1_1_1 - di_2_1_20
    for pref in di_names:
        tags['in'].update(dict([(pref + str(i), InTag(i)) for i in range(1, 21)]))

    # generate dio_1_1_i_1 - di_2_1_i_12
    # generate dio_1_1_o_1 - di_2_1_o_4
    for pref in dio_names:
        tags['in'].update(dict([(f'{pref}i_{i}', InTag(i)) for i in range(1, 13)]))
        tags['out'].update(dict([(f'{pref}o_{i}', OutTag(i)) for i in range(1, 5)]))
    # generate dio_1_i_1 - di_12_i_12
    # generate dio_1_o_1 - di_12_o_4
    for pref in dio_names2:
        tags['in'].update(dict([(f'{pref}i_{i}', InTag(i)) for i in range(1, 7)]))
        tags['out'].update(dict([(f'{pref}o_{i}', OutTag(i)) for i in range(1, 9)]))

    # generate fc1_ai_1 - fc8_ai_3, fc1_ao_1 - fc8_ao_2
    for pref in fc_names:
        tags['in'].update(dict([(f'{pref}ai_{i}', InTag(0x1875 + i - 1)) for i in range(1, 5)]))
        tags['out'].update(dict([(f'{pref}ao_{i}', OutTag(0x1870 + i - 1)) for i in range(1, 3)]))

    ai_1_1 = OwenAiMv210(tags=[tag for name, tag in tags['in'].items() if name.startswith('ai_1_1_')],
                         ip='192.168.200.20', timeout=0.03)
    ai_1_2 = OwenAiMv210(tags=[tag for name, tag in tags['in'].items() if name.startswith('ai_1_2_')],
                         ip='192.168.200.22', timeout=0.03)
    ai_2_1 = OwenAiMv210(tags=[tag for name, tag in tags['in'].items() if name.startswith('ai_2_1_')],
                         ip='192.168.200.21', timeout=0.03)
    ai_2_2 = OwenAiMv210(tags=[tag for name, tag in tags['in'].items() if name.startswith('ai_2_2_')],
                         ip='192.168.200.23', timeout=0.03)
    ai_3 = OwenAiMv210(tags=[tag for name, tag in tags['in'].items() if name.startswith('ai_3_')],
                       ip='192.168.200.81', timeout=0.03)

    di_1_1 = OwenDiMv210(tags=[tag for name, tag in tags['in'].items() if name.startswith('di_1_')],
                         ip='192.168.200.10', timeout=0.03)
    di_2_1 = OwenDiMv210(tags=[tag for name, tag in tags['in'].items() if name.startswith('di_2_')],
                         ip='192.168.200.11', timeout=0.03)

    do_1_1 = OwenDoMu210_403(tags=[tag for name, tag in tags['out'].items() if name.startswith('do_1_1_')],
                             ip='192.168.200.1', timeout=0.03)
    do_1_2 = OwenDoMu210_403(tags=[tag for name, tag in tags['out'].items() if name.startswith('do_1_2_')],
                             ip='192.168.200.2', timeout=0.03)
    do_1_3 = OwenDoMu210_403(tags=[tag for name, tag in tags['out'].items() if name.startswith('do_1_3_')],
                             ip='192.168.200.3', timeout=0.03)
    do_2_1 = OwenDoMu210_403(tags=[tag for name, tag in tags['out'].items() if name.startswith('do_2_1_')],
                             ip='192.168.200.4', timeout=0.03)
    do_2_2 = OwenDoMu210_403(tags=[tag for name, tag in tags['out'].items() if name.startswith('do_2_2_')],
                             ip='192.168.200.5', timeout=0.03)
    do_2_3 = OwenDoMu210_403(tags=[tag for name, tag in tags['out'].items() if name.startswith('do_2_3_')],
                             ip='192.168.200.6', timeout=0.03)

    # dio_tags = [tag for name, tag in tags['out'].items() if name.startswith('dio_1_1_')] + \
    #            [tag for name, tag in tags['in'].items() if name.startswith('dio_1_1_')]
    # dio_1_1 = OwenDiDoMk210(tags=dio_tags, ip='192.168.200.30', timeout=0.03)
    # dio_tags = [tag for name, tag in tags['out'].items() if name.startswith('dio_2_1_')] + \
    #            [tag for name, tag in tags['in'].items() if name.startswith('dio_2_1_')]
    # dio_2_1 = OwenDiDoMk210(tags=dio_tags, ip='192.168.200.31', timeout=0.03)
    dio_tags = [tag for name, tag in tags['out'].items() if name.startswith('dio_3_')] + \
               [tag for name, tag in tags['in'].items() if name.startswith('dio_3_')]
    dio_3 = OwenDiDoMk210(tags=dio_tags, ip='192.168.200.80', timeout=0.03)
    dio_tags = [tag for name, tag in tags['out'].items() if name.startswith('dio_4_')] + \
               [tag for name, tag in tags['in'].items() if name.startswith('dio_4_')]
    dio_4 = OwenDiDoMk210(tags=dio_tags, ip='192.168.200.90', timeout=0.03)

    dio_post = []
    for i in range(1, sum(post_quantity) + 1):
        dio_tags = [tag for name, tag in tags['out'].items() if name.startswith(f'dio_p_{i}_')] + \
                   [tag for name, tag in tags['in'].items() if name.startswith(f'dio_p_{i}_')]
        dio_post.append(OwenDiDoMk210(tags=dio_tags, ip=f'192.168.200.{100 + i}', timeout=0.03))

    if os.name == 'posix':
        com_port1_name = 'fc1_serial'
        com_port2_name = 'fc2_serial'
        com_port3_name = 'fc3_serial'
    else:
        com_port1_name = 'COM3'
        com_port2_name = 'COM5'
        com_port3_name = 'COM4'

    ports = {1: SerialSource(port=com_port1_name, baudrate=19200, bytesize=8, parity='E', stopbits=1, timeout=0.1),
             2: SerialSource(port=com_port2_name, baudrate=19200, bytesize=8, parity='E', stopbits=1, timeout=0.1),
             3: SerialSource(port=com_port3_name, baudrate=19200, bytesize=8, parity='E', stopbits=1, timeout=0.1)}
    fc_modules = {1: [], 2: [], 3: []}

    slave = 0
    for section_num, section_post_quantity in enumerate(post_quantity, start=1):
        for i in range(1, section_post_quantity + 1):
            slave += 1
            fc_modules[section_num].append(ModbusRTUModule(slave, ports[section_num], io_tags=[], max_answ_len=5,
                                              in_tags=[tag for name, tag in tags['in'].items() if
                                                       name.startswith(f'fc_{section_num}_{i}_ai_')],
                                              out_tags=[tag for name, tag in tags['out'].items() if
                                                        name.startswith(f'fc_{section_num}_{i}_ao_')]))

    fc_modules[1].append(ModbusRTUModule(30, ports[1], io_tags=[], max_answ_len=5,
                                     in_tags=[tag for name, tag in tags['in'].items() if
                                              name.startswith(f'fc_os_ai_')],
                                     out_tags=[tag for name, tag in tags['out'].items() if
                                               name.startswith(f'fc_os_ao_')]))

    fc_modules[3].append(ModbusRTUModule(40, ports[3], io_tags=[], max_answ_len=5,
                                         in_tags=[tag for name, tag in tags['in'].items() if
                                                  name.startswith(f'fc_hoover_1_ai_')],
                                         out_tags=[tag for name, tag in tags['out'].items() if
                                                   name.startswith(f'fc_hoover_1_ao_')]))
    fc_modules[3].append(ModbusRTUModule(41, ports[3], io_tags=[], max_answ_len=5,
                                         in_tags=[tag for name, tag in tags['in'].items() if
                                                  name.startswith(f'fc_hoover_2_ai_')],
                                         out_tags=[tag for name, tag in tags['out'].items() if
                                                   name.startswith(f'fc_hoover_2_ao_')]))

    modules = [do_1_1, do_1_2, do_1_3, do_2_1, do_2_2, do_2_3, di_1_1, di_2_1, ai_1_1, ai_1_2, ai_2_1, ai_2_2, ai_3,
               dio_3, dio_4] + dio_post

    dispatchers = {
        'disp_1': ParallelDispatcher(
            modules=modules
        ),
        'mb_disp_1': SerialDispatcher(modules=fc_modules[1]),
        'mb_disp_2': SerialDispatcher(modules=fc_modules[2]),
        'mb_disp_3': SerialDispatcher(modules=fc_modules[3])
    }

    return {
        'tags': tags,
        'sources': {'port_1': ports[1], 'port_2': ports[2]},
        'dispatchers': dispatchers
    }
