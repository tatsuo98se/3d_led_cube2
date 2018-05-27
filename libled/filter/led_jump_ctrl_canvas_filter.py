# -*- encoding:utf8 -*-
from led_canvs_filter import LedCanvasFilter
import time
from ..util.serial_manager import SerialManager

GRAVITY = 0.8
UPDATE_FREQ = 0.08

class LedJumpCtrlCanvasFilter(LedCanvasFilter):

    def __init__(self, canvas):
        super(LedJumpCtrlCanvasFilter, self).__init__(canvas)
        self.elapsed = 0
        self.last_update = time.time()
        self.initial_power = self.update_initial_power()
        self.power = self.update_initial_power() #テキトーな上昇する力の値

    def pre_draw(self):
        super(LedJumpCtrlCanvasFilter, self).pre_draw()
        param = SerialManager.get_data_as_json()
        if time.time() - self.last_update < UPDATE_FREQ:
            return

        self.power -= GRAVITY * (0.5 + param['a0'])
        if(self.power < -self.initial_power):
            self.initial_power = self.update_initial_power()
            self.power = self.initial_power
        self.last_update = time.time()

    def set_led(self, x, y, z, color):
        self.canvas.set_led(x, y + self.get_power(self.power) - self.get_power(self.initial_power), z, color)

    def get_power(self, power):
        return power * power

    def update_initial_power(self):
        param = SerialManager.get_data_as_json()
        return 2.5 * (0.5 + param['a1'])