logging_config = {
    'version': 1,
    'loggers': {
        'TagSrv': {
            'handlers':['tagsrv_file', 'tagsrv_console'],
            'propagate': False,
            'level':'DEBUG',
        },
        'PylogicLogger': {
            'handlers': ['common_console'],
            'propagate': False,
            'level': 'DEBUG',
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
    },
    'handlers': {
        'tagsrv_file': {
            'level': 'DEBUG',
            'formatter': 'verbose',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024*1024,
            'backupCount': 10,
            'filename': 'logs/tagsrv.log'
        },
        'tagsrv_console': {
            'level': 'WARNING',
            'formatter': 'verbose',
            'class': 'logging.StreamHandler'
        },
        'common_console': {
            'level': 'INFO',
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
            'format': '%(name)s - %(asctime)s: %(message)s'
        },
        'simple': {
            'format': '%(message)s'
        }
    }
}