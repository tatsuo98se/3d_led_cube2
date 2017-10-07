# coding: UTF-8
from led_object import LedObject
from ..led_cube import *
from ..util import vectors_util as Vectors
import numpy as np
import math


class LedRepbangObject(LedObject):

    def __init__(self, lifetime=0):
        super(LedRepbangObject, self).__init__(lifetime)
        self.ix = 0
        vec_length = 4000
        self.ps = [0] * vec_length
        for i in range(0, vec_length):
            self.ps[i] = self.rnd()

        self.ix = 0
        self.N = 216

    def draw(self, canvas):
        speed = 1.6
        r = 1 - math.cos(self.ix * math.pi / self.N * 8)
        t = self.ix * math.pi / self.N * 16
        for p in self.ps:
            q = Vectors.Xyz_t(math.cos(t) * p.p.x - math.sin(t) * p.p.z,
                              p.p.y,
                              math.sin(t) * p.p.x + math.cos(t) * p.p.z)
            pos = q * r * LED_HEIGHT + \
                Vectors.Xyz(LED_WIDTH, LED_HEIGHT, LED_DEPTH) * 0.5

            if Vectors.can_show(pos):
                canvas.set_led(pos.x, pos.y, pos.z, p.color)

        self.ix += speed

    def rnd(self):
        length = 4
        rnd = np.random.randint(0x1000000)
        rng = np.random.uniform(-1.0, 1.0, length)
        x = rng[0]
        y = rng[1]
        z = rng[2]
        r = rng[3] / math.sqrt(x * x + y * y + z * z + 1e-5)
        return Vectors.Xyzc_t(Vectors.Xyz_t(x * r, y * r, z * r), rnd)
