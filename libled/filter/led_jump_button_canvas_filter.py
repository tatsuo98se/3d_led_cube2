# -*- encoding:utf8 -*-
from led_canvs_filter import LedCanvasFilter
from ..led_cube import *
import time
import random
from ..util.hw_controller_bridge import get_data_as_json

GRAVITY = 0.8
UPDATE_FREQ = 0.08

class LedJumpButtonCanvasFilter(LedCanvasFilter):

    def __init__(self, canvas):
        super(LedJumpButtonCanvasFilter, self).__init__(canvas)
        self.elapsed = 0
        self.last_update = time.time()
        self.initial_power = 0
        self.power = 0
        self.push = 0

    def pre_draw(self):
        super(LedJumpButtonCanvasFilter, self).pre_draw()

        if time.time() - self.last_update < UPDATE_FREQ:
            return

        param = get_data_as_json(defaults={'d1':0.5})

        if self.push != param['d1'] and param['d1'] == 1:
            self.initial_power = self.update_initial_power()
            self.power = self.initial_power

        self.push = param['d1']

        self.power -= GRAVITY
        if self.power < -self.initial_power:
            self.initial_power = 0
            self.power = 0

        self.last_update = time.time()

    def set_led(self, x, y, z, color):
        self.canvas.set_led(x, y + self.get_power(self.power) - self.get_power(self.initial_power), z, color)

    def get_power(self, power):
        return power * power

    def update_initial_power(self):
        return 3 #random.uniform(2.5,4)