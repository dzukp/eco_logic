import copy

from pylogic.io_object import IoObject
from valve import Valve, NOValve
from engine import Engine
from fc import Altivar212
from tank import Tank
from post import Post
from waterpreparing import WaterPreparing
from nofrost import Nofrost
from subsystems import PidEngine
from top import Top


def get_object(post_quantity=10):
    objects = {
        'top': {
            'class': Top,
            'mb_cells_idx': 500,
            'children': {
                'supplier': {
                    'class': WaterPreparing,
                    'di_press_1': None,
                    'ai_pe_1': 'ai_2_5',
                    'di_press_2': None,
                    'ai_pe_2': 'ai_2_6',
                    'di_press_3': None,
                    'ai_pe_3': 'ai_2_4',
                    'di_press_4': None,
                    'do_no_n3_press_signal': None,
                    'mb_cells_idx': 0,
                    'children': {
                        'pump_n1': {
                            'class': Engine,
                            'do_start': None,
                            'mb_cells_idx': 30,
                        },
                        'pump_n1_2': {
                            'class': Engine,
                            'do_start': None,
                            'mb_cells_idx': 493,
                        },
                        'pump_n1_3': {
                            'class': Engine,
                            'do_start': None,
                            'mb_cells_idx': 495,
                        },
                        'pump_n2': {
                            'class': Engine,
                            'do_start': None,
                            'mb_cells_idx': 32
                        },
                        'pump_n3': {
                            'class': Engine,
                            'do_start': None,
                            'mb_cells_idx': 497
                        },
                        'pump_os1': {
                            'class': Engine,
                            'do_start': None,
                            'mb_cells_idx': 34
                        },
                        'pump_os2': {
                            'class': Engine,
                            'do_start': None,
                            'mb_cells_idx': None
                        },
                        'pump_os': {
                            'class': PidEngine,
                            'ai_sensor': None,
                            'mb_cells_idx': 471,
                            'children': {
                                'fc': {
                                    'class': Altivar212,
                                    # 'ao_command': 'fc_os_ao_1',
                                    # 'ao_frequency': 'fc_os_ao_2',
                                    # 'ai_status': 'fc_os_ai_1',
                                    # 'ai_frequency': 'fc_os_ai_2',
                                    # 'ai_alarm_code': 'fc_os_ai_3',
                                    # 'mb_cells_idx': 483
                                }
                            }
                        },
                        'pump_i1': {
                            'class': Engine,
                            'do_start': 'do_3_23',
                            'mb_cells_idx': 38
                        },
                        'valve_water_os': {
                            'class': Valve,
                            'do_open': None,
                            'mb_cells_idx': None
                        },
                        'valve_b1': {
                            'class': Valve,
                            'do_open': None,
                            'mb_cells_idx': 44
                        },
                        'valve_b2': {
                            'class': Valve,
                            'do_open': None,
                            'mb_cells_idx': None
                        },
                        'tank_b1': {
                            'class': Tank,
                            'di_low_level': 'di_1_1',
                            'di_mid_level': 'di_1_2',
                            'di_hi_level': 'di_1_3',
                            'mb_cells_idx': 48
                        },
                        'tank_b2': {
                            'class': Tank,
                            'di_low_level': 'di_1_4',
                            'di_mid_level': 'di_1_5',
                            'di_hi_level': 'di_1_6',
                            'mb_cells_idx': 50
                        },
                        'valve_dose_foam': {
                            'class': Valve,
                            'do_open': 'do_3_18',
                            'mb_cells_idx': 52
                        },
                        'valve_dose_wax': {
                            'class': Valve,
                            'do_open': 'do_3_19',
                            'mb_cells_idx': 54
                        },
                        'valve_dose_shampoo': {
                            'class': Valve,
                            'do_open': None,
                            'mb_cells_idx': None
                        },
                        'valve_dose_intensive': {
                            'class': Valve,
                            'do_open': 'do_3_16',
                            'mb_cells_idx': 58
                        },
                        'valve_dose_water_intensive': {
                            'class': Valve,
                            'do_open': 'do_3_15',
                            'mb_cells_idx': 56
                        },
                        'valve_dose_osmos_intensive': {
                            'class': Valve,
                            'do_open': 'do_3_14',
                            'mb_cells_idx': 40
                        },
                        'valve_dose_foam_2': {
                            'class': Valve,
                            'do_open': 'do_3_17',
                            'mb_cells_idx': 46
                        }
                    }
                }
            }
        }
    }

    post = {
        'class': Post,
        'ai_pressure': None,
        'di_flow': None,
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
            'valve_solution_2': {
                'class': Valve,
                'do_open': None
            },
            'pump': {
                'class': Altivar212,
                'ao_command': None,
                'ao_frequency': None,
                'ai_status': None,
                'ai_frequency': None,
                'ai_alarm_code': None,
                'mb_cells_idx': None
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
        # obj['children']['valve_out_foam']['mb_cells_idx'] = start_addr + 19
        obj['children']['valve_solution_2']['mb_cells_idx'] = start_addr + 19
        obj['children']['valve_intensive']['mb_cells_idx'] = start_addr + 21
        obj['children']['pump']['mb_cells_idx'] = start_addr + 23

        if post_number <= 3:
            obj['ai_pressure'] = f'ai_1_{post_number}'
        else:
            obj['ai_pressure'] = f'ai_2_{post_number - 3}'

        module_number = ((post_number - 1) // 3) + 1 if post_number <= 6 else ((post_number - 7) // 3) + 4
        obj['children']['valve_solution_2']['do_open'] = f'do_{module_number}_{(post_number - 1) % 3 * 8 + 1}'
        obj['children']['valve_wax']['do_open'] = f'do_{module_number}_{(post_number - 1) % 3 * 8 + 2}'
        obj['children']['valve_osmos']['do_open'] = f'do_{module_number}_{(post_number - 1) % 3 * 8 + 3}'
        obj['children']['valve_cold_water']['do_open'] = f'do_{module_number}_{(post_number - 1) % 3 * 8 + 4}'
        obj['children']['valve_hot_water']['do_open'] = f'do_{module_number}_{(post_number - 1) % 3 * 8 + 5}'
        obj['children']['valve_shampoo']['do_open'] = f'do_{module_number}_{(post_number - 1) % 3 * 8 + 6}'
        obj['children']['valve_out_water']['do_open'] = None
        obj['children']['valve_out_foam']['do_open'] = None
        if post_number <= 6:
            module2_number = 3
            obj['children']['valve_foam']['do_open'] = f'do_{module2_number}_{(post_number - 1) * 2 + 1}'
            obj['children']['valve_intensive']['do_open'] = f'do_{module2_number}_{(post_number - 1) * 2 + 2}'

        obj['children']['pump']['ao_command'] = f'fc_{post_number}_ao_1'
        obj['children']['pump']['ao_frequency'] = f'fc_{post_number}_ao_2'
        obj['children']['pump']['ai_status'] = f'fc_{post_number}_ai_1'
        obj['children']['pump']['ai_frequency'] = f'fc_{post_number}_ai_2'
        obj['children']['pump']['ai_alarm_code'] = None

    return objects
