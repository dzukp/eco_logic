from pylogic.tagsrv.tagsrv import InTag, OutTag
from pylogic.tagsrv.module_dispatcher import ParallelDispatcher, SerialDispatcher
from pylogic.tagsrv.owen_mx210 import OwenAiMv210, OwenDiMv210, OwenDoMu210_403
from pylogic.tagsrv.modbusrtu import ModbusRTUModule
from pylogic.tagsrv.serialsource import SerialSource


tags = {
    'in': {},
    'out': {}
}

# generate ai_1_1 - ai_2_8
for pref in ('ai_1_','ai_2_',):
    tags['in'].update(dict([(pref + str(i), InTag(i)) for i in range(1, 9)]))

# generate do_1_1 - do_4_24
for pref in ('do_1_', 'do_2_', 'do_3_', 'do_4_'):
    tags['out'].update(dict([(pref + str(i), OutTag(i)) for i in range(1, 25)]))

# generate di_1_1 - do_1_20
for pref in ('di_1_',):
    tags['in'].update(dict([(pref + str(i), InTag(i)) for i in range(1, 21)]))

# generate fc1_ai_1 - fc8_ai_3, fc1_ao_1 - fc8_ao_2
for pref in ('fc1_', 'fc2_', 'fc3_', 'fc4_', 'fc5_', 'fc6_', 'fc7_', 'fc8_'):
    tags['in'].update(dict([(f'{pref}ai_{i}', InTag(i)) for i in range(1, 4)]))
    tags['out'].update(dict([(f'{pref}ao_{i}', OutTag(i)) for i in range(1, 3)]))

ai_1 = OwenAiMv210(tags=[tag for name, tag in tags['in'].items() if name.startswith('ai_1_')], ip='192.168.200.20',
                       timeout=0.03)
ai_2 = OwenAiMv210(tags=[tag for name, tag in tags['in'].items() if name.startswith('ai_2_')], ip='192.168.200.21',
                       timeout=0.03)
di_1 = OwenDiMv210(tags=[tag for name, tag in tags['in'].items() if name.startswith('di_1_')], ip='192.168.200.10',
                       timeout=0.03)
# ao_0 = OwenAoMu210(tags=tags_ao_0, ip='192.168.1.2')
do_1 = OwenDoMu210_403(tags=[tag for name, tag in tags['out'].items() if name.startswith('do_1_')], ip='192.168.200.1',
                       timeout=0.03)
do_2 = OwenDoMu210_403(tags=[tag for name, tag in tags['out'].items() if name.startswith('do_2_')], ip='192.168.200.2',
                       timeout=0.03)
do_3 = OwenDoMu210_403(tags=[tag for name, tag in tags['out'].items() if name.startswith('do_3_')], ip='192.168.200.3',
                       timeout=0.03)
do_4 = OwenDoMu210_403(tags=[tag for name, tag in tags['out'].items() if name.startswith('do_4_')], ip='192.168.200.4',
                       timeout=0.03)

port_1 = SerialSource(port='COM3', baudrate=19200, bytesize=8, parity='N', stopbits=1)
fc_modules = []

for i in range(1, 9):
    fc_modules.append(ModbusRTUModule(1, port_1, io_tags=[], max_answ_len=5,
                           in_tags=[tag for name, tag in tags['in'].items() if name.startswith(f'fc{i}_ai_')],
                           out_tags=[tag for name, tag in tags['out'].items() if name.startswith(f'fc{i}_ao_')]))

dispatchers = {
    'disp_1': ParallelDispatcher(
        modules=[do_1, do_2, do_3, do_4, di_1, ai_1, ai_2]
    ),
    'mb_disp': SerialDispatcher(modules=fc_modules)
}

settings = {
    'tags': tags,
    'sources': {'port_1': port_1},
    'dispatchers': dispatchers
}
