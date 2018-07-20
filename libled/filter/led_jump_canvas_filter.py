# -*- encoding:utf8 -*-
from led_canvs_filter import LedCanvasFilter
from ..led_cube import *
import time
from ..util.sound_player import SoundPlayer as sp

GRAVITY = 0.8
UPDATE_FREQ = 0.08

class LedJumpCanvasFilter(LedCanvasFilter):

    def __init__(self, canvas, enable_controller = False):
        super(LedJumpCanvasFilter, self).__init__(canvas, enable_controller)
        self.elapsed = 0
        self.last_update = time.time()
        self.initial_power = self.update_initial_power()
        self.power = self.update_initial_power()  # テキトーな上昇する力の値
        self.wav = 'asset/audio/se_jump.wav'
        sp.instance().do_play(self.wav)

    def pre_draw(self):
        super(LedJumpCanvasFilter, self).pre_draw()
        param = self.get_param()
        if time.time() - self.last_update < UPDATE_FREQ:
            return

        self.power -= GRAVITY * (0.5 + param['a0'])
        if(self.power < -self.initial_power):
            self.initial_power = self.update_initial_power()
            self.power = self.initial_power
            sp.instance().do_play(self.wav)

        self.last_update = time.time()

    def set_led(self, x, y, z, color):
        self.canvas.set_led(x, y + self.get_power(self.power) -
                            self.get_power(self.initial_power), z, color)

    def get_power(self, power):
        return power * power

    def get_param(self):
        return self.get_param_from_controller(defaults={'a0':0.5, 'a1':0.8})

    def update_initial_power(self):
        param = self.get_param()
        return 2.5 * (0.5 + param['a1'])