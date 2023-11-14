#!/usr/bin/python3


import logging
import logging.handlers
import logging.config
from os import getcwd, makedirs
from pathlib import Path
import sys

from op_time_supervisor import OperatingTimeSupervisor
from pylogic.main import main
from pylogic.logged_object import DEFAULT_LOGGER
from pylogic.modbus_supervisor import ModbusSupervisor
from objects import get_object
from simulator_objects import get_simulator_objects
from tagsrv_settings import gen_tagsrv_config
from logconfig import logging_config
import settings


def start():
    post_quantity = settings.POST_QUANTITY
    simulator = settings.SIMULATOR
    sim_obj = get_simulator_objects(post_quantity) if simulator else {}
    log_dir = Path(getcwd()) / 'logs'
    if not log_dir.exists():
        makedirs(log_dir.absolute())
    config = {
        'objects': get_object(post_quantity),
        'simulators': sim_obj,
        'tagsrv_settings': gen_tagsrv_config(post_quantity),
        'logging_conf': logging_config,
        'supervisors': {'supervis_modbus': ModbusSupervisor, 'supervis_op_time': OperatingTimeSupervisor}
    }
    main(config)


def loggers_init():
    log_dir = Path(getcwd()) / 'logs'
    if not log_dir.exists():
        makedirs(log_dir.absolute())
    logging.getLogger(DEFAULT_LOGGER).setLevel(logging.DEBUG)


if __name__ == '__main__':
    start()
