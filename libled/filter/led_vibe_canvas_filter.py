from led_canvs_filter import LedCanvasFilter
from ..led_cube import *
from ..util.color import Color
import math
import time

class LedVibeCanvasFilter(LedCanvasFilter):

    def __init__(self, canvas):
        super(LedVibeCanvasFilter, self).__init__(canvas)
        self.t = 0

    def show(self, canvas = None):
        self.t += 40
        super(LedVibeCanvasFilter, self).show(canvas)

    def set_led(self, x, y, z, color):

        p = (self.t)
        sx = math.sin(p)
        sz = math.cos(p)
        self.canvas.set_led(x+sx, y, z+sz, color)
