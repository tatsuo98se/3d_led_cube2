# coding: UTF-8
import os.path
import time
import threading
from Queue import Queue
from libled.led_run_loop import LedRunLoop
from flask import Flask
from flask import request
import json
from os import listdir
from os.path import isfile, join
from libled.util.common_util import *
from libled.util.flask_on_thread import FlaskOnThread
from libled.util.sound_player import SoundPlayer

app = Flask(__name__)
q = Queue()


def get_logfiles(content_id):
    logpath = "./log/"+ str(content_id)
    logfiles = [join(logpath, f) for f in listdir(logpath) if isfile(join(logpath, f)) and not f.startswith('.') ]
    logfiles.sort(reverse=True)
    return logfiles

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/api/content/<content_id>/<rev_id>')
def get_content(content_id, rev_id):
    logfiles = get_logfiles(content_id)
    i = to_int_safe(rev_id)

    if len(logfiles) > 0 and i < len(logfiles) and os.path.isfile(logfiles[i]):
    	return open(logfiles[i]).read()
    else:
        return "(no contents)"


@app.route('/api/show', methods=['POST'])
def show():
    print('body:' + str(request.data))
    q.put('show:' + str(request.data))
    return ""

@app.route('/api/abort', methods=['POST'])
def abort():
    q.put('abort')
    return ""

@app.route('/api/audio', methods=['POST'])
def audio():
    volume = float(json.loads(request.data)['volume'])
    SoundPlayer.instance().set_volume(volume/100.0)
    return ""



class LedBlockHttpServer(LedRunLoop):

    def __init__(self):
        super(LedBlockHttpServer, self).__init__()

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


flask = FlaskOnThread(app)
flask.daemon = True
flask.start()

LedBlockHttpServer().run()
