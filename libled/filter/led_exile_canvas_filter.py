from led_canvs_filter import LedCanvasFilter
from ..led_cube import *
from ..util.color import Color
from ..util.common_util import *
from ..util.cube_util import *
import math
import time
import numpy as np
import colorsys

class LedExileCanvasFilter(LedCanvasFilter):

    def __init__(self, canvas):
        super(LedExileCanvasFilter, self).__init__(canvas)
        self.t = 0
        self.src = self.get_new_canvas()

    def get_new_canvas(self):
        return create_nested_dict(2)

    def pre_draw(self):
        super(LedExileCanvasFilter, self).pre_draw()
        self.src = self.get_new_canvas()

    def show(self, canvas = None):
        self.t += 0.3
        super(LedExileCanvasFilter, self).show(canvas)

    def set_led(self, xx, yy, z, color):

        c = Color.object_to_color(color)
        if c.is_black():
            return

        x = int(round(xx))
        y = int(round(yy))

        if self.src[x][y] is None:
            self.src[x][y] = c
        else:
            self.src[x][y] = self.src[x][y] | c

    def post_draw(self):
        super(LedExileCanvasFilter, self).post_draw()
        step = 2
        for x in range(LED_WIDTH):
            for y in range(LED_HEIGHT):
                for z in range(LED_DEPTH):
                    if self.src[x][y] is None:
                        continue
                    p = (self.t - z/step) # layer 4
                    sx = math.sin(p) * 3
                    sy = math.cos(p) * 3
                    if z == 0 or z == 1:
                        self.canvas.set_led(x+sx, y+sy, z, self.src[x][y])
                    else:
                        h = (math.sin(self.t+z/step) + 1) /2
                        self.canvas.set_led(x+sx, y+sy, z, 
                            Color.rgbtapple_to_color(colorsys.hsv_to_rgb(h, 1.0, 1.0)))
