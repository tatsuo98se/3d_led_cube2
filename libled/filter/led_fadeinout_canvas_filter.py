from led_canvs_filter import LedCanvasFilter
from ..led_cube import *
import math
import colorsys
from ..util.color import Color

#FADE_RATIO = 0.08

class LedFadeinoutCanvasFilter(LedCanvasFilter):

    def __init__(self, canvas, obj):
        super(LedFadeinoutCanvasFilter, self).__init__(canvas)
        self.obj = obj

    def set_led(self, x, y, z, color):
        if self.obj.lifetime == 0:
            self.canvas.set_led(x, y, z, color)
            
        new_color = Color.object_to_color(color)
#        margin = self.obj.lifetime * FADE_RATIO
        margin = 1.5
        if self.obj.elapsed() < margin:
            new_color.a = self.obj.elapsed() / margin
        else:
            new_color.a = (self.obj.elapsed() - self.obj.lifetime + margin )/ -margin

        new_color.a = min(max(new_color.a, 0), 1)

        self.canvas.set_led(x, y, z, new_color)
