from top_simulator import TopSimulator
from simple_simulators import *


def get_simulator_objects(post_quantity):
    simulators = {
        'top_simulator': {
            'class': TopSimulator,
            'version': '2.0',
            'di_valve_b1': 'do_1_2_20',
            'di_n1': 'do_1_2_13',
            'di_n1_2': 'do_1_2_14',
            'ao_p1': 'ai_1_2_1',
            'ao_p2': 'ai_1_2_2',
            'do_press1': None,
            'di_water_os': None,
            'do_press2': None,
            'di_os1': None,
            'di_os2': None,
            'di_valve_b2': None,
            'di_n2': 'do_1_2_14',
            'ao_p3': 'ai_1_2_19',
            'do_press3': None,
            'di_n3': 'do_1_2_19',
            'do_press4': 'di_1_6',
            'ao_press_1': 'ai_1_1_1',
            'ao_p7': 'ai_2_2_1',
            'di_n7': 'do_2_2_13',
            'di_n7_1': 'do_2_2_14',
            'children': {
                'b1': {
                    'class': TankSimulator,
                    'do_low': 'di_1_3',
                    'do_mid': 'di_1_2',
                    'do_hi': 'di_1_1',
                },
                'b1_1': {
                    'class': TankSimulator,
                    'do_low': 'di_1_9',
                    'do_mid': 'di_1_8',
                    'do_hi': 'di_1_7',
                },
                'b2': {
                    'class': TankSimulator,
                    'do_low': 'di_1_6',
                    'do_mid': 'di_1_5',
                    'do_hi': 'di_1_4',
                },
                'hoover_fc1': {
                    'class': FcSimulator,
                    'ai_cmd': 'fc_hoover_1_ao_1',
                    'ai_freq': 'fc_hoover_1_ao_2',
                    'ao_status': 'fc_hoover_1_ai_1',
                    'ao_freq': 'fc_hoover_1_ai_2'
                },
                'hoover_fc2': {
                    'class': FcSimulator,
                    'ai_cmd': 'fc_hoover_2_ao_1',
                    'ai_freq': 'fc_hoover_2_ao_2',
                    'ao_status': 'fc_hoover_2_ai_1',
                    'ao_freq': 'fc_hoover_2_ai_2'
                }
            }
        }
    }

    side = 1
    for posts in post_quantity:
        for post in range(1, posts + 1):
            simulators['top_simulator']['children'][f'fc_{post * side}'] = {
                'class': FcSimulator,
                'ai_cmd': f'fc_{side}_{post}_ao_1',
                'ai_freq': f'fc_{side}_{post}_ao_2',
                'ao_status': f'fc_{side}_{post}_ai_1',
                'ao_freq': f'fc_{side}_{post}_ai_2'
            }
            simulators['top_simulator'][f'do_{post}_hoover'] = f'dio_p_{post}_i_1'
            simulators['top_simulator'][f'do_{post}_brush'] = f'dio_p_{post}_i_2'
            simulators['top_simulator'][f'do_{post}_car_inside'] = f'dio_p_{post}_i_3'
        side += 1

    return simulators
