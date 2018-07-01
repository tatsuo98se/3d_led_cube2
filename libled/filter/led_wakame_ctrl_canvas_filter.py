from led_canvs_filter import LedCanvasFilter
from ..led_cube import *
from ..util.color import Color
from ..util.hw_controller_util import get_data_as_json
import math
import time

class LedWakameCtrlCanvasFilter(LedCanvasFilter):

    def __init__(self, canvas):
        super(LedWakameCtrlCanvasFilter, self).__init__(canvas)
        self.t = 0

    def pre_draw(self):
        super(LedWakameCtrlCanvasFilter, self).pre_draw()
        param = get_data_as_json(defaults={'a0':0.5, 'a1':0.5})
        self.t += 3 * param['a0']
        self.shift = 0.8 + param['a1'] * 3
 
    def set_led(self, x, y, z, color):

        p = (self.t+y)/2
        sx = math.sin(p) * self.shift
        sz = math.cos(p) * self.shift
        self.canvas.set_led(x+sx, y, z+sz, color)
