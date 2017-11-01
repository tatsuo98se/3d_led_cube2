from led_canvs_filter import LedCanvasFilter
from ..led_cube import *
import math
import colorsys
from ..util.color import Color
import time

SPEED = 8 # speed of moving color gradient
GRAD = 7.0 # small -> steep, large -> low  color gradient
class LedRainbowCanvasFilter(LedCanvasFilter):

    def __init__(self, canvas):
        super(LedRainbowCanvasFilter, self).__init__(canvas)
        self.born_at = time.time()

    def set_led(self, x, y, z, color):
        src_color = Color.object_to_color(color)
        c = ((self.born_at - time.time()) * SPEED + x + z + y/2) / GRAD
        h = (math.sin(c) + 1) /2
        self.canvas.set_led(x, y, z,
                            Color.rgbtapple_to_color(colorsys.hsv_to_rgb(h, 1.0, 1.0), src_color.a))
