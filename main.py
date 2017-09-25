# coding: UTF-8
from optparse import OptionParser
from libled.led_cube import *
from libled.util.led_block_util import *
import importlib
import os.path
import led_framework
import threading
from Queue import Queue
import time
from libled.util.color import Color
from libled.object.led_object import LedObject
from libled.object.led_dot_obj import LedDotObject
from libled.object.led_ripple_obj import LedRippleObject
from libled.object.led_fill_obj import LedFillObject
from libled.object.led_random_ripple_obj import LedRandomRippleObject
from libled.led_canvas import LedCanvas
from libled.i_led_canvas import ILedCanvas
from libled.filter.led_canvs_filter import LedCanvasFilter
from libled.filter.led_test_canvas_filter import LedTestCanvasFilter
from libled.filter.led_wave_canvas_filter import LedWaveCanvasFilter
from libled.filter.led_hsv_canvas_filter import LedHsvCanvasFilter
import sys
import traceback
import socket
import json

# Hostnameを取るための仮接続
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("0.0.0.0", 80))
hostname = s.getsockname()[0]
s.close()
print(hostname)


parser = OptionParser()
parser.add_option("-d", "--dest",
                  action="store", type="string", dest="dest", 
                  help="(optional) ip address of destination device which connect to real 3d cube.")

(options, args) = parser.parse_args()

if options.dest != None:
    led.SetUrl(options.dest)


test_data1 = {"filter-2","object-2","object-1","object-2","object-1","filter-0","object-2","object-1"} # this line will be json
#led_framework.show(led, test_data)

#th = threading.Thread(name="show", target=led_framework.show, args=(led, test_data))
#th.start()
#th.join()

#canvas = LedCanvas()
#canvas = LedHsvCanvasFilter(canvas)
#canvas = LedWaveCanvasFilter(canvas)

#canvas.add_object(LedDotObject(3, 3, 0, 0xffffff,5))
#canvas.add_object(LedRippleObject(3, 3, Color(0xff, 0xff, 0xff)))
#canvas.add_object(LedFillObject(Color(0xff, 0xff, 0xff)))
#canvas.add_object(LedRandomRippleObject(5))

message = Queue()
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((hostname, 20000))
serversocket.listen(1)
sock = None
sf = None


def message_receive_loop(q):
    global sock
    global sf

    try:
        while True:
            try:
                print('Waiting for connections...')
                sock, client_address = serversocket.accept() #接続されればデータを格納

                # ファイルオブジェクトを作成
                sf = sock.makefile()

                # 1行読み取る場合
                while True:
                    print('waiting data...')
                    line = sf.readline()
                    print('receive in thread: ' + line)
                    if not line:
                        break

                    q.put(line)

                sock.close()
                print('disconnected.')
            except socket.timeout:
                continue

    except:
        print("Unexpected error:", sys.exc_info()[0])
        print(traceback.format_exc())
        raise
    finally:
        print('finish')


th = threading.Thread(name="message_receive_loop", target=message_receive_loop, args=(message,))
th.setDaemon(True)
th.start()

try:
    while True:
        if message.empty():
            time.sleep(0.1)
        else:
            data = json.loads(message.get())

            print("receive: " + data)

except KeyboardInterrupt:
    print('keybord Ctrl+C')
    sf.close()
    sock.close()
finally:
    serversocket.shutdown(socket.SHUT_RDWR)
    serversocket.close()
    th.join()
    print('finish')
