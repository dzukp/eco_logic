
import logging
import logging.handlers
import logging.config
from os import getcwd, makedirs
from pathlib import Path

from pylogic.main import main
from pylogic.logged_object import DEFAULT_LOGGER
from objects import objects
from tagsrv_settings import settings as tagsrv_settings
from logconfig import logging_config


def start():
    log_dir = Path(getcwd()) / 'logs'
    if not log_dir.exists():
        makedirs(log_dir.absolute())
    config = {
        'objects': objects,
        'tagsrv_settings': tagsrv_settings,
        'logging_conf': logging_config
    }
    main(config)


def loggers_init():
    log_dir = Path(getcwd()) / 'logs'
    if not log_dir.exists():
        makedirs(log_dir.absolute())
    logging.getLogger(DEFAULT_LOGGER).setLevel(logging.DEBUG)
    # logging.config.fileConfig('logging.conf')
    # formatter = logging.Formatter('%(name)s - %(asctime)s: %(message)s')
    #
    # logging.getLogger('TagSrv').propagate = False
    #
    # # tagserver loggers
    # logging.getLogger('TagSrv').setLevel(logging.DEBUG)
    # tagsrv_file_handler = logging.handlers.RotatingFileHandler(
    #     log_dir / 'tagsrv.log', maxBytes=1024*1024, backupCount=10)
    # tagsrv_file_handler.setFormatter(formatter)
    # tagsrv_file_handler.setLevel(logging.DEBUG)
    # logging.getLogger('TagSrv').addHandler(tagsrv_file_handler)
    # tagsrv_stream_handler = logging.StreamHandler()
    # tagsrv_stream_handler.setFormatter(formatter)
    # tagsrv_stream_handler.setLevel(logging.WARNING)
    # logging.getLogger('TagSrv').addHandler(tagsrv_stream_handler)
    # logging.getLogger('TagSrv').info('Logger is created')


if __name__ == '__main__':
    start()
