# coding: UTF-8
from libled.led_run_loop import LedRunLoop
import codecs
import sys
import platform

class LedRawTextClient(LedRunLoop):

    def __init__(self):
        super(LedRawTextClient, self).__init__()
        if sys.platform == 'win32':
            sys.stdin = codecs.getreader('shift_jis')(sys.stdin) # set input codec

    def on_finish(self):
        pass

    def on_keyboard_interrupt(self):
        pass

    def on_exception_at_runloop(self, exception):
        return LedRunLoop.EXIT

    def read_data(self):
        return 'show:{"orders":[{"id":"filter-zanzo"},{"id":"object-realsense", "lifetime":120}]}'

    def on_pre_exec_runloop(self):
        pass

    def on_post_exec_runloop(self):
        pass

LedRawTextClient().run()
