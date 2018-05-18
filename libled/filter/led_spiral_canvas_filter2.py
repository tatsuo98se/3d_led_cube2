from led_canvs_filter import LedCanvasFilter
from ..led_cube import *
from ..util.color import Color
import math
import time

class LedSpiralCanvasFilter2(LedCanvasFilter):

    def __init__(self, canvas):
        super(LedSpiralCanvasFilter2, self).__init__(canvas)
        self.t = 0

    def show(self, canvas = None):
        self.t += 1
        super(LedSpiralCanvasFilter2, self).show(canvas)

    def set_led(self, x0, y, z0, color):

        T = 8
        deg = (math.sin((self.t+y)/5) + 0.3) / 1.3
        s = math.sin(deg)
        c = math.cos(deg)
        dx = LED_WIDTH / 2
        dz = LED_DEPTH / 2
        x = ((x0 - dx)*c + (z0 - dz)*s) + dx
        z = (-(x0 - dx)*s + (z0 - dz)*c) + dz
        self.canvas.set_led(x, y, z, color)
