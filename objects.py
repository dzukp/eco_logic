import copy

from valve import Valve, NOValve
from engine import Engine
from fc import Altivar212
from tank import Tank
from post import Post
from waterpreparing import WaterPreparing
from subsystems import PidEngine
from top import Top


def get_object(post_quantity=(6, 6)):
    objects = {
        'top': {
            'class': Top,
            'mb_cells_idx': 500,
            'children': {
            }
        }
    }
    supplier = {
        'class': WaterPreparing,
        'di_press_1': None,
        'ai_pe_1': 'ai_1_2_1',
        'di_press_2': None,
        'ai_pe_2': 'ai_1_2_2',
        'di_press_3': None,
        'ai_pe_3': 'ai_1_2_8',
        'mb_cells_idx': 0,
        'children': {
            'pump_n1': {
                'class': Engine,
                'do_start': 'do_1_2_13',
                'mb_cells_idx': 30,
            },
            'pump_n2': {
                'class': Engine,
                'do_start': 'do_1_2_14',
                'mb_cells_idx': 32
            },
            'pump_n1_2': {
                'class': Engine,
                'do_start': 'do_1_2_18',
                'mb_cells_idx': 493
            },
            'pump_n3': {
                'class': Engine,
                'do_start': 'do_1_2_19',
                'mb_cells_idx': 497
            },
            'pump_os': {
                'class': PidEngine,
                'ai_sensor': 'ai_1_2_4',
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
                'mb_cells_idx': 40
            },
            'valve_wash_osmos': {
                'class': Valve,
                'do_open': None,
                'mb_cells_idx': 42
            },
            'valve_b1': {
                'class': Valve,
                'do_open': 'do_1_2_20',
                'mb_cells_idx': 44
            },
            'valve_b2': {
                'class': Valve,
                'do_open': 'do_1_2_21',
                'mb_cells_idx': 46
            },
            'valve_b3': {
                'class': Valve,
                'do_open': None,
                'mb_cells_idx': 52
            },
            'tank_b1': {
                'class': Tank,
                'di_low_level': 'dio_1_1_3',
                'di_mid_level': 'dio_1_1_2',
                'di_hi_level': 'dio_1_1_1',
                'mb_cells_idx': 48
            },
            'tank_b2': {
                'class': Tank,
                'di_low_level': 'dio_1_1_6',
                'di_mid_level': 'dio_1_1_5',
                'di_hi_level': 'dio_1_1_4',
                'mb_cells_idx': 50
            },
            'tank_b3': {
                'class': Tank,
                'di_low_level': None,
                'di_mid_level': None,
                'di_hi_level': None,
                'mb_cells_idx': 54
            },
            # 'valve_dose_foam': {
            #     'class': Valve,
            #     'do_open': None,
            #     'mb_cells_idx': 52
            # },
            # 'valve_dose_wax': {
            #     'class': Valve,
            #     'do_open': None,
            #     'mb_cells_idx': 54
            # },
            # 'valve_dose_shampoo': {
            #     'class': Valve,
            #     'do_open': None,
            #     'mb_cells_idx': 56
            # },
            # 'valve_dose_intensive': {
            #     'class': Valve,
            #     'do_open': None,
            #     'mb_cells_idx': 58
            # }
        }
    }
    post = {
        'class': Post,
        'ai_pressure': None,
        'di_flow': None,
        'children': {
            'valve_osmos': {
                'class': Valve,
                'do_open': 'do_1_1_1',
            },
            'valve_cold_water': {
                'class': Valve,
                'do_open': 'do_1_1_2',
            },
            'valve_solution': {
                'class': Valve,
                'do_open': 'do_1_1_3',
            },
            'valve_brush': {
                'class': Valve,
                'do_open': 'do_1_1_4',
            },
            'valve_wax': {
                'class': Valve,
                'do_open': 'do_1_1_5',
            },
            'valve_foam': {
                'class': Valve,
                'do_open': 'do_1_1_6',
            },
            'valve_out_water': {
                'class': Valve,
                'do_open': None
            },
            'valve_out_foam': {
                'class': Valve,
                'do_open': None
            },
            'pump': {
                'class': Altivar212,
                'ao_command': 'fc_1_1_ao_1',
                'ao_frequency': 'fc_1_1_ao_2',
                'ai_status': 'fc_1_1_ai_1',
                'ai_frequency': 'fc_1_1_ai_2',
                'ai_alarm_code': 'fc_1_1_ai_3',
            }
        }
    }

    objects['top']['children']['supplier'] = supplier

    post_quantity = post_quantity if isinstance(post_quantity, (list, tuple)) else (post_quantity,)
    post_number = 0
    for side, post_q in enumerate(post_quantity, start=1):
        # new_supplier = copy.deepcopy(supplier)
        # objects['top']['children'][f'supplier_{str(side)}'] = new_supplier
        for i in range(1, post_q + 1):
            new_post = copy.deepcopy(post)
            post_number += 1
            post_name = f'post_{str(post_number)}'
            objects['top']['children'][post_name] = new_post
            
            start_addr = 60 + (post_number - 1) * 32
            new_post['mb_cells_idx'] = start_addr

            new_post['di_flow'] = f'di_{side}_1_{(post_number - 1) % post_q + 1}'
            new_post['ai_pressure'] = f'ai_{side}_1_{(post_number - 1) % post_q + 1}'

            children = new_post['children']
            children['valve_foam']['mb_cells_idx'] = start_addr + 5
            children['valve_wax']['mb_cells_idx'] = start_addr + 7
            children['valve_solution']['mb_cells_idx'] = start_addr + 9
            children['valve_cold_water']['mb_cells_idx'] = start_addr + 11
            children['valve_brush']['mb_cells_idx'] = start_addr + 13
            children['valve_osmos']['mb_cells_idx'] = start_addr + 15
            children['valve_out_water']['mb_cells_idx'] = start_addr + 17
            children['valve_out_foam']['mb_cells_idx'] = start_addr + 19
            children['pump']['mb_cells_idx'] = start_addr + 23

            module = int((post_number - 1) / 2) % 3 + 1
            d = ((post_number - 1) % 2) * 6
            children['valve_osmos']['do_open'] = f'do_{side}_{module}_{1 + d}'
            children['valve_cold_water']['do_open'] = f'do_{side}_{module}_{2 + d}'
            children['valve_solution']['do_open'] = f'do_{side}_{module}_{3 + d}'
            children['valve_brush']['do_open'] = f'do_{side}_{module}_{4 + d}'
            children['valve_wax']['do_open'] = f'do_{side}_{module}_{5 + d}'
            children['valve_foam']['do_open'] = f'do_{side}_{module}_{6 + d}'
            children['valve_out_water']['do_open'] = None
            children['valve_out_foam']['do_open'] = None
            children['pump']['ao_command'] = f'fc_{side}_{(post_number - 1) % post_q + 1}_ao_1'
            children['pump']['ao_frequency'] = f'fc_{side}_{(post_number - 1) % post_q + 1}_ao_2'
            children['pump']['ai_status'] = f'fc_{side}_{(post_number - 1) % post_q + 1}_ai_1'
            children['pump']['ai_frequency'] = f'fc_{side}_{(post_number - 1) % post_q + 1}_ai_2'
            children['pump']['ai_alarm_code'] = f'fc_{side}_{(post_number - 1) % post_q + 1}_ai_3'

    return objects

