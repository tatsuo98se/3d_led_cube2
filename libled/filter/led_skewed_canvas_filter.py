from led_canvs_filter import LedCanvasFilter
from ..led_cube import *
from ..util.color import Color
import math
import time
import numpy as np
from ..util.sound_interface import SoundInterface

T = 4

class LedSkewedCanvasFilter(LedCanvasFilter):

    def __init__(self, canvas, axis=['y'], enable_controller=False):
        super(LedSkewedCanvasFilter, self).__init__(canvas, enable_controller)
        self.t = 0
        self.last_update = time.time()
        self.axis = axis
        self.wav = 'asset/audio/se_swing.wav'
        self.s = self.c = 0
        self._pre_sign = -1

    def pre_draw(self):
        super(LedSkewedCanvasFilter, self).pre_draw()
        param = self.get_param_from_controller(defaults={'a0':0.4, 'a1':0.5})
        direction = (param['a0'] - 0.5)
        speed = param['a1'] / 5.0
        self.t += direction * speed
        self.s = math.sin(self.t*3.14*T)
        self.c = math.cos(self.t*3.14*T)

        sign = np.sign(self.s)
        # play sound
        if self._pre_sign != sign:
            SoundInterface.play(wav=self.wav)
        self._pre_sign = sign


    def set_led(self, x, y, z, color):
        dx = LED_WIDTH / 2.0
        dy = LED_HEIGHT / 4.0 * 3
        dz = LED_DEPTH / 2.0
        if 'y' in self.axis:
            x, y, z = ((x - dx)*self.c + (z - dz)*self.s) + dx, y, (-(x - dx)*self.s + (z - dz)*self.c) + dz

        if 'z' in self.axis:
#            x = ((x0 - dx)*c + (z0 - dy)*s) + dx 
            x, y, z = ((x - dx)*self.c + (y - dy)*self.s) + dx, (-(x - dx)*self.s + (y - dy)*self.c) + dy, z

        self.canvas.set_led(x, y, z, color)
