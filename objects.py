import copy

from pylogic.io_object import IoObject
from valve import Valve, NOValve
from engine import Engine
from fc import Altivar212, DoFc
from tank import FakeTank
from post import Post
from waterpreparing import WaterPreparing
from nofrost import Nofrost
from top import Top


def get_object(post_quantity=8):
    post_quantity = max(post_quantity, 6)
    objects = {
        'top': {
            'class': Top,
            'mb_cells_idx': 320,
            'children': {
                'supplier': {
                    'class': WaterPreparing,
                    'di_press_1': 'di_1_7',
                    'ai_pe_1': 'ai_2_1',
                    'di_press_2': 'di_1_8',
                    'ai_pe_2': 'ai_2_3',
                    'di_press_3': 'di_1_9',
                    'ai_pe_3': 'ai_2_2',
                    'mb_cells_idx': 0,
                    'children': {
                        'pump_n1': {
                            'class': Engine,
                            'do_start': None,
                            'mb_cells_idx': 30,
                        },
                        'pump_n2': {
                            'class': Engine,
                            'do_start': None,
                            'mb_cells_idx': 32
                        },
                        'pump_os1': {
                            'class': Engine,
                            'do_start': None,
                            'mb_cells_idx': 34
                        },
                        'pump_os2': {
                            'class': Engine,
                            'do_start': None,
                            'mb_cells_idx': 36
                        },
                        'pump_i1': {
                            'class': Engine,
                            'do_start': None,
                            'mb_cells_idx': 38
                        },
                        'valve_water_os': {
                            'class': Valve,
                            'do_open': None,
                            'mb_cells_idx': 40
                        },
                        'valve_wash_osmos': {
                            'class': Valve,
                            'do_open': None,
                            'mb_cells_idx': 42
                        },
                        'valve_b1': {
                            'class': Valve,
                            'do_open': None,
                            'mb_cells_idx': 44
                        },
                        'valve_b2': {
                            'class': Valve,
                            'do_open': None,
                            'mb_cells_idx': 46
                        },
                        'tank_b1': {
                            'class': FakeTank,
                            'mb_cells_idx': 48
                        },
                        'tank_b2': {
                            'class': FakeTank,
                            'mb_cells_idx': 50
                        },
                        'valve_dose_foam': {
                            'class': Valve,
                            'do_open': None,
                            'mb_cells_idx': 52
                        },
                        'valve_dose_wax': {
                            'class': Valve,
                            'do_open': None,
                            'mb_cells_idx': 54
                        },
                        'valve_dose_shampoo': {
                            'class': Valve,
                            'do_open': None,
                            'mb_cells_idx': 56
                        },
                        'valve_dose_intensive': {
                            'class': Valve,
                            'do_open': None,
                            'mb_cells_idx': 58
                        }
                    }
                },
            }
        }
    }

    post = {
        'class': Post,
        'ai_pressure': None,
        'di_flow': None,
        'do_fc_1': None,
        'do_fc_2': None,
        'do_fc_3': None,
        'children': {
            'valve_foam': {
                'class': Valve,
                'do_open': None
            },
            'valve_wax': {
                'class': Valve,
                'do_open': None
            },
            'valve_shampoo': {
                'class': Valve,
                'do_open': None
            },
            'valve_cold_water': {
                'class': Valve,
                'do_open': None
            },
            'valve_hot_water': {
                'class': Valve,
                'do_open': None
            },
            'valve_osmos': {
                'class': Valve,
                'do_open': None
            },
            'valve_out_water': {
                'class': Valve,
                'do_open': None
            },
            'valve_out_foam': {
                'class': Valve,
                'do_open': None
            },
            'valve_intensive': {
                'class': Valve,
                'do_open': None
            },
            'pump': {
                'class': DoFc,
                'do_fc_1': None,
                'do_fc_2': None,
                'do_fc_3': None,
            }
        }
    }
    posts = dict([(f'post_{n}', copy.deepcopy(post)) for n in range(1, post_quantity + 1)])

    objects['top']['children'].update(posts)

    for name, obj in objects['top']['children'].items():
        if not name.startswith('post_'):
            continue
        post_number = int(name.lstrip('post_'))
        start_addr = 60 + (post_number - 1) * 32
        obj['mb_cells_idx'] = start_addr
        obj['children']['valve_foam']['mb_cells_idx'] = start_addr + 5
        obj['children']['valve_wax']['mb_cells_idx'] = start_addr + 7
        obj['children']['valve_shampoo']['mb_cells_idx'] = start_addr + 9
        obj['children']['valve_cold_water']['mb_cells_idx'] = start_addr + 11
        obj['children']['valve_hot_water']['mb_cells_idx'] = start_addr + 13
        obj['children']['valve_osmos']['mb_cells_idx'] = start_addr + 15
        obj['children']['valve_out_water']['mb_cells_idx'] = start_addr + 17
        obj['children']['valve_out_foam']['mb_cells_idx'] = start_addr + 19
        obj['children']['valve_intensive']['mb_cells_idx'] = start_addr + 21
        obj['children']['pump']['mb_cells_idx'] = start_addr + 23

        module_number = ((post_number - 1) // 4) + 1
        obj['children']['pump']['do_fc_1'] = f'do_3_{post_number}'
        obj['children']['pump']['do_fc_2'] = f'do_3_{post_number + 6}'
        obj['children']['pump']['do_fc_3'] = f'do_3_{post_number + 12}'
        obj['children']['valve_foam']['do_open'] = f'do_{module_number}_{(post_number - 1) % 4 * 6 + 1}'
        obj['children']['valve_wax']['do_open'] = f'do_{module_number}_{(post_number - 1) % 4 * 6 + 2}'
        obj['children']['valve_shampoo']['do_open'] = f'do_{module_number}_{(post_number - 1) % 4 * 6 + 3}'
        obj['children']['valve_cold_water']['do_open'] = f'do_{module_number}_{(post_number - 1) % 4 * 6 + 4}'
        obj['children']['valve_hot_water']['do_open'] = f'do_{module_number}_{(post_number - 1) % 4 * 6 + 5}'
        obj['children']['valve_osmos']['do_open'] = f'do_{module_number}_{(post_number - 1) % 4 * 6 + 6}'
        obj['children']['valve_intensive']['do_open'] = f'do_2_{18 + post_number}'
        obj['children']['valve_out_water']['do_open'] = None
        obj['children']['valve_out_foam']['do_open'] = f'do_2_{12 + post_number}'

    return objects
