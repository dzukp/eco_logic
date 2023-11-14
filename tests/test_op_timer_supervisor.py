import datetime

from fake_periodic_clock import clock
from fc import Altivar212
from op_time_supervisor import OperatingTimeSupervisor, OperatingTimer
from post import Post

supervisor: OperatingTimeSupervisor = None
op_timer: OperatingTimer = None


def test_init():
    global supervisor, op_timer
    supervisor = OperatingTimeSupervisor(name='supervisor')
    post = Post(name='post_1', parent=None)
    fc = Altivar212(parent=post, name='fc')
    op_timer = fc.operation_timer
    supervisor.set_top_object(post)
    supervisor.init()

    assert supervisor.op_timers[0] == op_timer
    assert len(supervisor.op_timers)
    assert not supervisor.excess_msg.get(op_timer)


def test_send_regular():
    assert supervisor

    supervisor.next_send_regular_msg = datetime.datetime.now() + datetime.timedelta(hours=1)
    supervisor.receive_data()
    supervisor.send_data()

    supervisor.receive_data()
    op_timer.excess = True
    supervisor.send_data()

    supervisor.next_send_regular_msg = datetime.datetime.now() - datetime.timedelta(hours=1)
    supervisor.receive_data()
    supervisor.send_data()

    supervisor.receive_data()
    op_timer.excess = False
    supervisor.send_data()


