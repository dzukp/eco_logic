from pylogic.io_object import IoObject
from valve import Valve, NOValve
from engine import Engine
from fc import Altivar212
from tank import Tank
from post import Post
from waterpreparing import WaterPreparing
from nofrost import Nofrost
from top import Top


def get_object(post_quantity=8):
    objects = {
        'top': {
            'class': Top,
            'mb_cells_idx': 500,
            'children': {
                'supplier': {
                    'class': WaterPreparing,
                    'di_press_1': None,
                    'ai_pe_1': None,
                    'di_press_2': None,
                    'ai_pe_2': 'ai_2_8',
                    'di_press_3': None,
                    'ai_pe_3': None,
                    'mb_cells_idx': 0,
                    'children': {
                        'pump_n1': {
                            'class': Engine,
                            'do_start': 'do_1_19',
                            'mb_cells_idx': 30,
                        },
                        'pump_n2': {
                            'class': Engine,
                            'do_start': 'do_1_20',
                            'mb_cells_idx': 32
                        },
                        'pump_os1': {
                            'class': Engine,
                            'do_start': 'do_1_21',
                            'mb_cells_idx': 34
                        },
                        'pump_os2': {
                            'class': Engine,
                            'do_start': None,
                            'mb_cells_idx': 36
                        },
                        'pump_i1': {
                            'class': Engine,
                            'do_start': 'do_1_22',
                            'mb_cells_idx': 38
                        },
                        'valve_water_os': {
                            'class': Valve,
                            'do_open': 'do_1_23',
                            'mb_cells_idx': 40
                        },
                        'valve_b1': {
                            'class': Valve,
                            'do_open': 'do_2_19',
                            'mb_cells_idx': 44
                        },
                        'valve_b2': {
                            'class': Valve,
                            'do_open': None,
                            'mb_cells_idx': 46
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
                'post_1': {
                    'class': Post,
                    'ai_pressure': 'ai_1_1',
                    'di_flow': None,
                    'children': {
                        'valve_foam': {
                            'class': Valve,
                            'do_open': 'do_1_1'
                        },
                        'valve_wax': {
                            'class': Valve,
                            'do_open': 'do_1_2'
                        },
                        'valve_shampoo': {
                            'class': Valve,
                            'do_open': 'do_1_3'
                        },
                        'valve_cold_water': {
                            'class': Valve,
                            'do_open': 'do_1_4'
                        },
                        'valve_hot_water': {
                            'class': Valve,
                            'do_open': 'do_1_5'
                        },
                        'valve_osmos': {
                            'class': Valve,
                            'do_open': 'do_1_6'
                        },
                        'valve_out_water': {
                            'class': Valve,
                            'do_open': 'do_1_7'
                        },
                        'valve_out_foam': {
                            'class': Valve,
                            'do_open': 'do_1_8'
                        },
                        'valve_intensive': {
                            'class': Valve,
                            'do_open': 'do_1_9'
                        },
                        'pump': {
                            'class': Altivar212,
                            'ao_command': 'fc1_ao_1',
                            'ao_frequency': 'fc1_ao_2',
                            'ai_status': 'fc1_ai_1',
                            'ai_frequency': 'fc1_ai_2',
                            'ai_alarm_code': 'fc1_ai_3',
                            'mb_cells_idx': None
                        }
                    }
                },
                'post_2': {
                    'class': Post,
                    'ai_pressure': 'ai_1_2',
                    'di_flow': None,
                    'children': {
                        'valve_foam': {
                            'class': Valve,
                            'do_open': 'do_1_10'
                        },
                        'valve_wax': {
                            'class': Valve,
                            'do_open': 'do_1_11'
                        },
                        'valve_shampoo': {
                            'class': Valve,
                            'do_open': 'do_1_12'
                        },
                        'valve_cold_water': {
                            'class': Valve,
                            'do_open': 'do_1_13'
                        },
                        'valve_hot_water': {
                            'class': Valve,
                            'do_open': 'do_1_14'
                        },
                        'valve_osmos': {
                            'class': Valve,
                            'do_open': 'do_1_15'
                        },
                        'valve_out_water': {
                            'class': Valve,
                            'do_open': 'do_1_16'
                        },
                        'valve_out_foam': {
                            'class': Valve,
                            'do_open': 'do_1_17'
                        },
                        'valve_intensive': {
                            'class': Valve,
                            'do_open': 'do_1_18'
                        },
                        'pump': {
                            'class': Altivar212,
                            'ao_command': 'fc2_ao_1',
                            'ao_frequency': 'fc2_ao_2',
                            'ai_status': 'fc2_ai_1',
                            'ai_frequency': 'fc2_ai_2',
                            'ai_alarm_code': 'fc2_ai_3',
                            'mb_cells_idx': None
                        }
                    }
                },
                'post_3': {
                    'class': Post,
                    'ai_pressure': 'ai_1_3',
                    'di_flow': None,
                    'children': {
                        'valve_foam': {
                            'class': Valve,
                            'do_open': 'do_2_1'
                        },
                        'valve_wax': {
                            'class': Valve,
                            'do_open': 'do_2_2'
                        },
                        'valve_shampoo': {
                            'class': Valve,
                            'do_open': 'do_2_3'
                        },
                        'valve_cold_water': {
                            'class': Valve,
                            'do_open': 'do_2_4'
                        },
                        'valve_hot_water': {
                            'class': Valve,
                            'do_open': 'do_2_5'
                        },
                        'valve_osmos': {
                            'class': Valve,
                            'do_open': 'do_2_6'
                        },
                        'valve_out_water': {
                            'class': Valve,
                            'do_open': 'do_2_7'
                        },
                        'valve_out_foam': {
                            'class': Valve,
                            'do_open': 'do_2_8'
                        },
                        'valve_intensive': {
                            'class': Valve,
                            'do_open': 'do_2_9'
                        },
                        'pump': {
                            'class': Altivar212,
                            'ao_command': 'fc3_ao_1',
                            'ao_frequency': 'fc3_ao_2',
                            'ai_status': 'fc3_ai_1',
                            'ai_frequency': 'fc3_ai_2',
                            'ai_alarm_code': 'fc3_ai_3',
                            'mb_cells_idx': None
                        }
                    }
                },
                'post_4': {
                    'class': Post,
                    'ai_pressure': 'ai_1_4',
                    'di_flow': None,
                    'children': {
                        'valve_foam': {
                            'class': Valve,
                            'do_open': 'do_2_10'
                        },
                        'valve_wax': {
                            'class': Valve,
                            'do_open': 'do_2_11'
                        },
                        'valve_shampoo': {
                            'class': Valve,
                            'do_open': 'do_2_12'
                        },
                        'valve_cold_water': {
                            'class': Valve,
                            'do_open': 'do_2_13'
                        },
                        'valve_hot_water': {
                            'class': Valve,
                            'do_open': 'do_2_14'
                        },
                        'valve_osmos': {
                            'class': Valve,
                            'do_open': 'do_2_15'
                        },
                        'valve_out_water': {
                            'class': Valve,
                            'do_open': 'do_2_16'
                        },
                        'valve_out_foam': {
                            'class': Valve,
                            'do_open': 'do_2_17'
                        },
                        'valve_intensive': {
                            'class': Valve,
                            'do_open': 'do_2_18'
                        },
                        'pump': {
                            'class': Altivar212,
                            'ao_command': 'fc4_ao_1',
                            'ao_frequency': 'fc4_ao_2',
                            'ai_status': 'fc4_ai_1',
                            'ai_frequency': 'fc4_ai_2',
                            'ai_alarm_code': 'fc4_ai_3',
                            'mb_cells_idx': None
                        }
                    }
                },
                'post_5': {
                    'class': Post,
                    'ai_pressure': 'ai_1_5',
                    'di_flow': None,
                    'children': {
                        'valve_foam': {
                            'class': Valve,
                            'do_open': 'do_3_1'
                        },
                        'valve_wax': {
                            'class': Valve,
                            'do_open': 'do_3_2'
                        },
                        'valve_shampoo': {
                            'class': Valve,
                            'do_open': 'do_3_3'
                        },
                        'valve_cold_water': {
                            'class': Valve,
                            'do_open': 'do_3_4'
                        },
                        'valve_hot_water': {
                            'class': Valve,
                            'do_open': 'do_3_5'
                        },
                        'valve_osmos': {
                            'class': Valve,
                            'do_open': 'do_3_6'
                        },
                        'valve_out_water': {
                            'class': Valve,
                            'do_open': 'do_3_7'
                        },
                        'valve_out_foam': {
                            'class': Valve,
                            'do_open': 'do_3_8'
                        },
                        'valve_intensive': {
                            'class': Valve,
                            'do_open': 'do_3_9'
                        },
                        'pump': {
                            'class': Altivar212,
                            'ao_command': 'fc5_ao_1',
                            'ao_frequency': 'fc5_ao_2',
                            'ai_status': 'fc5_ai_1',
                            'ai_frequency': 'fc5_ai_2',
                            'ai_alarm_code': 'fc5_ai_3',
                            'mb_cells_idx': None
                        }
                    }
                },
                'post_6': {
                    'class': Post,
                    'ai_pressure': 'ai_1_6',
                    'di_flow': None,
                    'children': {
                        'valve_foam': {
                            'class': Valve,
                            'do_open': 'do_3_10'
                        },
                        'valve_wax': {
                            'class': Valve,
                            'do_open': 'do_3_11'
                        },
                        'valve_shampoo': {
                            'class': Valve,
                            'do_open': 'do_3_12'
                        },
                        'valve_cold_water': {
                            'class': Valve,
                            'do_open': 'do_3_13'
                        },
                        'valve_hot_water': {
                            'class': Valve,
                            'do_open': 'do_3_14'
                        },
                        'valve_osmos': {
                            'class': Valve,
                            'do_open': 'do_3_15'
                        },
                        'valve_out_water': {
                            'class': Valve,
                            'do_open': 'do_3_16'
                        },
                        'valve_out_foam': {
                            'class': Valve,
                            'do_open': 'do_3_17'
                        },
                        'valve_intensive': {
                            'class': Valve,
                            'do_open': 'do_3_18'
                        },
                        'pump': {
                            'class': Altivar212,
                            'ao_command': 'fc6_ao_1',
                            'ao_frequency': 'fc6_ao_2',
                            'ai_status': 'fc6_ai_1',
                            'ai_frequency': 'fc6_ai_2',
                            'ai_alarm_code': 'fc6_ai_3',
                            'mb_cells_idx': None
                        }
                    }
                }
            }
        }
    }

    if post_quantity > 6:
        objects['top']['children'].update(
            {
                'post_7': {
                    'class': Post,
                    'ai_pressure': 'ai_1_7',
                    'di_flow': None,
                    'children': {
                        'valve_foam': {
                            'class': Valve,
                            'do_open': 'do_4_1'
                        },
                        'valve_wax': {
                            'class': Valve,
                            'do_open': 'do_4_2'
                        },
                        'valve_shampoo': {
                            'class': Valve,
                            'do_open': 'do_4_3'
                        },
                        'valve_cold_water': {
                            'class': Valve,
                            'do_open': 'do_4_4'
                        },
                        'valve_hot_water': {
                            'class': Valve,
                            'do_open': 'do_4_5'
                        },
                        'valve_osmos': {
                            'class': Valve,
                            'do_open': 'do_4_6'
                        },
                        'valve_out_water': {
                            'class': Valve,
                            'do_open': 'do_4_7'
                        },
                        'valve_out_foam': {
                            'class': Valve,
                            'do_open': 'do_4_8'
                        },
                        'valve_intensive': {
                            'class': Valve,
                            'do_open': 'do_4_9'
                        },
                        'pump': {
                            'class': Altivar212,
                            'ao_command': 'fc7_ao_1',
                            'ao_frequency': 'fc7_ao_2',
                            'ai_status': 'fc7_ai_1',
                            'ai_frequency': 'fc7_ai_2',
                            'ai_alarm_code': 'fc7_ai_3',
                            'mb_cells_idx': None
                        }
                    }
                }
            }
        )
        objects['top']['children']['supplier']['ai_pe_1'] = 'ai_1_8'

    if post_quantity > 7:
        objects['top']['children'].update({
            'post_8': {
                'class': Post,
                'ai_pressure': 'ai_1_8',
                'di_flow': None,
                'children': {
                    'valve_foam': {
                        'class': Valve,
                        'do_open': 'do_4_10'
                    },
                    'valve_wax': {
                        'class': Valve,
                        'do_open': 'do_4_11'
                    },
                    'valve_shampoo': {
                        'class': Valve,
                        'do_open': 'do_4_12'
                    },
                    'valve_cold_water': {
                        'class': Valve,
                        'do_open': 'do_4_13'
                    },
                    'valve_hot_water': {
                        'class': Valve,
                        'do_open': 'do_4_14'
                    },
                    'valve_osmos': {
                        'class': Valve,
                        'do_open': 'do_4_15'
                    },
                    'valve_out_water': {
                        'class': Valve,
                        'do_open': 'do_4_16'
                    },
                    'valve_out_foam': {
                        'class': Valve,
                        'do_open': 'do_4_17'
                    },
                    'valve_intensive': {
                        'class': Valve,
                        'do_open': 'do_4_18'
                    },
                    'pump': {
                        'class': Altivar212,
                        'ao_command': 'fc8_ao_1',
                        'ao_frequency': 'fc8_ao_2',
                        'ai_status': 'fc8_ai_1',
                        'ai_frequency': 'fc8_ai_2',
                        'ai_alarm_code': 'fc8_ai_3',
                        'mb_cells_idx': None
                    }
                }
            }
        })
        objects['top']['children']['supplier']['ai_pe_1'] = 'ai_2_1'

    if post_quantity > 8:
        objects['top']['children'].update(
            {
                'post_9': {
                    'class': Post,
                    'ai_pressure': 'ai_2_1',
                    'di_flow': None,
                    'children': {
                        'valve_foam': {
                            'class': Valve,
                            'do_open': 'do_5_1'
                        },
                        'valve_wax': {
                            'class': Valve,
                            'do_open': 'do_5_2'
                        },
                        'valve_shampoo': {
                            'class': Valve,
                            'do_open': 'do_5_3'
                        },
                        'valve_cold_water': {
                            'class': Valve,
                            'do_open': 'do_5_4'
                        },
                        'valve_hot_water': {
                            'class': Valve,
                            'do_open': 'do_5_5'
                        },
                        'valve_osmos': {
                            'class': Valve,
                            'do_open': 'do_5_6'
                        },
                        'valve_out_water': {
                            'class': Valve,
                            'do_open': 'do_5_7'
                        },
                        'valve_out_foam': {
                            'class': Valve,
                            'do_open': 'do_5_8'
                        },
                        'valve_intensive': {
                            'class': Valve,
                            'do_open': 'do_5_9'
                        },
                        'pump': {
                            'class': Altivar212,
                            'ao_command': 'fc9_ao_1',
                            'ao_frequency': 'fc9_ao_2',
                            'ai_status': 'fc9_ai_1',
                            'ai_frequency': 'fc9_ai_2',
                            'ai_alarm_code': 'fc9_ai_3',
                            'mb_cells_idx': None
                        }
                    }
                }
            }
        )
        objects['top']['children']['supplier']['ai_pe_1'] = 'ai_2_2'

    if post_quantity > 9:
        objects['top']['children'].update({
            'post_10': {
                'class': Post,
                'ai_pressure': 'ai_2_2',
                'di_flow': None,
                'children': {
                    'valve_foam': {
                        'class': Valve,
                        'do_open': 'do_5_10'
                    },
                    'valve_wax': {
                        'class': Valve,
                        'do_open': 'do_5_11'
                    },
                    'valve_shampoo': {
                        'class': Valve,
                        'do_open': 'do_5_12'
                    },
                    'valve_cold_water': {
                        'class': Valve,
                        'do_open': 'do_5_13'
                    },
                    'valve_hot_water': {
                        'class': Valve,
                        'do_open': 'do_5_14'
                    },
                    'valve_osmos': {
                        'class': Valve,
                        'do_open': 'do_5_15'
                    },
                    'valve_out_water': {
                        'class': Valve,
                        'do_open': 'do_5_16'
                    },
                    'valve_out_foam': {
                        'class': Valve,
                        'do_open': 'do_5_17'
                    },
                    'valve_intensive': {
                        'class': Valve,
                        'do_open': 'do_5_18'
                    },
                    'pump': {
                        'class': Altivar212,
                        'ao_command': 'fc10_ao_1',
                        'ao_frequency': 'fc10_ao_2',
                        'ai_status': 'fc10_ai_1',
                        'ai_frequency': 'fc10_ai_2',
                        'ai_alarm_code': 'fc10_ai_3',
                        'mb_cells_idx': None
                    }
                }
            }
        })
        objects['top']['children']['supplier']['ai_pe_1'] = 'ai_2_3'

    for name, obj in objects['top']['children'].items():
        if not name.startswith('post_'):
            continue
        start_addr = 60 + (int(name.lstrip('post_')) - 1) * 32
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

    return objects
