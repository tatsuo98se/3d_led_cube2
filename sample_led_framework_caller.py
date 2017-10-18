import base64
from led_framework import LedFramework

dic = None
with open("asset/image/luigi_run_1.png", "rb") as luigi1, \
       open("asset/image/luigi_run_2.png", "rb") as luigi2 :

    dic = {"orders":
        [
            {"id" : "object-bk-mountain", "lifetime":30, "z":6, "overlap":True, "cycle":7},
            {"id" : "object-bk-cloud", "lifetime":30, "z":7, "overlap":True, "cycle":20},
            {"id" : "object-bk-grass", "lifetime":30, "z":4, "overlap":True, "cycle":4},
            {"id" : "ctrl-loop", "count":20},
            {"id" : "object-bitmap", "lifetime":0.5, "bitmap":base64.b64encode(luigi1.read())},
            {"id" : "object-bitmap", "lifetime":0.5, "bitmap":base64.b64encode(luigi2.read())},
        ]
    }


led = LedFramework()
led.show(dic)