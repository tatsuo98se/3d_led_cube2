# coding: UTF-8
import os.path
import time
import threading
from Queue import Queue
from libled.led_run_loop import LedRunLoop
from flask import Flask, render_template
from flask import request
from os import listdir
from os.path import isfile, join
from libled.util.common_util import *
from werkzeug import ImmutableDict
from libled.led_cube import *
from libled.util.color import Color
from libled.util.paint_manager import PaintManager

class FlaskWithHamlish(Flask):
    jinja_options = ImmutableDict(
        extensions=['jinja2.ext.autoescape', 'jinja2.ext.with_', 'hamlish_jinja.HamlishExtension']
    )
app = FlaskWithHamlish(__name__)

q = Queue()

@app.route('/')
def index():
    q.put('show:' + "{\"orders\":[{\"id\":\"object-painting\", \"lifetime\":0}]}")
    return render_template('index.haml')


@app.route('/api/led', methods=['POST'])
def api_led():
    print('param:' + str(request.args))

    for x in range(16):
        datalist_id = "led[{0}][]".format(x)
        datalist = request.form.getlist(datalist_id)
        for y in range(32):
            PaintManager.get_instance().set_color(x, y,  Color.int_to_color(int(datalist[y], 16)))
    return ""


@app.route('/api/abort', methods=['POST'])
def abort():
    q.put('abort')
    return ""

class LedPaintHttpServer(LedRunLoop):

    def __init__(self):
        super(LedPaintHttpServer, self).__init__()

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


class FlaskThread(threading.Thread):

    def __init__(self, app, host='0.0.0.0', port=5301):
        super(FlaskThread, self).__init__()
        self.app = app
        self.host = host
        self.port = port
    
    def run(self):
        self.app.run(
            debug=False,
            host=self.host,
            port=int(self.port)
        )
        

flask = FlaskThread(app)
flask.daemon = True
flask.start()

LedPaintHttpServer().run()
