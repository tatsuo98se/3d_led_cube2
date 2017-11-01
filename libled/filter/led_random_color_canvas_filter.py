from led_canvs_filter import LedCanvasFilter
from ..led_cube import *
import math
import colorsys
from ..util.color import Color
import random

class LedRandomColorCanvasFilter(LedCanvasFilter):

    def __init__(self, canvas):
        super(LedRandomColorCanvasFilter, self).__init__(canvas)

    def set_led(self, x, y, z, color):
        src_color = Color.object_to_color(color)
        h = random.uniform(0.0, 1.0)
        self.canvas.set_led(x, y, z,
                            Color.rgbtapple_to_color(colorsys.hsv_to_rgb(h, 1.0, 1.0), src_color.a))
