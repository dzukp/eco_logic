from fake_periodic_clock import clock
from fc import Altivar212

from operating_time import OperatingTimer
from post import Post


def test_operating_timer():
    post = Post(name='post_1', parent=None)
    fc = Altivar212(parent=post, name='fc')
    o = fc.operation_timer
    o.process()

    o.run(False)
    clock.set_time(2.0 * 3600)
    o.process()
    assert o.next_save > 0

    o.run(True)
    clock.set_time(4.0 * 3600)
    o.process()
    assert o.get_operating_hours() == 2.0

    o.run(False)
    clock.set_time(6.0 * 3600)
    o.process()
    assert o.get_operating_hours() == 2.0
    assert o.next_save > o.operating_time
    assert o.next_save % o.save_step == 0
