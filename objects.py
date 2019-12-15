from pylogic.io_object import IoObject
from valve import Valve, NOValve
from engine import Engine
from fc import Altivar212
from tank import Tank
from post import Post
from waterpreparing import WaterPreparing
from nofrost import Nofrost
from top import Top


objects = {
    'top': {
        'class': Top,
        'children': {
            'supplier': {
                'class': WaterPreparing,
                'di_press_1': '',
                'ai_pe_1': '',
                'di_press_2': '',
                'ai_pe_2': '',
                'di_press_3': '',
                'mb_cells_idx': 86,
                'children': {
                    'pump_n1': {
                        'class': Engine,
                        'do_start': '',
                        'mb_cells_idx': 0,
                    },
                    'pump_n2': {
                        'class': Engine,
                        'do_start': '',
                        'mb_cells_idx': 3
                    },
                    'pump_os1': {
                        'class': Engine,
                        'do_start': '',
                        'mb_cells_idx': 6
                    },
                    'pump_os2': {
                        'class': Engine,
                        'do_start': '',
                        'mb_cells_idx': 9
                    },
                    'pump_i1': {
                        'class': Engine,
                        'do_start': '',
                        'mb_cells_idx': 12
                    },
                    'valve_b1': {
                        'class': Valve,
                        'do_open': '',
                        'mb_cells_idx': 15
                    },
                    'valve_b2': {
                        'class': Valve,
                        'do_open': '',
                        'mb_cells_idx': 18
                    },
                    'valve_water_os': {
                        'class': Valve,
                        'do_open': '',
                        'mb_cells_idx': 21
                    },
                    'tank_b1': {
                        'class': Tank,
                        'di_low_level': '',
                        'di_mid_level': '',
                        'di_hi_level': '',
                        'mb_cells_idx': 24
                    },
                    'tank_b2': {
                        'class': Tank,
                        'di_low_level': '',
                        'di_mid_level': '',
                        'di_hi_level': '',
                        'mb_cells_idx': 26
                    },
                    'valve_dose_wax': {
                        'class': Valve,
                        'do_open': '',
                        'mb_cells_idx': 87
                    },
                    'valve_dose_shampoo': {
                        'class': Valve,
                        'do_open': '',
                        'mb_cells_idx': 90
                    },
                    'valve_dose_foam': {
                        'class': Valve,
                        'do_open': '',
                        'mb_cells_idx': 93
                    },
                    'valve_dose_intensive': {
                        'class': Valve,
                        'do_open': '',
                        'mb_cells_idx': 96
                    }
                }
            },
            'nofrost': {
                'class': Nofrost,
                'ai_temp_1': '',
                'ai_temp_2': '',
                'mb_cells_idx': 28,
                'children': {
                    'valve_nc': {
                        'class': Valve,
                        'do_open': '',
                        'mb_cells_idx': 32
                    },
                    'valve_no': {
                        'class': NOValve,
                        'do_close': '',
                        'mb_cells_idx': 35
                    },
                }
            },
            'post_1': {
                'class': Post,
                'ai_pressure': 'ai_1_1',
                'mb_cells_idx': 76,
                'children': {
                    'valve_foam': {
                        'class': Valve,
                        'do_open': 'do_1_1',
                        'mb_cells_idx': 39
                    },
                    'valve_wax': {
                        'class': Valve,
                        'do_open': 'do_1_2',
                        'mb_cells_idx': 42
                    },
                    'valve_shampoo': {
                        'class': Valve,
                        'do_open': 'do_1_3',
                        'mb_cells_idx': 45
                    },
                    'valve_cold_water': {
                        'class': Valve,
                        'do_open': 'do_1_4',
                        'mb_cells_idx': 48
                    },
                    'valve_hot_water': {
                        'class': Valve,
                        'do_open': 'do_1_5',
                        'mb_cells_idx': 51
                    },
                    'valve_osmos': {
                        'class': Valve,
                        'do_open': 'do_1_6',
                        'mb_cells_idx': 54
                    },
                    'valve_out_1': {
                        'class': Valve,
                        'do_open': 'do_1_7',
                        'mb_cells_idx': 57
                    },
                    'valve_out_2': {
                        'class': Valve,
                        'do_open': 'do_1_8',
                        'mb_cells_idx': 60
                    },
                    'valve_intensive': {
                        'class': Valve,
                        'do_open': 'do_2_9',
                        'mb_cells_idx': 63
                    },
                    'pump': {
                        'class': Altivar212,
                        'ao_command': '',
                        'ao_frequency': '',
                        'ai_status': '',
                        'ai_frequency': '',
                        'ai_alarm_code': '',
                        'mb_cells_idx': 66
                    }
                }
            },
            'post_2': {
                'class': Post,
                'ai_pressure': 'ai_1_2',
                'children': {
                    'valve_foam': {
                        'class': Valve,
                        'do_open': 'do_1_9'
                    },
                    'valve_wax': {
                        'class': Valve,
                        'do_open': 'do_1_10'
                    },
                    'valve_shampoo': {
                        'class': Valve,
                        'do_open': 'do_1_11'
                    },
                    'valve_cold_water': {
                        'class': Valve,
                        'do_open': 'do_1_12'
                    },
                    'valve_hot_water': {
                        'class': Valve,
                        'do_open': 'do_1_13'
                    },
                    'valve_osmos': {
                        'class': Valve,
                        'do_open': 'do_1_14'
                    },
                    'valve_out_1': {
                        'class': Valve,
                        'do_open': 'do_1_15'
                    },
                    'valve_out_2': {
                        'class': Valve,
                        'do_open': 'do_1_16'
                    },
                    'valve_intensive': {
                        'class': Valve,
                        'do_open': 'do_2_10'
                    }
                }
            },
            'post_3': {
                'class': Post,
                'ai_pressure': 'ai_1_3',
                'children': {
                    'valve_foam': {
                        'class': Valve,
                        'do_open': 'do_1_17'
                    },
                    'valve_wax': {
                        'class': Valve,
                        'do_open': 'do_1_18'
                    },
                    'valve_shampoo': {
                        'class': Valve,
                        'do_open': 'do_1_19'
                    },
                    'valve_cold_water': {
                        'class': Valve,
                        'do_open': 'do_1_20'
                    },
                    'valve_hot_water': {
                        'class': Valve,
                        'do_open': 'do_1_21'
                    },
                    'valve_osmos': {
                        'class': Valve,
                        'do_open': 'do_1_22'
                    },
                    'valve_out_1': {
                        'class': Valve,
                        'do_open': 'do_1_23'
                    },
                    'valve_out_2': {
                        'class': Valve,
                        'do_open': 'do_1_24'
                    },
                    'valve_intensive': {
                        'class': Valve,
                        'do_open': 'do_2_11'
                    }
                }
            },
            'post_4': {
                'class': Post,
                'ai_pressure': 'ai_2_4',
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
                    'valve_out_1': {
                        'class': Valve,
                        'do_open': 'do_2_7'
                    },
                    'valve_out_2': {
                        'class': Valve,
                        'do_open': 'do_2_8'
                    },
                    'valve_intensive': {
                        'class': Valve,
                        'do_open': 'do_2_12'
                    }
                }
            },
            'post_5': {
                'class': Post,
                'ai_pressure': 'ai_3_5',
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
                    'valve_out_1': {
                        'class': Valve,
                        'do_open': 'do_3_7'
                    },
                    'valve_out_2': {
                        'class': Valve,
                        'do_open': 'do_3_8'
                    },
                    'valve_intensive': {
                        'class': Valve,
                        'do_open': 'do_4_9'
                    }
                }
            },
            'post_6': {
                'class': Post,
                'ai_pressure': 'ai_3_6',
                'children': {
                    'valve_foam': {
                        'class': Valve,
                        'do_open': 'do_3_9'
                    },
                    'valve_wax': {
                        'class': Valve,
                        'do_open': 'do_3_10'
                    },
                    'valve_shampoo': {
                        'class': Valve,
                        'do_open': 'do_3_11'
                    },
                    'valve_cold_water': {
                        'class': Valve,
                        'do_open': 'do_3_12'
                    },
                    'valve_hot_water': {
                        'class': Valve,
                        'do_open': 'do_3_13'
                    },
                    'valve_osmos': {
                        'class': Valve,
                        'do_open': 'do_3_14'
                    },
                    'valve_out_1': {
                        'class': Valve,
                        'do_open': 'do_3_15'
                    },
                    'valve_out_2': {
                        'class': Valve,
                        'do_open': 'do_3_16'
                    },
                    'valve_intensive': {
                        'class': Valve,
                        'do_open': 'do_4_10'
                    }
                }
            },
            'post_7': {
                'class': Post,
                'ai_pressure': 'ai_3_7',
                'children': {
                    'valve_foam': {
                        'class': Valve,
                        'do_open': 'do_3_17'
                    },
                    'valve_wax': {
                        'class': Valve,
                        'do_open': 'do_3_18'
                    },
                    'valve_shampoo': {
                        'class': Valve,
                        'do_open': 'do_3_19'
                    },
                    'valve_cold_water': {
                        'class': Valve,
                        'do_open': 'do_3_20'
                    },
                    'valve_hot_water': {
                        'class': Valve,
                        'do_open': 'do_3_21'
                    },
                    'valve_osmos': {
                        'class': Valve,
                        'do_open': 'do_3_22'
                    },
                    'valve_out_1': {
                        'class': Valve,
                        'do_open': 'do_3_23'
                    },
                    'valve_out_2': {
                        'class': Valve,
                        'do_open': 'do_3_24'
                    },
                    'valve_intensive': {
                        'class': Valve,
                        'do_open': 'do_4_11'
                    }
                }
            },
            'post_8': {
                'class': Post,
                'ai_pressure': 'ai_3_8',
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
                    'valve_out_1': {
                        'class': Valve,
                        'do_open': 'do_4_7'
                    },
                    'valve_out_2': {
                        'class': Valve,
                        'do_open': 'do_4_8'
                    },
                    'valve_intensive': {
                        'class': Valve,
                        'do_open': 'do_4_12'
                    }
                }
            }
        }
    }
}