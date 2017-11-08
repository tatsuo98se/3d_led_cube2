from led_canvs_filter import LedCanvasFilter
from ..led_cube import *
from ..util.color import Color
import math
import time

class LedSwayingCanvasFilter(LedCanvasFilter):

    def __init__(self, canvas):
        super(LedSwayingCanvasFilter, self).__init__(canvas)
        self.born_at = time.time()

    def set_led(self, x0, y0, z, color):
        swaying = math.cos((time.time() - self.born_at) * 4) * 0.03
        T = 4
        s = math.sin(swaying*3.14*T)
        c = math.cos(swaying*3.14*T)
        dx = LED_WIDTH / 2
        dy = LED_HEIGHT
        x = ((x0 - dx)*c + (y0 - dy)*s) + dx
        y = (-(x0 - dx)*s + (y0 - dy)*c) + dy
        self.canvas.set_led(x, y, z, color)
