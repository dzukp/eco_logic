from pylogic.tagsrv.tagsrv import InTag, OutTag
from pylogic.tagsrv.module_dispatcher import ParallelDispatcher, SerialDispatcher
from pylogic.tagsrv.owen_mx210 import OwenAiMv210, OwenDiMv210, OwenDoMu210_403, OwenDiDoMk210
from pylogic.tagsrv.modbusrtu import ModbusRTUModule
from pylogic.tagsrv.serialsource import SerialSource

import settings


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
        ai_names = ('ai_1_', 'ai_2_', 'ai_3_', 'ai_4_')
        do_names = ('do_1_', 'do_2_', 'do_3_', 'do_4_', 'do_5_')
    else:
        ai_names = ('ai_1_',)
        do_names = ('do_1_', 'do_2_')
    fc_names = [f'fc_{i}_' for i in range(1, post_quantity + 1)]

    if version in ('1.1', '1.2', '1.5'):
        fc_names.append('fc_os_')

    if version in ('1.2',):
        fc_names.append('fc_foam_1_')
        fc_names.append('fc_foam_2_')
        fc_names.append('fc_water_')
        fc_names.append('fc_osmos_')

    if version in ('1.4',):
        fc_names.append('fc_water_')
        fc_names.append('fc_osmos_')

    # generate ai_1_1 - ai_2_8
    for pref in ai_names:
        tags['in'].update(dict([(pref + str(i), InTag(i)) for i in range(1, 9)]))

    # generate do_1_1 - do_4_24
    for pref in do_names:
        tags['out'].update(dict([(pref + str(i), OutTag(i)) for i in range(1, 25)]))

    if version in ('1.2', '1.4'):
        for pref in ('dio_1_',):
            tags['in'].update(dict([(pref + 'i_' + str(i), InTag(i)) for i in range(1, 13)]))
            tags['out'].update(dict([(pref + 'o_' + str(i), OutTag(i)) for i in range(1, 9)]))

    if version in ('1.0', '1.2', '1.4', '1.5'):
        # generate di_1_1 - do_1_20
        for pref in ('di_1_',):
            tags['in'].update(dict([(pref + str(i), InTag(i)) for i in range(1, 21)]))
    else:
        for pref in ('di_1_',):
            tags['in'].update(dict([(pref + str(i), InTag(i)) for i in range(1, 13)]))

    for pref in fc_names:
        tags['in'].update({
            f'{pref}ai_1': InTag(0x3000),
            f'{pref}ai_2': InTag(0x1001),
            f'{pref}ai_3': InTag(0x8000),

        })
        tags['out'].update({
            f'{pref}ao_1': OutTag(0x2000),
            f'{pref}ao_2': OutTag(0x1000)
        })

    ai_1 = OwenAiMv210(tags=[tag for name, tag in tags['in'].items() if name.startswith('ai_1_')], ip='192.168.200.11',
                       timeout=0.03)
    ai_2 = OwenAiMv210(tags=[tag for name, tag in tags['in'].items() if name.startswith('ai_2_')], ip='192.168.200.12',
                       timeout=0.03)
    ai_3 = OwenAiMv210(tags=[tag for name, tag in tags['in'].items() if name.startswith('ai_3_')], ip='192.168.200.13',
                       timeout=0.03)
    ai_4 = OwenAiMv210(tags=[tag for name, tag in tags['in'].items() if name.startswith('ai_4_')], ip='192.168.200.14',
                       timeout=0.03)
    if version in ('1.0', '1.2', '1.4', '1.5'):
        di_1 = OwenDiMv210(tags=[tag for name, tag in tags['in'].items() if name.startswith('di_1_')],
                           ip='192.168.200.16', timeout=0.03)
    else:
        di_1 = OwenDiDoMk210(tags=[tag for name, tag in tags['in'].items() if name.startswith('di_1_')],
                             ip='192.168.200.30', timeout=0.03)

    dio_1 = None
    if version in ('1.2', '1.4'):
        dio_tags = [tag for name, tag in tags['in'].items() if name.startswith('dio_1_i_')] + \
                   [tag for name, tag in tags['out'].items() if name.startswith('dio_1_o_')]
        dio_1 = OwenDiDoMk210(tags=dio_tags, ip='192.168.200.15', timeout=0.03)
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

    com_port1_name = settings.COM1
    com_port2_name = settings.COM2

    # if quantity pumps > 4 use both serial ports
    if version in ('1.2', '1.4', '1.5'):
        com1_end = 6
    elif post_quantity > 4:
        com1_end = post_quantity // 2
    else:
        com1_end = post_quantity

    sources = {
        'port_1': SerialSource(port=com_port1_name, baudrate=19200, bytesize=8, parity='E', stopbits=1, timeout=0.1)
    }

    if post_quantity > com1_end:
        sources['port_2'] = SerialSource(port=com_port2_name, baudrate=19200, bytesize=8, parity='E', stopbits=1,
                                         timeout=0.1)

    fc_modules_1 = []
    fc_modules_2 = []
    for i in range(1, com1_end + 1):
        fc_modules_1.append(ModbusRTUModule(i, sources['port_1'], io_tags=[], max_answ_len=5,
                                          in_tags=[tag for name, tag in tags['in'].items() if
                                                   name.startswith(f'fc_{i}_ai_')],
                                          out_tags=[tag for name, tag in tags['out'].items() if
                                                    name.startswith(f'fc_{i}_ao_')]))

    if version in ('1.2', '1.4'):
        fc_module = fc_modules_2 if post_quantity > com1_end else fc_modules_1
        comport = sources['port_2'] if post_quantity > com1_end else sources['port_1']

        in_tags = [tag for name, tag in tags['in'].items() if name.startswith(f'fc_foam_1_ai_')]
        out_tags = [tag for name, tag in tags['out'].items() if name.startswith(f'fc_foam_1_ao_')]
        if in_tags or out_tags:
            fc_modules_1.append(ModbusRTUModule(
                50, sources['port_1'], io_tags=[], max_answ_len=5, in_tags=in_tags, out_tags=out_tags))

        in_tags = [tag for name, tag in tags['in'].items() if name.startswith(f'fc_foam_2_ai_')]
        out_tags = [tag for name, tag in tags['out'].items() if name.startswith(f'fc_foam_2_ao_')]
        if in_tags or out_tags:
            fc_module.append(ModbusRTUModule(
                51, comport, io_tags=[], max_answ_len=5, in_tags=in_tags, out_tags=out_tags))

        in_tags = [tag for name, tag in tags['in'].items() if name.startswith(f'fc_osmos_ai_')]
        out_tags = [tag for name, tag in tags['out'].items() if name.startswith(f'fc_osmos_ao_')]
        if in_tags or out_tags:
            fc_module.append(ModbusRTUModule(
                11, comport, io_tags=[], max_answ_len=5, in_tags=in_tags, out_tags=out_tags))

        in_tags = [tag for name, tag in tags['in'].items() if name.startswith(f'fc_water_ai_')]
        out_tags = [tag for name, tag in tags['out'].items() if name.startswith(f'fc_water_ao_')]
        if in_tags or out_tags:
            fc_module.append(ModbusRTUModule(
                12, comport, io_tags=[], max_answ_len=5, in_tags=in_tags, out_tags=out_tags))

    for i in range(com1_end + 1, post_quantity + 1):
        in_tags = [tag for name, tag in tags['in'].items() if name.startswith(f'fc_{i}_ai_')]
        out_tags = [tag for name, tag in tags['out'].items() if name.startswith(f'fc_{i}_ao_')]
        fc_modules_2.append(ModbusRTUModule(
            i, sources['port_2'], io_tags=[], max_answ_len=5, in_tags=in_tags, out_tags=out_tags))

    if version in ('1.1', '1.2', '1.4', '1.5'):
        comport = sources['port_2'] if post_quantity > com1_end else sources['port_1']
        fc_module = fc_modules_2 if post_quantity > com1_end else fc_modules_1
        in_tags = [tag for name, tag in tags['in'].items() if name.startswith(f'fc_os_ai_')]
        out_tags = [tag for name, tag in tags['out'].items() if name.startswith(f'fc_os_ao_')]
        fc_module.append(ModbusRTUModule(13, comport, io_tags=[], max_answ_len=5, in_tags=in_tags, out_tags=out_tags))

    if post_quantity in (5, 6):
        modules = [do_1, do_2, do_3, di_1, ai_1, ai_2]
    elif post_quantity in (7, 8):
        modules = [do_1, do_2, do_3, do_4, di_1, ai_1, ai_2]
    elif post_quantity in (9, 10):
        modules = [do_1, do_2, do_3, do_4, do_5, di_1, ai_1, ai_2, ai_3]
        if version == '1.2':
            modules.append(ai_4)
    else:
        modules = [do_1, do_2, di_1, ai_1]
        if version == '1.2':
            modules.append(ai_4)

    if dio_1:
        modules.extend([dio_1])

    dispatchers = {
        'disp_1': ParallelDispatcher(
            modules=modules
        )
    }

    if fc_modules_1:
        dispatchers['mb_disp1'] = SerialDispatcher(modules=fc_modules_1)
    if fc_modules_2:
        dispatchers['mb_disp2'] = SerialDispatcher(modules=fc_modules_2)

    return {
        'tags': tags,
        'sources': sources,
        'dispatchers': dispatchers
    }
