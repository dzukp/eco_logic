import argparse
import os


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('post_quantity', type=int)
    parser.add_argument('-v', '--version', type=str, default='1.1')
    parser.add_argument('--simulator', action='store_true')

    parser.add_argument('--com1', default=None, type=str)
    parser.add_argument('--com2', default=None, type=str)
    parser.add_argument('--com3', default=None, type=str)

    args = parser.parse_args()
    return args


arguments = parse_args()


POST_QUANTITY = arguments.post_quantity
VERSION = arguments.version
SIMULATOR = arguments.simulator
COM1 = arguments.com1
COM2 = arguments.com2
COM3 = arguments.com3
