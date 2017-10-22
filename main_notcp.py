# coding: UTF-8
from libled.led_run_loop import LedRunLoop
import codecs
import sys

class LedRawTextClient(LedRunLoop):

    def __init__(self):
        super(LedRawTextClient, self).__init__()
        sys.stdin = codecs.getreader('shift_jis')(sys.stdin) # set input codec

    def on_finish(self):
        pass

    def on_keyboard_interrupt(self):
        pass

    def on_exception_at_runloop(self, exception):
        return LedRunLoop.EXIT

    def read_data(self):
        print('Please input order...')
        return raw_input('>>> ')

    def on_pre_exec_runloop(self):
        pass

    def on_post_exec_runloop(self):
        pass

LedRawTextClient().run()
