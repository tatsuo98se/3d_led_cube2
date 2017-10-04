from led_canvs_filter import LedCanvasFilter
from ..led_cube import *
import time
import math

class LedFlatWaveCanvasFilter(LedCanvasFilter):

    def __init__(self, canvas):
        super(LedFlatWaveCanvasFilter, self).__init__(canvas)
        self.born_at = time.time()

    def set_led(self, x, y, z, color):
        offset = self.born_at - time.time()
        ywavelength = 3 * math.pi
        ywavedepth = 1.5
        ydot = ywavelength / LED_HEIGHT
        ystart = (offset * 10) * ydot

        xwavelength = 3 * math.pi
        xwavedepth = 1.5
        xdot = xwavelength / LED_WIDTH
        xstart = (offset * 5) * xdot

        z = (xwavedepth + math.sin(xdot * x + xstart) * xwavedepth) + (ywavedepth + math.sin(ydot * y + ystart) * ywavedepth)

        self.canvas.set_led(x, y, z, color)

