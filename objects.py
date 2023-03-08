from pathlib import Path
import csv
import logging

from objects_v1_0 import get_object as get_object_v1_0
from objects_v1_1 import get_object as get_object_v1_1
from objects_v1_2 import get_object as get_object_v1_2
from simulator_objects_v1_0 import get_simulator_objects as get_simulator_objects_v1_0
from simulator_objects_v1_1 import get_simulator_objects as get_simulator_objects_v1_1
from simulator_objects_v1_2 import get_simulator_objects as get_simulator_objects_v1_2


def get_object(version='1.0', post_quantity=8):
    if version == '1.0':
        objs = get_object_v1_0(post_quantity)
    elif version == '1.1':
        objs = get_object_v1_1(post_quantity)
    elif version == '1.2':
        objs = get_object_v1_2(post_quantity)
    else:
        raise Exception('Need version')
    objs = extra_obj_attach(objs, 'change.csv')
    create_channels_file(objs, 'objects.csv')
    return objs


def get_simulator_object(version='1.0', post_quantity=8):
    if version == '1.0':
        return get_simulator_objects_v1_0(post_quantity)
    elif version == '1.1':
        return get_simulator_objects_v1_1(post_quantity)
    elif version == '1.2':
        return get_simulator_objects_v1_2(post_quantity)


def extra_obj_attach(objs, filename):
    path = Path('channels') / filename
    if path.exists():
        first_line = True
        with open(path) as fl:
            csv_reader = csv.reader(fl)
            for obj, channel, tag in csv_reader:
                if first_line:
                    first_line = False
                    continue
                else:
                    try:
                        o = {'children': objs}
                        for name in obj.split('.'):
                            o = o['children'][name]
                        o[channel] = tag
                    except KeyError:
                        logging.error(f'Bad {path} object "{obj}" not found')
                        raise
    return objs


def create_channels_file(objs, filename):
    def add_obj_channels(obj, path, content):
        for name, value in obj.items():
            if name.startswith('do_') or name.startswith('di_') or name.startswith('ao_') or name.startswith('ai_'):
                content.append((f'{path}', name, value or ''))
        for name, value in obj.get('children', {}).items():
            add_obj_channels(value, f'{path}.{name}', content)

    content = []
    for name, o in objs.items():
        add_obj_channels(o, name, content)
    dir = Path('channels')
    dir.mkdir(parents=True, exist_ok=True)
    filepath = dir / filename
    with open(filepath, 'w') as fl:
        csv_writer = csv.writer(fl)
        csv_writer.writerows([('object', 'channel', 'tag')] + content)
