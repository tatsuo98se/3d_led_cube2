from led_canvs_filter import LedCanvasFilter
from ..led_cube import *
from ..util.color import Color
import math
import time

class LedWakameCanvasFilter(LedCanvasFilter):

    def __init__(self, canvas):
        super(LedWakameCanvasFilter, self).__init__(canvas)
        self.t = 0

    def show(self, canvas = None):
        self.t += 1
        super(LedWakameCanvasFilter, self).show(canvas)

    def set_led(self, x, y, z, color):

        p = (self.t+y)/2
        sx = math.sin(p)
        sz = math.cos(p)
        self.canvas.set_led(x+sx, y, z+sz, color)
