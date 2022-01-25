from pylogic.tagsrv.tagsrv import InTag, OutTag
from pylogic.tagsrv.module_dispatcher import ParallelDispatcher, SerialDispatcher
from pylogic.tagsrv.owen_mx210 import OwenAiMv210, OwenDiMv210, OwenDoMu210_403, OwenDiDoMk210
from pylogic.tagsrv.modbusrtu import ModbusRTUModule
from pylogic.tagsrv.serialsource import SerialSource

import os


def gen_tagsrv_config(version='1.0', post_quantity=8):
    tags = {
        'in': {},
        'out': {}
    }

    if post_quantity in (5, 6):
        ai_names = ('ai_1_', 'ai_2_',)
        do_names = ('do_1_', 'do_2_', 'do_3_')
    elif post_quantity in (7, 8):
        ai_names = ('ai_1_', 'ai_2_',)
        do_names = ('do_1_', 'do_2_', 'do_3_', 'do_4_')
    elif post_quantity in (9, 10):
        ai_names = ('ai_1_', 'ai_2_', 'ai_3_',)
        do_names = ('do_1_', 'do_2_', 'do_3_', 'do_4_', 'do_5_')
    else:
        ai_names = ('ai_1_',)
        do_names = ('do_1_', 'do_2_')
    fc_names = [f'fc_{i}_' for i in range(1, post_quantity + 1)]

    if version in ('1.1',):
        fc_names.append('fc_os_')

    if version in ('1.2',):
        fc_names.append('fc_foam_1_')
        fc_names.append('fc_foam_2_')

    # generate ai_1_1 - ai_2_8
    for pref in ai_names:
        tags['in'].update(dict([(pref + str(i), InTag(i)) for i in range(1, 9)]))

    # generate do_1_1 - do_4_24
    for pref in do_names:
        tags['out'].update(dict([(pref + str(i), OutTag(i)) for i in range(1, 25)]))

    if version == '1.2':
        for pref in ('dio_1_',):
            tags['in'].update(dict([(pref + 'i_' + str(i), InTag(i)) for i in range(1, 13)]))
            tags['out'].update(dict([(pref + 'o_' + str(i), OutTag(i)) for i in range(1, 5)]))

    if version in ('1.0', '1.2'):
        # generate di_1_1 - do_1_20
        for pref in ('di_1_',):
            tags['in'].update(dict([(pref + str(i), InTag(i)) for i in range(1, 21)]))
    else:
        for pref in ('di_1_',):
            tags['in'].update(dict([(pref + str(i), InTag(i)) for i in range(1, 13)]))

    # generate fc1_ai_1 - fc8_ai_3, fc1_ao_1 - fc8_ao_2
    for pref in fc_names:
        tags['in'].update(dict([(f'{pref}ai_{i}', InTag(0x1875 + i - 1)) for i in range(1, 5)]))
        tags['out'].update(dict([(f'{pref}ao_{i}', OutTag(0x1870 + i - 1)) for i in range(1, 3)]))

    ai_1 = OwenAiMv210(tags=[tag for name, tag in tags['in'].items() if name.startswith('ai_1_')], ip='192.168.200.11',
                       timeout=0.03)
    ai_2 = OwenAiMv210(tags=[tag for name, tag in tags['in'].items() if name.startswith('ai_2_')], ip='192.168.200.12',
                       timeout=0.03)
    ai_3 = OwenAiMv210(tags=[tag for name, tag in tags['in'].items() if name.startswith('ai_3_')], ip='192.168.200.13',
                       timeout=0.03)
    if version in ('1.0', '1.2'):
        di_1 = OwenDiMv210(tags=[tag for name, tag in tags['in'].items() if name.startswith('di_1_')], ip='192.168.200.10', timeout=0.03)
    else:
        di_1 = OwenDiDoMk210(tags=[tag for name, tag in tags['in'].items() if name.startswith('di_1_')], ip='192.168.200.30', timeout=0.03)

    dio_1 = None
    if version == '1.2':
        dio_tags = [tag for name, tag in tags['in'].items() if name.startswith('dio_1_i_')] + \
                   [tag for name, tag in tags['out'].items() if name.startswith('dio_1_o_')]
        dio_1 = OwenDiDoMk210(tags=dio_tags, ip='192.168.200.40', timeout=0.03)
    # ao_0 = OwenAoMu210(tags=tags_ao_0, ip='192.168.1.2')
    do_1 = OwenDoMu210_403(tags=[tag for name, tag in tags['out'].items() if name.startswith('do_1_')], ip='192.168.200.1',
                           timeout=0.03)
    do_2 = OwenDoMu210_403(tags=[tag for name, tag in tags['out'].items() if name.startswith('do_2_')], ip='192.168.200.2',
                           timeout=0.03)
    do_3 = OwenDoMu210_403(tags=[tag for name, tag in tags['out'].items() if name.startswith('do_3_')], ip='192.168.200.3',
                           timeout=0.03)
    do_4 = OwenDoMu210_403(tags=[tag for name, tag in tags['out'].items() if name.startswith('do_4_')], ip='192.168.200.4',
                           timeout=0.03)
    do_5 = OwenDoMu210_403(tags=[tag for name, tag in tags['out'].items() if name.startswith('do_5_')], ip='192.168.200.5',
                           timeout=0.03)

    if os.name == 'posix':
        com_port1_name = 'fc_serial1'
        com_port2_name = 'fc_serial2'
    else:
        com_port1_name = 'COM5'
        com_port2_name = 'COM6'

    sources = {
        'port_1': SerialSource(port=com_port1_name, baudrate=19200, bytesize=8, parity='E', stopbits=1, timeout=0.1)
    }

    if post_quantity > 4:
        sources['port_2'] = SerialSource(port=com_port2_name, baudrate=19200, bytesize=8, parity='E', stopbits=1,
                                         timeout=0.1)

    fc_modules_1 = []
    fc_modules_2 = []

    # if quantity pumps > 4 use both serial ports
    if version == '1.2':
        com1_end = 6
    elif post_quantity > 4:
        com1_end = post_quantity // 2
    else:
        com1_end = post_quantity
    for i in range(1, com1_end + 1):
        fc_modules_1.append(ModbusRTUModule(i, sources['port_1'], io_tags=[], max_answ_len=5,
                                          in_tags=[tag for name, tag in tags['in'].items() if
                                                   name.startswith(f'fc_{i}_ai_')],
                                          out_tags=[tag for name, tag in tags['out'].items() if
                                                    name.startswith(f'fc_{i}_ao_')]))

    if version in ('1.2',):
        fc_modules_1.append(ModbusRTUModule(50, sources['port_1'], io_tags=[], max_answ_len=5,
                                              in_tags=[tag for name, tag in tags['in'].items() if
                                                       name.startswith(f'fc_foam_1_ai_')],
                                              out_tags=[tag for name, tag in tags['out'].items() if
                                                        name.startswith(f'fc_foam_1_ao_')]))
        fc_modules_2.append(ModbusRTUModule(51, sources['port_2'], io_tags=[], max_answ_len=5,
                                              in_tags=[tag for name, tag in tags['in'].items() if
                                                       name.startswith(f'fc_foam_2_ai_')],
                                              out_tags=[tag for name, tag in tags['out'].items() if
                                                        name.startswith(f'fc_foam_2_ao_')]))

    for i in range(com1_end + 1, post_quantity + 1):
        fc_modules_2.append(ModbusRTUModule(i, sources['port_2'], io_tags=[], max_answ_len=5,
                                          in_tags=[tag for name, tag in tags['in'].items() if
                                                   name.startswith(f'fc_{i}_ai_')],
                                          out_tags=[tag for name, tag in tags['out'].items() if
                                                    name.startswith(f'fc_{i}_ao_')]))

    if version in ('1.1',) and 'port_2' in sources:
        fc_modules_2.append(ModbusRTUModule(30, sources['port_2'], io_tags=[], max_answ_len=5,
                                          in_tags=[tag for name, tag in tags['in'].items() if
                                                   name.startswith(f'fc_os_ai_')],
                                          out_tags=[tag for name, tag in tags['out'].items() if
                                                    name.startswith(f'fc_os_ao_')]))

    if post_quantity in (5, 6):
        modules = [do_1, do_2, do_3, di_1, ai_1, ai_2]
    elif post_quantity in (7, 8):
        modules = [do_1, do_2, do_3, do_4, di_1, ai_1, ai_2]
    elif post_quantity in (9, 10):
        modules = [do_1, do_2, do_3, do_4, do_5, di_1, ai_1, ai_2, ai_3]
        if version == '1.2':
            modules.append(dio_1)
    else:
        modules = [do_1, do_2, di_1, ai_1]

    dispatchers = {
        'disp_1': ParallelDispatcher(
            modules=modules
        ),
        'mb_disp1': SerialDispatcher(modules=fc_modules_1),
        'mb_disp2': SerialDispatcher(modules=fc_modules_2)
    }

    return {
        'tags': tags,
        'sources': sources,
        'dispatchers': dispatchers
    }
