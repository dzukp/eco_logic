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
from side_supplier import SideSupplier
from top import Top


def get_object(post_quantity=10):
    objects = {
        'top': {
            'class': Top,
            'mb_cells_idx': 500,
            'children': {
                'supplier': {
                    'class': WaterPreparing,
                    'sides': {},
                    'di_press_1': 'di_1_14',
                    'ai_pe_1': 'ai_1_6',
                    'di_press_2': None,
                    'ai_pe_2': 'ai_1_5',
                    'di_press_3': 'di_1_15',
                    'ai_pe_3': 'ai_1_7',
                    'di_press_4': 'di_1_13',
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
                        'pump_water_supplier': {
                            'class': PidEngine,
                            'ai_sensor': 'ai_1_5',
                            'mb_cells_idx': None,
                            'children': {
                                'fc': {
                                    'class': Altivar212,
                                    'ao_command': 'fc_water_ao_1',
                                    'ao_frequency': 'fc_water_ao_2',
                                    'ai_status': 'fc_water_ai_1',
                                    'ai_frequency': 'fc_water_ai_2',
                                    'ai_alarm_code': 'fc_water_ai_3',
                                    'mb_cells_idx': None
                                }
                            }
                        },
                        'pump_osmos_supplier': {
                            'class': PidEngine,
                            'ai_sensor': 'ai_1_7',
                            'mb_cells_idx': None,
                            'children': {
                                'fc': {
                                    'class': Altivar212,
                                    'ao_command': 'fc_osmos_ao_1',
                                    'ao_frequency': 'fc_osmos_ao_2',
                                    'ai_status': 'fc_osmos_ai_1',
                                    'ai_frequency': 'fc_osmos_ai_2',
                                    'ai_alarm_code': 'fc_osmos_ai_3',
                                    'mb_cells_idx': None
                                }
                            }
                        },
                        'pump_os1': {
                            'class': Engine,
                            'do_start': None,
                            'mb_cells_idx': None
                        },
                        'pump_os2': {
                            'class': Engine,
                            'do_start': None,
                            'mb_cells_idx': None
                        },
                        'pump_os': {
                            'class': PidEngine,
                            'ai_sensor': 'ai_4_1',
                            'mb_cells_idx': 471,
                            'children': {
                                'fc': {
                                    'class': Altivar212,
                                    'ao_command': 'fc_os_ao_1',
                                    'ao_frequency': 'fc_os_ao_2',
                                    'ai_status': 'fc_os_ai_1',
                                    'ai_frequency': 'fc_os_ai_2',
                                    'ai_alarm_code': 'fc_os_ai_3',
                                    'mb_cells_idx': 483
                                }
                            }
                        },
                        'valve_water_os': {
                            'class': Valve,
                            'do_open': None,
                            'mb_cells_idx': None
                        },
                        'valve_b1': {
                            'class': Valve,
                            'do_open': 'dio_1_o_1',
                            'mb_cells_idx': 44
                        },
                        'valve_b2': {
                            'class': Valve,
                            'do_open': 'dio_1_o_3',
                            'mb_cells_idx': 46
                        },
                        'valve_b3': {
                            'class': Valve,
                            'do_open': 'dio_1_o_2',
                            'mb_cells_idx': 42
                        },
                        'tank_b1': {
                            'class': Tank,
                            'di_low_level': 'di_1_2',
                            'di_mid_level': 'di_1_3',
                            'di_hi_level': 'di_1_4',
                            'mb_cells_idx': 48
                        },
                        'tank_b2': {
                            'class': Tank,
                            'di_low_level': 'di_1_10',
                            'di_mid_level': 'di_1_11',
                            'di_hi_level': 'di_1_12',
                            'mb_cells_idx': 50
                        },
                        'tank_b3': {
                            'class': Tank,
                            'di_low_level': 'di_1_6',
                            'di_mid_level': 'di_1_7',
                            'di_hi_level': 'di_1_8',
                            'mb_cells_idx': 558
                        }
                    }
                }
            }
        }
    }

    side_suppliers = {}
    for i in (1, 2):
        do_module = {1: 3, 2: 5}[i]
        side_suppliers[f'side_{i}'] = {
            'class': SideSupplier,
            'mb_cells_idx': None,
            'children': {
                'pump_foam': {
                    'class': PidEngine,
                    'ai_sensor': 'ai_2_4' if i == 1 else 'ai_3_5',
                    'set_point': 10.0,
                    'mb_cells_idx': 527 if i == 1 else 547,
                    'children': {
                        'fc': {
                            'class': Altivar212,
                            'ao_command': f'fc_foam_{i}_ao_1',
                            'ao_frequency': f'fc_foam_{i}_ao_2',
                            'ai_status': f'fc_os_foam_{i}_ai_1',
                            'ai_frequency': f'fc_foam_{i}_ai_2',
                            'ai_alarm_code': f'fc_foam_{i}_ai_3',
                            'mb_cells_idx': 518 if i == 1 else 538
                        }
                    }
                },
                'pump_intensive': {
                    'class': Engine,
                    'do_start': f'do_{do_module}_23',
                    'mb_cells_idx': 38 if i == 1 else None
                },
                'valve_dose_foam': {
                    'class': Valve,
                    'do_open': f'do_{do_module}_18',
                    'mb_cells_idx': 52 if i == 1 else None
                },
                'valve_dose_wax': {
                    'class': Valve,
                    'do_open': f'do_{do_module}_19',
                    'mb_cells_idx': 54 if i == 1 else None
                },
                'valve_dose_shampoo': {
                    'class': Valve,
                    'do_open': f'do_{do_module}_22',
                    'mb_cells_idx': 56 if i == 1 else None
                },
                'valve_dose_water_shampoo': {
                    'class': Valve,
                    'do_open': f'do_{do_module}_20',
                    'mb_cells_idx': 512 if i == 1 else None
                },
                'valve_dose_hot_water_shampoo': {
                    'class': Valve,
                    'do_open': f'do_{do_module}_21',
                    'mb_cells_idx': 514 if i == 1 else None
                },
                'valve_dose_intensive': {
                    'class': Valve,
                    'do_open': f'do_{do_module}_16',
                    'mb_cells_idx': 58 if i == 1 else None
                },
                'valve_dose_water_intensive': {
                    'class': Valve,
                    'do_open': f'do_{do_module}_15',
                    'mb_cells_idx': 516 if i == 1 else None
                },
                'valve_dose_osmos_intensive': {
                    'class': Valve,
                    'do_open': f'do_{do_module}_14',
                    'mb_cells_idx': 40 if i == 1 else None
                },
                'valve_dose_foam_2': {
                    'class': Valve,
                    'do_open': f'do_{do_module}_17',
                    'mb_cells_idx': 34 if i == 1 else None
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

    objects['top']['children']['supplier']['children'].update(side_suppliers)

    posts = dict([(f'post_{n}', copy.deepcopy(post)) for n in range(1, post_quantity + 1)])
    objects['top']['children'].update(posts)

    for name, obj in objects['top']['children'].items():
        if not name.startswith('post_'):
            continue
        post_number = int(name.lstrip('post_'))
        start_addr = 60 + (post_number - 1) * 32

        objects['top']['children']['supplier']['sides'][name] = 'side_1' if post_number <= 6 else 'side_2'

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
        elif post_number <= 6:
            obj['ai_pressure'] = f'ai_2_{post_number - 3}'
        else:
            obj['ai_pressure'] = f'ai_3_{post_number - 6}'

        if post_number <= 6:
            module_number = ((post_number - 1) // 3) + 1 if post_number <= 6 else ((post_number - 7) // 3) + 4
            obj['children']['valve_solution_2']['do_open'] = f'do_{module_number}_{(post_number - 1) % 3 * 8 + 1}'
            obj['children']['valve_wax']['do_open'] = f'do_{module_number}_{(post_number - 1) % 3 * 8 + 2}'
            obj['children']['valve_osmos']['do_open'] = f'do_{module_number}_{(post_number - 1) % 3 * 8 + 3}'
            obj['children']['valve_cold_water']['do_open'] = f'do_{module_number}_{(post_number - 1) % 3 * 8 + 4}'
            obj['children']['valve_hot_water']['do_open'] = f'do_{module_number}_{(post_number - 1) % 3 * 8 + 5}'
            obj['children']['valve_shampoo']['do_open'] = f'do_{module_number}_{(post_number - 1) % 3 * 8 + 6}'
            obj['children']['valve_out_water']['do_open'] = None
            obj['children']['valve_out_foam']['do_open'] = None
        else:
            module_number = 4
            obj['children']['valve_solution_2']['do_open'] = f'do_{module_number}_{(post_number - 7) % 4 * 6 + 1}'
            obj['children']['valve_wax']['do_open'] = f'do_{module_number}_{(post_number - 7) % 4 * 6 + 2}'
            obj['children']['valve_osmos']['do_open'] = f'do_{module_number}_{(post_number - 7) % 4 * 6 + 3}'
            obj['children']['valve_cold_water']['do_open'] = f'do_{module_number}_{(post_number - 7) % 4 * 6 + 4}'
            obj['children']['valve_hot_water']['do_open'] = f'do_{module_number}_{(post_number - 7) % 4 * 6 + 5}'
            obj['children']['valve_shampoo']['do_open'] = f'do_{module_number}_{(post_number - 7) % 4 * 6 + 6}'
            obj['children']['valve_out_water']['do_open'] = None
            obj['children']['valve_out_foam']['do_open'] = None

        if post_number <= 6:
            module2_number = 3
            obj['children']['valve_foam']['do_open'] = f'do_{module2_number}_{(post_number - 1) * 2 + 1}'
            obj['children']['valve_intensive']['do_open'] = f'do_{module2_number}_{(post_number - 1) * 2 + 2}'
        else:
            module2_number = 5
            obj['children']['valve_foam']['do_open'] = f'do_{module2_number}_{(post_number - 7) * 2 + 1}'
            obj['children']['valve_intensive']['do_open'] = f'do_{module2_number}_{(post_number - 7) * 2 + 2}'

        obj['children']['pump']['ao_command'] = f'fc_{post_number}_ao_1'
        obj['children']['pump']['ao_frequency'] = f'fc_{post_number}_ao_2'
        obj['children']['pump']['ai_status'] = f'fc_{post_number}_ai_1'
        obj['children']['pump']['ai_frequency'] = f'fc_{post_number}_ai_2'
        obj['children']['pump']['ai_alarm_code'] = None

    return objects
