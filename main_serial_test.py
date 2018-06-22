# coding: UTF-8
import base64
import serial
import os.path
import time
import threading
from Queue import Queue
from libled.led_run_loop import LedRunLoop
import json

laststate = 0
ser = serial.Serial('/dev/cu.usbmodem1411', 9600)

dic = None
with open("asset/image/luigi_run_1.png", "rb") as luigi1, \
       open("asset/image/luigi_run_2.png", "rb") as luigi2 :

    dic = {"orders":
        [
            {"id" : "object-bk-mountain", "lifetime":30, "z":6, "overlap":True, "cycle":7},
            {"id" : "object-bk-cloud", "lifetime":30, "z":7, "overlap":True, "cycle":20},
            {"id" : "object-bk-grass", "lifetime":30, "z":4, "overlap":True, "cycle":4},
            {"id" : "ctrl-loop", "count":20},
            {"id" : "object-bitmap", "lifetime":0.1, "bitmap":base64.b64encode(luigi1.read())},
            {"id" : "object-bitmap", "lifetime":0.1, "bitmap":base64.b64encode(luigi2.read())},
        ]
    }


q = Queue()


class LedSerialButton(LedRunLoop):

    def __init__(self):
        super(LedSerialButton, self).__init__()

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


class SerialThread(threading.Thread):

    def __init__(self, ):
        super(SerialThread, self).__init__()
        self._laststate = 0
    
    def run(self):
        try:
            while True:
                line = ser.readline().strip()
                if self._laststate == line:
                    continue

                if line == '1':
                    print('Switch ON!')
                    q.put('show:' + json.dumps(dic))
                else:
                    print('Switch OFF!')
                print(line)

                self._laststate = line

        except:
            ser.close()
        

serial_thread = SerialThread()
serial_thread.daemon = True
serial_thread.start()

LedSerialButton().run()
