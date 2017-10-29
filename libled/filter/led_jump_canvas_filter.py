# -*- encoding:utf8 -*-
from led_canvs_filter import LedCanvasFilter
from ..led_cube import *
import time
import random

GRAVITY = 0.8
UPDATE_FREQ = 0.08

class LedJumpCanvasFilter(LedCanvasFilter):

    def __init__(self, canvas):
        super(LedJumpCanvasFilter, self).__init__(canvas)
        self.elapsed = 0
        self.last_update = time.time()
        self.initial_power = self.update_initial_power()
        self.power = self.update_initial_power() #テキトーな上昇する力の値

    def pre_draw(self):
        super(LedJumpCanvasFilter, self).pre_draw()
        if time.time() - self.last_update < UPDATE_FREQ:
            return

        self.power -= GRAVITY
        if(self.power < -self.initial_power):
            self.initial_power = self.update_initial_power()
            self.power = self.initial_power
        self.last_update = time.time()

    def set_led(self, x, y, z, color):
        self.canvas.set_led(x, y + self.get_power(self.power) - self.get_power(self.initial_power), z, color)

    def get_power(self, power):
        return power * power

    def update_initial_power(self):
        return random.uniform(2.5,4)