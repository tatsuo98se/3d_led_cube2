from led_object import LedObject
from ..led_cube import *
from ..util.vectors_util import *
import math
from ..util.sound_player import SoundPlayer as sp
import numpy as np

N = 200
PS = 1000

def red(ix):
    i = int(ix) % 90
    if i < 30:
        return i * 255 / 30
    elif i < 60:
        return (60 - i) * 255 / 30
    else:
        return 0

def rgb(ix):
    n = math.floor(ix * 1 * 90)
    return red(n) * 0x10000 + red(n+30) * 0x100 + red(n+60) * 0x1

def darken(x):
    r = ((int(x) & 0xff0000) * 49 / 50) & 0xff0000
    g = ((int(x) & 0xff00) * 49 / 50) & 0xff00
    b = ((int(x) & 0xff) * 49 / 50) & 0xff
    return r + g + b

class LedFireworksObject(LedObject):

    def __init__(self, lifetime = 0 ):
        super(LedFireworksObject, self).__init__(lifetime)
        self.ix = 0
        self.vs = []
        self.poss = []
        self.wavs = ['asset/audio/se_fireworks.wav', 
                     'asset/audio/se_fireworks2.wav',
                     'asset/audio/se_fireworks3.wav']

    def draw(self, canvas):
        if  self.ix % 20 == 0 :
            cx = LED_WIDTH * np.random.rand()
            cy = LED_HEIGHT * np.random.rand()
            cz = LED_DEPTH * np.random.rand()
            for i in range(PS):
                sf = sphere_face()
                self.vs.append(sf)
                self.poss.append(Xyzc_t(Xyz_t(cx, cy, cz), rgb(sf.len())))
            
            # play sound
            wav = np.random.choice(self.wavs, 1, p=[0.7, 0.2, 0.1])[0]
            sp.instance().do_play(wav)

        delete_idx = []
        for i in range(len(self.poss)):

            p = self.poss[i]
            v = self.vs[i]
            if can_show(p.p):
                canvas.set_led(p.p.x, p.p.y, p.p.z, int(p.color))
            else:
                delete_idx.append(i)
            p.p = p.p + v
            p.color = darken(p.color)

        delete_idx.reverse()
        for i in delete_idx:
            del self.poss[i]
            del self.vs[i]

        self.ix += 1
