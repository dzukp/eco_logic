from pylogic.tagsrv.tagsrv import InTag, OutTag
from pylogic.tagsrv.module_dispatcher import ParallelDispatcher
from pylogic.tagsrv.owen_mx210 import OwenAiMv210, OwenAoMu210, OwenDiMv210, OwenDoMu210_403, OwenDiDoMk210


tags = {
    'in': {
        'ai_1_0': InTag(0),
    },
    'out': {}
}

module_tags = {}

# generate ai_1_1 - ai_2_8
for pref in ('ai_1_','ai_2_',):
    tags['in'].update(dict([(pref + str(i), InTag(i)) for i in range(8)]))

# generate do_1_1 - do_4_24
for pref in ('do_1_', 'do_2_', 'do_3_', 'do_4_'):
    tags['out'].update(dict([(pref + str(i), OutTag(i)) for i in range(1, 25)]))

# generate di_1_1 - do_1_20
for pref in ('di_1_',):
    tags['in'].update(dict([(pref + str(i), InTag(i)) for i in range(1, 21)]))


ai_1 = OwenAiMv210(tags=[tag for name, tag in tags['in'].items() if name.startswith('ai_1_')], ip='192.168.1.105',
                       timeout=0.03)
ai_2 = OwenAiMv210(tags=[tag for name, tag in tags['in'].items() if name.startswith('ai_2_')], ip='192.168.1.2',
                       timeout=0.03)
di_1 = OwenDiMv210(tags=[tag for name, tag in tags['in'].items() if name.startswith('di_1_')], ip='192.168.1.2',
                       timeout=0.03)
# ao_0 = OwenAoMu210(tags=tags_ao_0, ip='192.168.1.2')
do_1 = OwenDoMu210_403(tags=[tag for name, tag in tags['out'].items() if name.startswith('do_1_')], ip='192.168.1.100',
                       timeout=0.03)
do_2 = OwenDoMu210_403(tags=[tag for name, tag in tags['out'].items() if name.startswith('do_2_')], ip='192.168.1.2',
                       timeout=0.03)
do_3 = OwenDoMu210_403(tags=[tag for name, tag in tags['out'].items() if name.startswith('do_3_')], ip='192.168.1.2',
                       timeout=0.03)
do_4 = OwenDoMu210_403(tags=[tag for name, tag in tags['out'].items() if name.startswith('do_4_')], ip='192.168.1.2',
                       timeout=0.03)


dispatchers = {
    'disp_1': ParallelDispatcher(
        modules=[do_1, do_2, do_3, do_4, di_1, ai_1, ai_2]
    )
}

settings = {
    'tags': tags,
    'sources': {},
    'dispatchers': dispatchers
}
