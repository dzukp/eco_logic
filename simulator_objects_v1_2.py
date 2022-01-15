from top_simulator import TopSimulator
from simple_simulators import TankSimulator, FcSimulator


def get_simulator_objects(post_quantity):
    simulators = {
        'top_simulator': {
            'class': TopSimulator,
            'version': '1.2',
            'di_valve_b1': None,
            'di_n1': None,
            'ao_p1': 'ai_2_5',
            'ao_p2': 'ai_2_6',
            'do_press1': None,
            'di_water_os': None,
            'do_press2': None,
            'di_os1': None,
            'di_os2': None,
            'di_valve_b2': None,
            'di_n2': None,
            'ao_p3': 'ai_2_4',
            'do_press3': None,
            'di_n3': 'do_1_21',
            'do_press4': None,
            'children': {
                'b1': {
                    'class': TankSimulator,
                    'do_low': 'di_1_1',
                    'do_mid': 'di_1_2',
                    'do_hi': 'di_1_3',
                },
                'b2': {
                    'class': TankSimulator,
                    'do_low': 'di_1_4',
                    'do_mid': 'di_1_5',
                    'do_hi': 'di_1_6',
                }
            }
        }
    }

    for post in range(1, post_quantity + 1):
        if post <= 3:
            ai_press = f'ai_1_{post}'
        else:
            ai_press = f'ai_2_{post - 3}'
        simulators['top_simulator']['children'][f'fc_{post}'] = {
            'class': FcSimulator,
            'ai_cmd': f'fc_{post}_ao_1',
            'ai_freq': f'fc_{post}_ao_2',
            'ao_status': f'fc_{post}_ai_1',
            'ao_freq': f'fc_{post}_ai_2',
            'ao_pressure': ai_press
        }

    return simulators
