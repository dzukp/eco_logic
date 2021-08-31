from pylogic.tagsrv.tagsrv import InTag, OutTag
from pylogic.tagsrv.module_dispatcher import ParallelDispatcher, SerialDispatcher
from pylogic.tagsrv.owen_mx210 import OwenAiMv210, OwenDiMv210, OwenDoMu210_403, OwenDiDoMk210
from pylogic.tagsrv.modbusrtu import ModbusRTUModule
from pylogic.tagsrv.serialsource import SerialSource

import os


def gen_tagsrv_config(post_quantity=8):
    tags = {
        'in': {},
        'out': {}
    }

    # if post_quantity in (5, 6, 7, 8):
    #     ai_names = ('ai_1_', 'ai_2_',)
    #     do_names = ('do_1_', 'do_2_', 'do_3_', 'do_4_')
    # else:
    #     ai_names = ('ai_1_',)
    #     do_names = ('do_1_', 'do_2_')
    fc_names = tuple([f'fc{i}_' for i in range(1, post_quantity + 1)])

    # ai_names = (,)
    do_names = ('do_1_', 'do_2_',)
    dio_names = ('dio_1_',)

    # generate ai_1_1 - ai_2_8
    # for pref in ai_names:
    #     tags['in'].update(dict([(pref + str(i), InTag(i)) for i in range(1, 9)]))

    # generate do_1_1 - do_4_24
    for pref in do_names:
        tags['out'].update(dict([(pref + str(i), OutTag(i)) for i in range(1, 25)]))

    # # generate di_1_1 - do_1_20
    # for pref in ('di_1_',):
    #     tags['in'].update(dict([(pref + str(i), InTag(i)) for i in range(1, 21)]))

    # generate dio_1_o_1 - dio_1_o_8, dio_1_i_1 - dio_1_i_6
    for pref in dio_names:
        tags['in'].update(dict([(f'{pref}i_{i}', InTag(i)) for i in range(1, 7)]))
        tags['out'].update(dict([(f'{pref}o_{i}', OutTag(i)) for i in range(1, 9)]))

    # generate fc1_ai_1 - fc8_ai_3, fc1_ao_1 - fc8_ao_2
    for pref in fc_names:
        tags['in'].update(
            {
                f'{pref}ai_1': InTag(50199),
                f'{pref}ai_2': InTag(50209)
            }
        )
        tags['out'].update(
            {
                f'{pref}ao_1': OutTag(49999),
                f'{pref}ao_2': OutTag(50009)
            }
        )

    # ai_1 = OwenAiMv210(tags=[tag for name, tag in tags['in'].items() if name.startswith('ai_1_')], ip='192.168.7.251',
    #                    timeout=0.03)
    # ai_2 = OwenAiMv210(tags=[tag for name, tag in tags['in'].items() if name.startswith('ai_2_')], ip='192.168.200.20',
    #                    timeout=0.03)
    dio_tags = [tag for name, tag in tags['out'].items() if name.startswith('dio_1_o_')] + \
               [tag for name, tag in tags['in'].items() if name.startswith('dio_1_i_')]
    dio_1 = OwenDiDoMk210(tags=dio_tags, ip='192.168.200.30', timeout=0.03)
    # di_1 = OwenDiMv210(tags=[tag for name, tag in tags['in'].items() if name.startswith('di_1_')], ip='192.168.200.10',
    #                    timeout=0.03)
    # ao_0 = OwenAoMu210(tags=tags_ao_0, ip='192.168.1.2')
    do_1 = OwenDoMu210_403(tags=[tag for name, tag in tags['out'].items() if name.startswith('do_1_')],
                           ip='192.168.200.1',
                           timeout=0.03)
    do_2 = OwenDoMu210_403(tags=[tag for name, tag in tags['out'].items() if name.startswith('do_2_')],
                           ip='192.168.200.2',
                           timeout=0.03)
    # do_3 = OwenDoMu210_403(tags=[tag for name, tag in tags['out'].items() if name.startswith('do_3_')],
    #                        ip='192.168.200.3',
    #                        timeout=0.03)
    # do_4 = OwenDoMu210_403(tags=[tag for name, tag in tags['out'].items() if name.startswith('do_4_')],
    #                        ip='192.168.200.4',
    #                        timeout=0.03)
    #
    if os.name == 'posix':
        com_port_name = 'fc_serial'
        com_port1_name = 'fc_serial1'
        com_port2_name = 'fc_serial2'
    else:
        com_port1_name = 'COM3'
        com_port2_name = 'COM4'

    port_1 = SerialSource(port=com_port1_name, baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=0.1)
    port_2 = SerialSource(port=com_port2_name, baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=0.1)

    fc_modules_1 = []
    fc_modules_2 = []

    for i in range(1, (post_quantity + 1 , 5)[post_quantity // 5]):
        fc_modules_1.append(ModbusRTUModule(i, port_1, io_tags=[], max_answ_len=5,
                                          in_tags=[tag for name, tag in tags['in'].items() if
                                                   name.startswith(f'fc{i}_ai_')],
                                          out_tags=[tag for name, tag in tags['out'].items() if
                                                    name.startswith(f'fc{i}_ao_')]))

    for i in range(5, post_quantity + 1):
        fc_modules_2.append(ModbusRTUModule(i, port_2, io_tags=[], max_answ_len=5,
                                          in_tags=[tag for name, tag in tags['in'].items() if
                                                   name.startswith(f'fc{i}_ai_')],
                                          out_tags=[tag for name, tag in tags['out'].items() if
                                                    name.startswith(f'fc{i}_ao_')]))

    # if post_quantity in (5, 6, 7, 8):
    #     modules = [do_1, do_2, do_3, do_4, di_1, ai_1, ai_2]
    # else:
    #     modules = [do_1, do_2, di_1, ai_1]

    dispatchers = {
        'disp_1': ParallelDispatcher(
            modules=(do_1, do_2, dio_1)
        ),
        'mb_disp1': SerialDispatcher(modules=fc_modules_1),
        'mb_disp2': SerialDispatcher(modules=fc_modules_2)
    }

    return {
        'tags': tags,
        'sources': {},
        'dispatchers': dispatchers
    }
