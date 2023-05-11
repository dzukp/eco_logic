logging_config = {
    'version': 1,
    'loggers': {
        'TagSrv': {
            'handlers': ['tagsrv_file', 'tagsrv_console'],
            'propagate': False,
            'level': 'DEBUG',
        },
        'TagSrv.serial_port_COM3': {
            'handlers': ['comport_file', 'tagsrv_console'],
            'propagate': False,
            'level': 'DEBUG',

        },
        'TagSrv.serial_port_COM4': {
            'handlers': ['comport_file', 'tagsrv_console'],
            'propagate': False,
            'level': 'DEBUG',

        },
        'TagSrv.serial_port_COM5': {
            'handlers': ['comport_file', 'tagsrv_console'],
            'propagate': False,
            'level': 'DEBUG',

        },
        'TagSrv.serial_port_fc_serial': {
            'handlers': ['comport_file'],
            'propagate': False,
            'level': 'DEBUG'
        },
        'TagSrv.serial_port_fc_serial1': {
            'handlers': ['comport_file'],
            'propagate': False,
            'level': 'DEBUG'
        },
        'TagSrv.serial_port_fc_serial2': {
            'handlers': ['comport_file'],
            'propagate': False,
            'level': 'DEBUG'
        },
        'PylogicLogger': {
            'handlers': ['common_console'],
            'propagate': False,
            'level': 'INFO',
        },
        'top': {
            'handlers': ['common_console', 'top_file'],
            'propagate': False,
            'level': 'DEBUG',
        },
        'TagSrv.OwenDoMu210_403_1921681100_502': {
            'handlers':['tmp_file', 'tagsrv_file', 'tagsrv_console'],
            'propagate': False,
            'level':'DEBUG',
        },
        'supervisors': {
            'handlers': ['common_console'],
            'propagate': False,
            'level': 'INFO',
        },
        'PylogicLogger.rpc_post_server': {
            'handlers': ['rpc_post_server_file'],
            'propagate': False,
            'level': 'INFO'
        },
        'PylogicLogger.rpc_post_state': {
            'handlers': ['rpc_post_state_file'],
            'propagate': False,
            'level': 'INFO'
        }
        # 'modbus_tk': {
        #     'handlers': ['common_console'],
        #     'propagate': False,
        #     'level': 'DEBUG',
        # }
    },
    'handlers': {
        'tagsrv_file': {
            'level': 'DEBUG',
            'formatter': 'verbose',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024*1024,
            'backupCount': 100,
            'filename': 'logs/tagsrv.log'
        },
        'tagsrv_console': {
            'level': 'CRITICAL',
            'formatter': 'verbose',
            'class': 'logging.StreamHandler'
        },
        'comport_file': {
            'level': 'DEBUG',
            'formatter': 'verbose',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024*1024,
            'backupCount': 100,
            'filename': 'logs/comport.log'
        },
        'common_console': {
            'level': 'DEBUG',
            'formatter': 'verbose',
            'class': 'logging.StreamHandler'
        },
        'top_file': {
            'level': 'DEBUG',
            'formatter': 'verbose',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024*1024,
            'backupCount': 10,
            'filename': 'logs/objects.log'
        },
        'rpc_post_server_file': {
            'level': 'DEBUG',
            'formatter': 'verbose',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024*1024,
            'backupCount': 100,
            'filename': 'logs/rpc.log'
        },
        'rpc_post_state_file': {
            'level': 'DEBUG',
            'formatter': 'verbose',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 200 * 1024 * 1024,
            'backupCount': 2,
            'filename': 'logs/rpc_state.log'
        },
        'tmp_file': {
            'level': 'DEBUG',
            'formatter': 'verbose',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024*1024,
            'backupCount': 10,
            'filename': 'logs/tmp.log'
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(asctime)s - %(name)s: %(message)s'
        },
        'simple': {
            'format': '%(message)s'
        }
    }
}
