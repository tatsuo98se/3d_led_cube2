from led_canvs_filter import LedCanvasFilter
from ..led_cube import *
from ..util.color import Color
import math
import time

class LedSwayingCanvasFilter(LedCanvasFilter):

    def __init__(self, canvas, dx = LED_WIDTH/2, dy = LED_HEIGHT, swaying = 0.015):
        super(LedSwayingCanvasFilter, self).__init__(canvas)
        self.born_at = time.time()
        self.dx = dx
        self.dy = dy
        self.swaying = swaying


    def set_led(self, x0, y0, z, color):
        swaying = math.cos((time.time() - self.born_at) * 4) * self.swaying
        T = 4
        s = math.sin(swaying*3.14*T)
        c = math.cos(swaying*3.14*T)
        x = ((x0 - self.dx)*c + (y0 - self.dy)*s) + self.dx
        y = (-(x0 - self.dx)*s + (y0 - self.dy)*c) + self.dy
        self.canvas.set_led(x, y, z, color)
