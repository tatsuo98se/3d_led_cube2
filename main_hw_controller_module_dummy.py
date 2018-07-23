# coding: UTF-8
import base64
import serial
import os.path
import time
import threading
import serial
from flask import Flask, abort
from flask import request
from flask import Flask, render_template
from libled.led_run_loop import LedRunLoop
from Queue import Queue
import json
from werkzeug import ImmutableDict
from libled.util.serial_util import *
import libled.util.logger as logger
import zmq
import traceback
from time import sleep
from libled.util.flask_on_thread import FlaskOnThread

class FlaskWithHamlish(Flask):
    jinja_options = ImmutableDict(
        extensions=['jinja2.ext.autoescape', 'jinja2.ext.with_', 'hamlish_jinja.HamlishExtension']
    )

app = FlaskWithHamlish(__name__)
tcp_port = 5601
zmq_port = tcp_port + 1
gamepad_state = {"a0":0.5, "a1":0.5, "a2":0.5, "d1":0}
q = Queue()

@app.route('/')
def index():
    return render_template('dummy_controller.haml')

@app.route('/api/gamepad', methods=['POST'])
def set_gamepad():
    global gamepad_state
    gamepad_state.update(json.loads(request.data))
    q.put(json.dumps(gamepad_state))
    return ''

@app.route('/api/gamepad')
def gamepad():
    global gamepad_state
    return json.dumps(gamepad_state)

flask = FlaskOnThread(app, port=tcp_port)
flask.daemon = True
flask.start()

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:" + str(zmq_port))

try:
    flask.check_error()
    logger.i("searching controller....")

    while True:
        try:
            socket.send_string(q.get(timeout=1))
        except KeyboardInterrupt:
            break
        except:
            continue

except:
    logger.e('HwControllerManager.init() failed.' + str(sys.exc_info()[0]))
    logger.e(traceback.format_exc())
finally:
    if socket is not None:
        socket.close()
    if context is not None:
        context.term()
 
