# coding: UTF-8
from libled.led_run_loop import LedRunLoop
import urllib2

class LedHttpClient(LedRunLoop):

    def __init__(self):
        super(LedHttpClient, self).__init__()

    def on_finish(self):
        pass

    def on_keyboard_interrupt(self):
        pass

    def on_exception_at_runloop(self, exception):
        return LedRunLoop.EXIT

    def read_data(self):
        print('Press Enter...')
        input_word = raw_input('>>> ')

        return urllib2.urlopen("http://172.27.175.176:5000/api/content/2").read()

    def on_pre_exec_runloop(self):
        pass

    def on_post_exec_runloop(self):
        pass

LedHttpClient().run()
