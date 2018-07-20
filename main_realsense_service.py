# coding: UTF-8
from libled.led_run_loop import LedRunLoop
import codecs
import sys
import platform
import time
import json
from Queue import Queue
from flask import Flask, request
from libled.util.flask_on_thread import FlaskOnThread
from libled.util.sound_player import SoundPlayer

q = Queue()

app = Flask(__name__)

@app.route('/api/audio', methods=['POST'])
def audio():
    volume = float(json.loads(request.data)['volume'])
    SoundPlayer.instance().set_volume(volume/100.0)
    return ""

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

flask = FlaskOnThread(app, port=5402)
flask.daemon = True
flask.start()

LedRawTextClient().run()

