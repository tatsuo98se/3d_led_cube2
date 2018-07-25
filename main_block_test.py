# coding: UTF-8
from libled.led_run_loop import LedRunLoop
import codecs
import sys
import platform
from libled.util.sound_interface import SoundInterface
from flask import Flask
from flask import request
from libled.util.flask_on_thread import FlaskOnThread
import json

app = Flask(__name__)
SoundInterface.content_id = 'block_test'

@app.route('/api/audio', methods=['POST'])
def audio():
    volume = float(json.loads(request.data)['volume'])
    SoundInterface.volume(val=volume/100.0)
    return ""

class LedRawTextClient(LedRunLoop):

    def __init__(self):
        super(LedRawTextClient, self).__init__()
        if sys.platform == 'win32':
            sys.stdin = codecs.getreader('shift_jis')(sys.stdin) # set input codec
        SoundInterface.content_id = 'block_test'

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

flask = FlaskOnThread(app, port=5802)
flask.daemon = True
flask.start()

LedRawTextClient().run()
