#!/usr/bin/python3


import logging
import logging.handlers
import logging.config
from os import getcwd, makedirs
from pathlib import Path

from pylogic.main import main
from pylogic.logged_object import DEFAULT_LOGGER
from pylogic.modbus_supervisor import ModbusSupervisor
from objects import get_object, get_simulator_object
from tagsrv_settings import gen_tagsrv_config
from logconfig import logging_config
from rpc_supervisor import RpcSupervisor
import settings


def start():
    post_quantity = settings.POST_QUANTITY
    version = settings.VERSION
    simulator = settings.SIMULATOR

    sim_obj = get_simulator_object(version=version, post_quantity=post_quantity) if simulator else {}
    log_dir = Path(getcwd()) / 'logs'
    if not log_dir.exists():
        makedirs(log_dir.absolute())
    config = {
        'objects': get_object(version=version, post_quantity=post_quantity),
        'simulators': sim_obj,
        'tagsrv_settings': gen_tagsrv_config(version=version, post_quantity=post_quantity),
        'logging_conf': logging_config,
        'supervisors': {'supervis_modbus': ModbusSupervisor, 'supervis_rpc': RpcSupervisor}
    }
    main(config)


def loggers_init():
    log_dir = Path(getcwd()) / 'logs'
    if not log_dir.exists():
        makedirs(log_dir.absolute())
    logging.getLogger(DEFAULT_LOGGER).setLevel(logging.DEBUG)


if __name__ == '__main__':
    start()
