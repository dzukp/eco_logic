import logging
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta

import requests as requests

from pylogic.io_object import IoObject
from pylogic.supervisor_manager import BaseSupervisor

from operating_time import OperatingTimer
import settings


class OperatingTimeSupervisor(BaseSupervisor):

    logger = logging.getLogger('operating_timer')

    def __init__(self, name):
        super().__init__(name)
        self.thread_pool_executor = ThreadPoolExecutor()
        self.op_timers = []
        self.excess_msg = {}
        self.next_send_regular_msg = datetime.now() + timedelta(seconds=10.0)
        self.regular_msg_period = timedelta(hours=24)

    def init(self):
        self.prepare_object(self.top_object)

    def prepare_object(self, obj):
        if isinstance(obj, OperatingTimer):
            self.op_timers.append(obj)
            self.excess_msg[obj] = False
        if isinstance(obj, IoObject):
            for child in obj.children:
                self.prepare_object(child)

    def send_data(self):
        for op_timer in self.op_timers:
            if op_timer.excess and not self.excess_msg[op_timer]:
                self.send_exceed_msg(op_timer)
                self.excess_msg[op_timer] = True
            elif not op_timer.excess and self.excess_msg[op_timer]:
                self.excess_msg[op_timer] = False
        if datetime.now() > self.next_send_regular_msg:
            self.next_send_regular_msg += self.regular_msg_period
            self.send_regular_msg()

    def send_regular_msg(self):
        msg = ['Наработка']
        for op_timer in self.op_timers:
            msg.append(f'{op_timer.parent_name}:\t {round(op_timer.get_operating_hours())}ч')
        msg = '\n'.join(msg)
        self.logger.info(f'Send message: {msg}')
        self.tg_send(msg)

    def send_exceed_msg(self, op_timer: OperatingTimer):
        msg = f'{op_timer.parent_name}:\t превышена наработка - {round(op_timer.get_operating_hours())}ч'
        self.logger.info(f'Send message: {msg}')
        self.tg_send(msg)

    def tg_send(self, msg):
        if settings.TG_CHAT_ID:
            def __send():
                try:
                    resp = requests.post(
                        f'https://api.telegram.org/bot{settings.TG_BOT_TOKEN}/sendMessage',
                        params={'chat_id': settings.TG_CHAT_ID, 'parse_mode': 'html'},
                        json={"text": msg}
                    )
                    if resp.ok:
                        self.logger.debug('send msg OK', resp.elapsed)
                        print('resp time: ', resp.elapsed)
                except requests.exceptions.Timeout:
                    self.logger.exception('Timeout')
                except requests.exceptions.TooManyRedirects:
                    self.logger.exception('TooManyRedirects')
                except:
                    self.logger.exception('Another exception')

            self.thread_pool_executor.submit(__send)
