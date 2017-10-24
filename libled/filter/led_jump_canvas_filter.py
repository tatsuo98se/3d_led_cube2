# -*- encoding:utf8 -*-
from led_canvs_filter import LedCanvasFilter
from ..led_cube import *
import time

INITIAL_POWER = 4

class LedJumpCanvasFilter(LedCanvasFilter):


    def __init__(self, canvas):
        super(LedJumpCanvasFilter, self).__init__(canvas)
        self.elapsed = 0
        self.power = INITIAL_POWER #テキトーな上昇する力の値
        self.last_update = time.time()

    def pre_draw(self):
        if time.time() - self.last_update < 0.1:
            return

        self.power -= 0.5
        if(self.power < -INITIAL_POWER):
            self.power = INITIAL_POWER
        self.last_update = time.time()
        
    def set_led(self, x, y, z, color):
        self.canvas.set_led(x, y + self.get_power(self.power) - self.get_power(INITIAL_POWER), z, color)

    def get_power(self, power):
        return power * power
