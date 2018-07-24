# coding: UTF-8
import os.path
import time
import threading
import json
import pprint
import csv
from datetime import datetime
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
from libled.util.flask_on_thread import FlaskOnThread
from libled.util.sound_interface import SoundInterface
from PIL import Image as pimg

SoundInterface.content_id = 'paint'


def save_image(data, filename):
    image = pimg.new('RGB', (LED_WIDTH, LED_HEIGHT))
    pixels = image.load()
    for x in range(LED_WIDTH):
        for y in range(LED_HEIGHT):
            color = Color.int_to_color(int(str(data[x][y]), 16))
            pixels[x, y] = color.to_rgb255()
    image.save(filename, 'PNG')

class FlaskWithHamlish(Flask):
    jinja_options = ImmutableDict(
        extensions=['jinja2.ext.autoescape', 'jinja2.ext.with_', 'hamlish_jinja.HamlishExtension']
    )
app = FlaskWithHamlish(__name__)

q = Queue()
q.put('show:' + json.dumps({'orders': [{'id':'object-painting', 'lifetime':0}]}))

@app.route('/')
def index():
    return render_template('index.haml')

@app.route('/api/filters', methods=['POST'])
def api_filter():
    filters = json.loads(request.data)['filters']

    filters.append({'id':'object-painting', 'lifetime':0})

    orders = {'orders': filters}
    q.put('show:' + json.dumps(orders))
    return ""

@app.route('/api/stamp' , methods=['POST'])
def api_stamp():
    print("api_stamp()*******************")
    filename = "stamp_params/"+str(datetime.now())+".csv"
    writecsv = csv.writer(file(filename,'w'))
    stamp_params = json.loads(request.data)['stamp_params']
    pprint.pprint(stamp_params)
    writecsv.writerow(stamp_params)
    return ""

@app.route('/api/led', methods=['POST'])
def api_led():
    data = json.loads(request.data)
    if 'points' in data:
        points = data['points']
        for point in points:
            color = int(str(point['color']), 16)
            logger.d("x:{0}, y:{1}, color:{2}".format(point['x'], point['y'], color))
            PaintManager.get_instance().set_color( \
                                                int(point['x']), 
                                                int(point['y']), 
                                                Color.int_to_color(color))

    else:
        # save order
        logorder = datetime.now().strftime('%Y%m%d-%H-%M-%S-%f')[:-3]
        filename = 'log/painting_history/' + logorder + '.png'
        save_image(data['led'], filename)
        for x in range(LED_WIDTH):
            for y in range(LED_HEIGHT):
                PaintManager.get_instance().set_color(x, y, Color.int_to_color(int(str(data['led'][x][y]), 16)))
    return ""


@app.route('/api/abort', methods=['POST'])
def abort():
    q.put('abort')
    return ""

@app.route('/api/audio', methods=['POST'])
def audio():
    volume = float(json.loads(request.data)['volume'])
    SoundInterface.volume(val=volume/100.0)
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


flask = FlaskOnThread(app, port=5302)
flask.daemon = True
flask.start()

LedPaintHttpServer().run()
