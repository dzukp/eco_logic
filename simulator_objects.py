from top_simulator import TopSimulator
from simple_simulators import TankSimulator


def get_simulator_objects(post_quantity):
    simulators = {
        'top_simulator': {
            'class': TopSimulator,
            'version': '2.0',
            'di_valve_b1': 'do_1_2_20',
            'di_n1': 'do_1_2_13',
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
            'di_n3': 'do_1_2_13',
            'do_press4': 'di_1_6',
            'children': {
                'b1': {
                    'class': TankSimulator,
                    'do_low': 'dio_1_1_i_3',
                    'do_mid': 'dio_1_1_i_2',
                    'do_hi': 'dio_1_1_i_1',
                },
                'b2': {
                    'class': TankSimulator,
                    'do_low': 'dio_1_1_i_6',
                    'do_mid': 'dio_1_1_i_5',
                    'do_hi': 'dio_1_1_i_4',
                }
            }
        }
    }
    return simulators
