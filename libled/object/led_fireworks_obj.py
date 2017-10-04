from led_object import LedObject
from ..led_cube import *
from ..util.vectors_util import *
import math
import random

N = 200
PS = 1000

class LedFireworksObject(LedObject):

    def __init__(self, lifetime = 0 ):
        super(LedFireworksObject, self).__init__(lifetime)
        self.ix = 0
        self.vs = []
        self.poss = []

    def draw(self, canvas):
        if  self.ix % 20 == 0 :
            cx = LED_WIDTH * random.random()
            cy = LED_HEIGHT * random.random()
            cz = LED_DEPTH * random.random()
            for i in range(PS):
                sf = sphere_face()
                self.vs.append(sf)
                self.poss.append(Xyzc_t(Xyz_t(cx, cy, cz), rgb(sf.len())))

        for i in range(len(self.poss)):

            p = self.poss[i]
            v = self.vs[i]
            if can_show(p.p):
                canvas.set_led(p.p.x, p.p.y, p.p.z, int(p.color))
            p.p = p.p + v
            p.color = darken(p.color)

        self.ix += 1
