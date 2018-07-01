# coding: UTF-8
import base64
import serial
import os.path
import time
import threading
import serial
from flask import Flask, abort
from flask import request
from Queue import Queue
from libled.led_run_loop import LedRunLoop
import json
from libled.util.serial_util import *
import libled.util.logger as logger
import zmq
import traceback
from time import sleep
from libled.util.flask_on_thread import FlaskOnThread

app = Flask(__name__)
tcp_port = 5601
zmq_port = tcp_port + 1
gamepad_state = ''

@app.route('/api/gamepad')
def gamepad():
    if gamepad_state == '':
        abort(503)
    return gamepad_state

flask = FlaskOnThread(app, port=tcp_port)
flask.daemon = True
flask.start()

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:" + str(zmq_port))

def find_controller_port():
    ports = enum_serial_posts()
    for port in ports:
        s = None
        try:
            s = serial.Serial(port, 9600, timeout=0.3)
            line = ''
            for _ in xrange(3): # try 3 times
                s.write("z")
                line = s.readline().strip()
                if not line == '':
                    j = json.loads(line)
                    if j['id'] == 'abcdef':
                        gamepad_state = line
                        return port
                sleep(0.1)
        except (OSError, serial.SerialException, ValueError):
            pass
        finally:
            if s is not None:
                s.close()

    return None

port = None
s = None
try:
    flask.check_error()
    logger.i("searching controller....")
    port = find_controller_port()

    if port is None:
        logger.e('game pad not found.')
        exit
    logger.i("find port: " + str(port))
    s = serial.Serial(port, 9600)

    logger.i("gamepad server has started on port" + str(tcp_port))

    while True:
        line = s.readline().strip()
        gamepad_state = line
        socket.send_string(line)

except:
    logger.e('HwControllerManager.init() failed.' + str(sys.exc_info()[0]))
    logger.e(traceback.format_exc())
