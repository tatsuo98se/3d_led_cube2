from led_canvs_filter import LedCanvasFilter
from ..led_cube import *
import math
import colorsys
from ..util.color import Color

class LedHsvCanvasFilter(LedCanvasFilter):

    def __init__(self, canvas):
        super(LedHsvCanvasFilter, self).__init__(canvas)

    def set_led(self, x, y, z, color):
        self.canvas.set_led(x, y, z,
                            Color.rgbtapple_to_color(colorsys.hsv_to_rgb(float(z) / LED_DEPTH, 1.0, 1.0), color.a))
