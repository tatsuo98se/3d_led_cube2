# coding: UTF-8
from libled.led_run_loop import LedRunLoop
import codecs
import sys
import platform
import time
from Queue import Queue
q = Queue()

class LedRawTextClient(LedRunLoop):

    def __init__(self):
        super(LedRawTextClient, self).__init__()
        if sys.platform == 'win32':
            sys.stdin = codecs.getreader('shift_jis')(sys.stdin) # set input codec

    def on_keyboard_interrupt(self):
        q.put('abort')
        pass

    def on_exception_at_runloop(self, exception):
        return LedRunLoop.EXIT

    def read_data(self):
        print("waiting data.")
        while True:
            if self.aborted:
                break

            if q.empty():
                time.sleep(0.1)
            else:
                return q.get()

q.put('show:{"orders":[{"id":"filter-zanzo"},{"id":"object-realsense", "lifetime":0}]}')
LedRawTextClient().run()

