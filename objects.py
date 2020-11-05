from objects_v1_0 import get_object as get_object_v1_0
from objects_v1_1 import get_object as get_object_v1_1
from simulator_objects_v1_0 import get_simulator_objects as get_simulator_objects_v1_0
from simulator_objects_v1_1 import get_simulator_objects as get_simulator_objects_v1_1


def get_object(version='1.0', post_quantity=8):
    if version == '1.0':
        return get_object_v1_0(post_quantity)
    elif version == '1.1':
        return get_object_v1_1(post_quantity)


def get_simulator_object(version='1.0', post_quantity=8):
    if version == '1.0':
        return get_simulator_objects_v1_0(post_quantity)
    elif version == '1.1':
        return get_simulator_objects_v1_1(post_quantity)
