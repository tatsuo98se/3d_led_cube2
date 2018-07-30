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
        self.yt = self.zt = 0
        self.last_update = time.time()
        self.axis = axis
        self.wav = 'asset/audio/se_swing.wav'
        self.ys = self.yc = 0
        self.zs = self.zc = 0
        self._pre_sign = -1

    def pre_draw(self):
        super(LedSkewedCanvasFilter, self).pre_draw()
        param = self.get_param_from_controller(defaults={'a0':0.4, 'a1':0.4, 'a2':0.5})
        yd = (param['a1'] - 0.5) / 4.0
        zd = (param['a2'] - 0.5) / 4.0
        speed = param['a0'] / 5.0 + 0.1
        self.yt += yd * speed
        self.zt += zd * speed
        self.ys = math.sin(self.yt*3.14*T)
        self.yc = math.cos(self.yt*3.14*T)
        self.zs = math.sin(self.zt*3.14*T)
        self.zc = math.cos(self.zt*3.14*T)

        sign = np.sign(self.ys)
        # play sound
        if self._pre_sign != sign:
            SoundInterface.play(wav=self.wav)
        self._pre_sign = sign


    def set_led(self, x, y, z, color):
        dx = LED_WIDTH / 2.0
        dy = LED_HEIGHT / 4.0 * 3
        dz = LED_DEPTH / 2.0
        if 'y' in self.axis:
            x, y, z = ((x - dx)*self.yc + (z - dz)*self.ys) + dx, y, (-(x - dx)*self.ys + (z - dz)*self.yc) + dz

        if 'z' in self.axis:
#            x = ((x0 - dx)*c + (z0 - dy)*s) + dx 
            x, y, z = ((x - dx)*self.zc + (y - dy)*self.zs) + dx, (-(x - dx)*self.zs + (y - dy)*self.zc) + dy, z

        self.canvas.set_led(x, y, z, color)
