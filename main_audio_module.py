# -*- encoding:utf-8 -*-
'''
音楽再生モジュール
別プロセスで音楽を再生するために作成

使い方

'''

import time
import json
from flask import Flask, request
from Queue import Queue
from libled.led_run_loop import LedRunLoop
from libled.util.common_util import *
from libled.util.flask_on_thread import FlaskOnThread
from libled.util.sound_player import SoundPlayer
from libled.util.logger import logger


app = Flask(__name__)
q = Queue()


def run():
    flask = FlaskOnThread(app)
    flask.daemon = True
    flask.star()
    SoundPlayingServer().run()


class SoundPlayingServer(LedRunLoop):

    def __init__(self):
        super(SoundPlayingServer, self).__init__()

    def on_exception_at_runloop(self, exception):
        return LedRunLoop.EXIT

    def read_data(self):
        while True:
            if self.aborted:
                break

            if q.empty():
                time.sleep(0.1)
            else:
                return q.get()


@app.route('/')
def hello_world():
    return 'Hello Audio module!'


@app.route('/api/play', methods=['POST'])
def play():
    logger.d('call play rest-api audio module.')
    pass


@app.route('/api/stop', methods=['POST'])
def stop():
    logger.d('call stop rest-api audio module.')
    pass


@app.route('/api/volume', methods=['POST'])
def vol():
    logger.d('call volume rest-api audio module.')
    pass


@app.route('/api/pause', methods=['POST'])
def pause():
    logger.d('call pause rest-api audio module.')
    pass


@app.route('/api/resume', methods=['POST'])
def resume():
    logger.d('call resume rest-api audio module.')
    pass


def get_request():
    return json.loads(request.data)


# run module
run()
