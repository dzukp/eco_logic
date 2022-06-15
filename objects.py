import copy

from valve import Valve, NOValve
from engine import Engine
from fc import Altivar212
from tank import Tank
from post import Post
from waterpreparing import WaterPreparing
from subsystems import PidEngine
from top import Top
from hoover import Hoover
from bottom_wash import BottomWash
from brush_washer import BrushWasher


def get_object(post_quantity=(6, 6)):
    objects = {
        'top': {
            'class': Top,
            'mb_cells_idx': 808,
            'children': {}
        }
    }
    supplier = {
        'class': WaterPreparing,
        'di_press_1': None,
        'ai_pe_1': 'ai_1_2_1',
        'di_press_2': None,
        'ai_pe_2': 'ai_1_2_2',
        'di_press_3': None,
        'ai_pe_3': 'ai_1_2_3',
        'ai_pe_7': 'ai_2_2_1',
        'mb_cells_idx': 0,
        'children': {
            'pump_n1': {
                'class': Engine,
                'do_start': 'do_1_2_13',
                'mb_cells_idx': 50,
            },
            'pump_n2': {
                'class': Engine,
                'do_start': 'do_1_2_14',
                'mb_cells_idx': 52
            },
            'pump_n1_2': {
                'class': Engine,
                'do_start': 'do_1_2_18',
                'mb_cells_idx': 54
            },
            'pump_n3': {
                'class': Engine,
                'do_start': 'do_1_2_19',
                'mb_cells_idx': 56
            },
            'pump_os': {
                'class': PidEngine,
                'ai_sensor': 'ai_1_2_4',
                'mb_cells_idx': 58,
                'children': {
                    'fc': {
                        'class': Altivar212,
                        'ao_command': 'fc_os_ao_1',
                        'ao_frequency': 'fc_os_ao_2',
                        'ai_status': 'fc_os_ai_1',
                        'ai_frequency': 'fc_os_ai_2',
                        'ai_alarm_code': 'fc_os_ai_3',
                        'mb_cells_idx': 69
                    }
                }
            },
            'valve_water_os': {
                'class': Valve,
                'do_open': None,
                'mb_cells_idx': 68
            },
            'valve_wash_osmos': {
                'class': Valve,
                'do_open': None,
                'mb_cells_idx': 80
            },
            'valve_b1': {
                'class': Valve,
                'do_open': 'do_1_2_20',
                'mb_cells_idx': 82
            },
            'valve_b2': {
                'class': Valve,
                'do_open': 'do_1_2_21',
                'mb_cells_idx': 84
            },
            'valve_b1_1': {
                'class': Valve,
                'do_open': 'do_2_2_20',
                'mb_cells_idx': 86
            },
            'tank_b1': {
                'class': Tank,
                'di_low_level': 'di_1_3',
                'di_mid_level': 'di_1_2',
                'di_hi_level': 'di_1_1',
                'mb_cells_idx': 88
            },
            'tank_b2': {
                'class': Tank,
                'di_low_level': 'di_1_6',
                'di_mid_level': 'di_1_5',
                'di_hi_level': 'di_1_4',
                'mb_cells_idx': 90
            },
            'pump_n4': {
                'class': Engine,
                'do_start': 'do_1_2_15',
                'mb_cells_idx': 92
            },
            'pump_n5': {
                'class': Engine,
                'do_start': 'do_1_2_16',
                'mb_cells_idx': 94
            },
            'pump_n6': {
                'class': Engine,
                'do_start': 'do_1_2_17',
                'mb_cells_idx': 96
            },
            'pump_n7': {
                'class': Engine,
                'do_start': 'do_2_2_13',
                'mb_cells_idx': 98,
            },
            'pump_n7_1': {
                'class': Engine,
                'do_start': 'do_2_2_14',
                'mb_cells_idx': 100
            },
            'tank_b1_1': {
                'class': Tank,
                'di_low_level': 'di_2_3',
                'di_mid_level': 'di_2_2',
                'di_hi_level': 'di_2_1',
                'mb_cells_idx': 102
            },
            'pump_n8': {
                'class': Engine,
                'do_start': 'do_1_2_23',
                'mb_cells_idx': 104
            },
        }
    }
    hoover = {
        'class': Hoover,
        'ai_press_1': 'ai_3_1',
        'ai_press_2': 'ai_3_2',
        'mb_cells_idx': 106,
        'children': {
            'flap': {
                'class': Valve,
                'do_open': 'dio_3_o_1',
                'mb_cells_idx': 135
            },
            'fc_1': {
                'class': Altivar212,
                'ao_command': 'fc_hoover_1_ao_1',
                'ao_frequency': 'fc_hoover_1_ao_2',
                'ai_status': 'fc_hoover_1_ai_1',
                'ai_frequency': 'fc_hoover_1_ai_2',
                'ai_alarm_code': 'fc_hoover_1_ai_3',
                'mb_cells_idx': 137
            },
            'fc_2': {
                'class': Altivar212,
                'ao_command': 'fc_hoover_2_ao_1',
                'ao_frequency': 'fc_hoover_2_ao_2',
                'ai_status': 'fc_hoover_2_ai_1',
                'ai_frequency': 'fc_hoover_2_ai_2',
                'ai_alarm_code': 'fc_hoover_2_ai_3',
                'mb_cells_idx': 146
            }
        }
    }
    brush_washer = {
        'class': BrushWasher,
        'mb_cells_idx': None,
        'children': {
            'valve': {
                'class': Valve,
                'do_open': None,
            }
        }
    }
    post = {
        'class': Post,
        'ai_pressure': None,
        'children': {
            'valve_osmos': {
                'class': Valve,
                'do_open': None,
            },
            'valve_cold_water': {
                'class': Valve,
                'do_open': None,
            },
            'valve_solution': {
                'class': Valve,
                'do_open': None,
            },
            'valve_brush': {
                'class': Valve,
                'do_open': None,
            },
            'valve_wax': {
                'class': Valve,
                'do_open': None,
            },
            'valve_foam': {
                'class': Valve,
                'do_open': None,
            },
            'valve_wheel_black': {
                'class': Valve,
                'do_open': None
            },
            'valve_air': {
                'class': Valve,
                'do_open': None
            },
            'valve_polish': {
                'class': Valve,
                'do_open': None
            },
            'valve_glass': {
                'class': Valve,
                'do_open': None
            },
            'valve_hoover': {
                'class': Valve,
                'do_open': None
            },
            'valve_shell': {
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
    objects['top']['children']['hoover'] = hoover
    objects['top']['children']['brush_wash_1'] = copy.deepcopy(brush_washer)
    objects['top']['children']['brush_wash_2'] = copy.deepcopy(brush_washer)

    objects['top']['children']['brush_wash_1']['children']['valve']['do_open'] = 'do_1_2_22'
    objects['top']['children']['brush_wash_1']['mb_cells_idx'] = 171
    objects['top']['children']['brush_wash_1']['children']['valve']['mb_cells_idx'] = 175
    objects['top']['children']['brush_wash_2']['children']['valve']['do_open'] = 'do_2_2_22'
    objects['top']['children']['brush_wash_2']['mb_cells_idx'] = 177
    objects['top']['children']['brush_wash_2']['children']['valve']['mb_cells_idx'] = 181

    post_quantity = post_quantity if isinstance(post_quantity, (list, tuple)) else (post_quantity,)
    post_number = 0
    for side, post_q in enumerate(post_quantity, start=1):
        for i in range(1, post_q + 1):
            new_post = copy.deepcopy(post)
            post_number += 1
            post_name = f'post_{str(post_number)}'
            objects['top']['children'][post_name] = new_post
            
            start_addr = 200 + (post_number - 1) * 38
            new_post['mb_cells_idx'] = start_addr

            new_post['ai_pressure'] = f'ai_{side}_1_{(post_number - 1) % post_q + 1}'
            new_post['di_hoover'] = f'dio_p_{post_number}_i_1'
            new_post['di_brush'] = f'dio_p_{post_number}_i_2'
            new_post['di_car_inside'] = f'dio_p_{post_number}_i_3'
            new_post['do_green_light'] = f'dio_p_{post_number}_o_6'
            new_post['do_red_light'] = f'dio_p_{post_number}_o_7'

            children = new_post['children']
            children['valve_osmos']['mb_cells_idx'] = start_addr + 5
            children['valve_cold_water']['mb_cells_idx'] = start_addr + 7
            children['valve_solution']['mb_cells_idx'] = start_addr + 9
            children['valve_brush']['mb_cells_idx'] = start_addr + 11
            children['valve_wax']['mb_cells_idx'] = start_addr + 13
            children['valve_foam']['mb_cells_idx'] = start_addr + 15
            children['valve_wheel_black']['mb_cells_idx'] = start_addr + 17
            children['valve_air']['mb_cells_idx'] = start_addr + 19
            children['valve_polish']['mb_cells_idx'] = start_addr + 21
            children['valve_glass']['mb_cells_idx'] = start_addr + 23
            children['valve_hoover']['mb_cells_idx'] = start_addr + 25
            # children['valve_shell']['mb_cells_idx'] = start_addr + 27
            children['pump']['mb_cells_idx'] = start_addr + 29

            module = int((post_number - 1) / 2) % 3 + 1
            d = ((post_number - 1) % 2) * 6
            children['valve_osmos']['do_open'] = f'do_{side}_{module}_{1 + d}'
            children['valve_cold_water']['do_open'] = f'do_{side}_{module}_{2 + d}'
            children['valve_solution']['do_open'] = f'do_{side}_{module}_{3 + d}'
            children['valve_brush']['do_open'] = f'do_{side}_{module}_{4 + d}'
            children['valve_wax']['do_open'] = f'do_{side}_{module}_{5 + d}'
            children['valve_foam']['do_open'] = f'do_{side}_{module}_{6 + d}'
            children['valve_wheel_black']['do_open'] = f'dio_p_{post_number}_o_1'
            children['valve_air']['do_open'] = f'dio_p_{post_number}_o_2'
            children['valve_polish']['do_open'] = f'dio_p_{post_number}_o_3'
            children['valve_glass']['do_open'] = f'dio_p_{post_number}_o_4'
            children['valve_hoover']['do_open'] = f'dio_p_{post_number}_o_5'
            children['pump']['ao_command'] = f'fc_{side}_{(post_number - 1) % post_q + 1}_ao_1'
            children['pump']['ao_frequency'] = f'fc_{side}_{(post_number - 1) % post_q + 1}_ao_2'
            children['pump']['ai_status'] = f'fc_{side}_{(post_number - 1) % post_q + 1}_ai_1'
            children['pump']['ai_frequency'] = f'fc_{side}_{(post_number - 1) % post_q + 1}_ai_2'
            children['pump']['ai_alarm_code'] = f'fc_{side}_{(post_number - 1) % post_q + 1}_ai_3'

    return objects

