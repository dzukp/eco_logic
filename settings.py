import argparse
import os


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--post_quantity', nargs=2, type=int, default=[6, 6])
    parser.add_argument('-v', '--version', type=str, default='2.1')
    parser.add_argument('--simulator', action='store_true')

    if os.name == 'posix':
        parser.add_argument('--com1', default='fc_serial1', type=str)
        parser.add_argument('--com2', default='fc_serial2', type=str)
        parser.add_argument('--com3', default='fc_serial3', type=str)
    else:
        parser.add_argument('--com1', default='COM3', type=str)
        parser.add_argument('--com2', default='COM4', type=str)
        parser.add_argument('--com3', default='COM5', type=str)

    args = parser.parse_args()
    return args


arguments = parse_args()


POST_QUANTITY = arguments.post_quantity
VERSION = arguments.version
SIMULATOR = arguments.simulator
COM1 = arguments.com1
COM2 = arguments.com2
COM3 = arguments.com3
