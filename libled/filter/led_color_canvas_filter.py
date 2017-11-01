from led_canvs_filter import LedCanvasFilter
from ..led_cube import *
import math
import colorsys
from ..util.color import Color

class LedColorCanvasFilter(LedCanvasFilter):

    def __init__(self, canvas, color):
        super(LedColorCanvasFilter, self).__init__(canvas)
        self.color = color

    def set_led(self, x, y, z, color):
        self.canvas.set_led(x, y, z, self.color)
