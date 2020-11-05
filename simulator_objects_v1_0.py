from top_simulator import TopSimulator
from simple_simulators import TankSimulator


def get_simulator_objects(post_quantity=8):
    simulators = {
        'top_simulator': {
            'class': TopSimulator,
            'di_valve_b1': ('do_2_18', 'do_2_20')[post_quantity // 5],
            'di_n1': 'do_2_13',
            'ao_p1': ('ai_1_5', 'ai_2_1')[post_quantity // 5],
            'ao_p2': ('ai_1_6', 'ai_2_2')[post_quantity // 5],
            'do_press1': 'di_1_7',
            'di_water_os': ('do_2_17', 'do_2_18')[post_quantity // 5],
            'do_press2': 'di_1_8',
            'di_os1': 'do_2_15',
            'di_os2': (None, 'do_2_16')[post_quantity // 5],
            'di_valve_b2': ('do_2_19', 'do_2_21')[post_quantity // 5],
            'di_n2': 'do_2_14',
            'ao_p3': ('ai_1_7', 'ai_2_3')[post_quantity // 5],
            'do_press3': 'di_1_9',
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
    return simulators