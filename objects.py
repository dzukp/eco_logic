from pylogic.io_object import IoObject
from valve import Valve
from post import Post


objects = {
    'top': {
        'class': IoObject,
        'children': {
            'xxx': {
                'class': IoObject,
            },
            'post_1': {
                'class': Post,
                'ai_pressure': 'ai_1_1',
                'children': {
                    'v_foam': {
                        'class': Valve,
                        'do_open': 'do_1_1'
                    },
                    'v_wax': {
                        'class': Valve,
                        'do_open': 'do_1_2'
                    },
                    'v_shampoo': {
                        'class': Valve,
                        'do_open': 'do_1_3'
                    },
                    'v_cold_water': {
                        'class': Valve,
                        'do_open': 'do_1_4'
                    },
                    'v_hot_water': {
                        'class': Valve,
                        'do_open': 'do_1_5'
                    },
                    'v_osmos': {
                        'class': Valve,
                        'do_open': 'do_1_6'
                    },
                    'v_out_1': {
                        'class': Valve,
                        'do_open': 'do_1_7'
                    },
                    'v_out_2': {
                        'class': Valve,
                        'do_open': 'do_1_8'
                    },
                    'v_intensive': {
                        'class': Valve,
                        'do_open': 'do_2_9'
                    }
                }
            },
            'post_2': {
                'class': Post,
                'ai_pressure': 'ai_1_2',
                'children': {
                    'v_foam': {
                        'class': Valve,
                        'do_open': 'do_1_9'
                    },
                    'v_wax': {
                        'class': Valve,
                        'do_open': 'do_1_10'
                    },
                    'v_shampoo': {
                        'class': Valve,
                        'do_open': 'do_1_11'
                    },
                    'v_cold_water': {
                        'class': Valve,
                        'do_open': 'do_1_12'
                    },
                    'v_hot_water': {
                        'class': Valve,
                        'do_open': 'do_1_13'
                    },
                    'v_osmos': {
                        'class': Valve,
                        'do_open': 'do_1_14'
                    },
                    'v_out_1': {
                        'class': Valve,
                        'do_open': 'do_1_15'
                    },
                    'v_out_2': {
                        'class': Valve,
                        'do_open': 'do_1_16'
                    },
                    'v_intensive': {
                        'class': Valve,
                        'do_open': 'do_2_10'
                    }
                }
            },
            'post_3': {
                'class': Post,
                'ai_pressure': 'ai_1_3',
                'children': {
                    'v_foam': {
                        'class': Valve,
                        'do_open': 'do_1_17'
                    },
                    'v_wax': {
                        'class': Valve,
                        'do_open': 'do_1_18'
                    },
                    'v_shampoo': {
                        'class': Valve,
                        'do_open': 'do_1_19'
                    },
                    'v_cold_water': {
                        'class': Valve,
                        'do_open': 'do_1_20'
                    },
                    'v_hot_water': {
                        'class': Valve,
                        'do_open': 'do_1_211'
                    },
                    'v_osmos': {
                        'class': Valve,
                        'do_open': 'do_1_22'
                    },
                    'v_out_1': {
                        'class': Valve,
                        'do_open': 'do_1_23'
                    },
                    'v_out_2': {
                        'class': Valve,
                        'do_open': 'do_1_24'
                    },
                    'v_intensive': {
                        'class': Valve,
                        'do_open': 'do_2_11'
                    }
                }
            },
            'post_4': {
                'class': Post,
                'ai_pressure': 'ai_2_4',
                'children': {
                    'v_foam': {
                        'class': Valve,
                        'do_open': 'do_2_1'
                    },
                    'v_wax': {
                        'class': Valve,
                        'do_open': 'do_2_2'
                    },
                    'v_shampoo': {
                        'class': Valve,
                        'do_open': 'do_2_3'
                    },
                    'v_cold_water': {
                        'class': Valve,
                        'do_open': 'do_2_4'
                    },
                    'v_hot_water': {
                        'class': Valve,
                        'do_open': 'do_2_5'
                    },
                    'v_osmos': {
                        'class': Valve,
                        'do_open': 'do_2_6'
                    },
                    'v_out_1': {
                        'class': Valve,
                        'do_open': 'do_2_7'
                    },
                    'v_out_2': {
                        'class': Valve,
                        'do_open': 'do_2_8'
                    },
                    'v_intensive': {
                        'class': Valve,
                        'do_open': 'do_2_12'
                    }
                }
            },
            'post_5': {
                'class': Post,
                'ai_pressure': 'ai_3_5',
                'children': {
                    'v_foam': {
                        'class': Valve,
                        'do_open': 'do_3_1'
                    },
                    'v_wax': {
                        'class': Valve,
                        'do_open': 'do_3_2'
                    },
                    'v_shampoo': {
                        'class': Valve,
                        'do_open': 'do_3_3'
                    },
                    'v_cold_water': {
                        'class': Valve,
                        'do_open': 'do_3_4'
                    },
                    'v_hot_water': {
                        'class': Valve,
                        'do_open': 'do_3_5'
                    },
                    'v_osmos': {
                        'class': Valve,
                        'do_open': 'do_3_6'
                    },
                    'v_out_1': {
                        'class': Valve,
                        'do_open': 'do_3_7'
                    },
                    'v_out_2': {
                        'class': Valve,
                        'do_open': 'do_3_8'
                    },
                    'v_intensive': {
                        'class': Valve,
                        'do_open': 'do_4_9'
                    }
                }
            },
            'post_6': {
                'class': Post,
                'ai_pressure': 'ai_3_6',
                'children': {
                    'v_foam': {
                        'class': Valve,
                        'do_open': 'do_3_9'
                    },
                    'v_wax': {
                        'class': Valve,
                        'do_open': 'do_3_10'
                    },
                    'v_shampoo': {
                        'class': Valve,
                        'do_open': 'do_3_11'
                    },
                    'v_cold_water': {
                        'class': Valve,
                        'do_open': 'do_3_12'
                    },
                    'v_hot_water': {
                        'class': Valve,
                        'do_open': 'do_3_13'
                    },
                    'v_osmos': {
                        'class': Valve,
                        'do_open': 'do_3_14'
                    },
                    'v_out_1': {
                        'class': Valve,
                        'do_open': 'do_3_15'
                    },
                    'v_out_2': {
                        'class': Valve,
                        'do_open': 'do_3_16'
                    },
                    'v_intensive': {
                        'class': Valve,
                        'do_open': 'do_4_10'
                    }
                }
            },
            'post_7': {
                'class': Post,
                'ai_pressure': 'ai_3_7',
                'children': {
                    'v_foam': {
                        'class': Valve,
                        'do_open': 'do_3_17'
                    },
                    'v_wax': {
                        'class': Valve,
                        'do_open': 'do_3_18'
                    },
                    'v_shampoo': {
                        'class': Valve,
                        'do_open': 'do_3_19'
                    },
                    'v_cold_water': {
                        'class': Valve,
                        'do_open': 'do_3_20'
                    },
                    'v_hot_water': {
                        'class': Valve,
                        'do_open': 'do_3_211'
                    },
                    'v_osmos': {
                        'class': Valve,
                        'do_open': 'do_3_22'
                    },
                    'v_out_1': {
                        'class': Valve,
                        'do_open': 'do_3_23'
                    },
                    'v_out_2': {
                        'class': Valve,
                        'do_open': 'do_3_24'
                    },
                    'v_intensive': {
                        'class': Valve,
                        'do_open': 'do_4_11'
                    }
                }
            },
            'post_8': {
                'class': Post,
                'ai_pressure': 'ai_3_8',
                'children': {
                    'v_foam': {
                        'class': Valve,
                        'do_open': 'do_4_1'
                    },
                    'v_wax': {
                        'class': Valve,
                        'do_open': 'do_4_2'
                    },
                    'v_shampoo': {
                        'class': Valve,
                        'do_open': 'do_4_3'
                    },
                    'v_cold_water': {
                        'class': Valve,
                        'do_open': 'do_4_4'
                    },
                    'v_hot_water': {
                        'class': Valve,
                        'do_open': 'do_4_5'
                    },
                    'v_osmos': {
                        'class': Valve,
                        'do_open': 'do_4_6'
                    },
                    'v_out_1': {
                        'class': Valve,
                        'do_open': 'do_4_7'
                    },
                    'v_out_2': {
                        'class': Valve,
                        'do_open': 'do_4_8'
                    },
                    'v_intensive': {
                        'class': Valve,
                        'do_open': 'do_4_12'
                    }
                }
            }
        }
    }
}