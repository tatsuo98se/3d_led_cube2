from led_canvs_filter import LedCanvasFilter
from ..led_cube import *
from ..util.color import Color
import math
import time

class LedSpiralCanvasFilter(LedCanvasFilter):

    def __init__(self, canvas):
        super(LedSpiralCanvasFilter, self).__init__(canvas)
        self.t = 0

    def show(self, canvas = None):
        self.t += 5
        super(LedSpiralCanvasFilter, self).show(canvas)

    def set_led(self, x0, y, z0, color):

        T = 4
        s = math.sin((self.t+y*20)*3.14*T)
        c = math.cos((self.t+y*20)*3.14*T)
        dx = LED_WIDTH / 2
        dz = LED_DEPTH / 2
        x = ((x0 - dx)*c + (z0 - dz)*s) + dx
        z = (-(x0 - dx)*s + (z0 - dz)*c) + dz
        self.canvas.set_led(x, y, z, color)
