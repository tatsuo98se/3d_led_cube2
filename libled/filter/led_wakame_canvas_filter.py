from led_canvs_filter import LedCanvasFilter
from ..led_cube import *
from ..util.color import Color
import math
import time

class LedWakameCanvasFilter(LedCanvasFilter):

    def __init__(self, canvas, enable_controller=False):
        super(LedWakameCanvasFilter, self).__init__(canvas, enable_controller)
        self.t = 0

    def pre_draw(self):
        super(LedWakameCanvasFilter, self).pre_draw()
        param = self.get_param_from_controller(defaults={'a0':0.5, 'a1':0.5})
        self.t += 3 * param['a0']
        self.shift = 0.8 + param['a1'] * 3
 
    def set_led(self, x, y, z, color):
        p = (self.t+y)/2
        sx = math.sin(p) * self.shift
        sz = math.cos(p) * self.shift
        self.canvas.set_led(x+sx, y, z+sz, color)
