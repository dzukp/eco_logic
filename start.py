
import logging
import logging.handlers
import logging.config
from os import getcwd, makedirs
from pathlib import Path

from pylogic.main import main
from pylogic.logged_object import DEFAULT_LOGGER
from pylogic.modbus_supervisor import ModbusSupervisor
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
        'logging_conf': logging_config,
        'supervisors': {'supervis_modbus': ModbusSupervisor,}
    }
    main(config)


def loggers_init():
    log_dir = Path(getcwd()) / 'logs'
    if not log_dir.exists():
        makedirs(log_dir.absolute())
    logging.getLogger(DEFAULT_LOGGER).setLevel(logging.DEBUG)


if __name__ == '__main__':
    start()
