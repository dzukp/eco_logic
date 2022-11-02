from top_simulator import TopSimulator
from simple_simulators import TankSimulator


def get_simulator_objects(post_quantity):
    simulators = {
        'top_simulator': {
            'class': TopSimulator,
            'version': '1.1',
            'di_valve_b1': 'do_2_19',
            'di_valve_b3': 'do_1_24',
            'di_n1': 'do_1_19',
            'ao_p1': 'ai_2_5',
            'ao_p2': 'ai_2_6',
            'do_press1': None,
            'di_water_os': 'do_1_23',
            'do_press2': None,
            'di_os1': 'do_1_21',
            'di_os2': None,
            'di_valve_b2': None,
            'di_n2': 'do_1_20',
            'ao_p3': 'ai_2_4',
            'do_press3': None,
            'di_n3': 'do_1_21',
            'do_press4': 'di_1_6',
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
                },
                'b3': {
                    'class': TankSimulator,
                    'do_low': 'di_1_7',
                    'do_mid': 'di_1_8',
                    'do_hi': 'di_1_9',
                }
            }
        }
    }
    return simulators
