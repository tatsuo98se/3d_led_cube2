from led_canvs_filter import LedCanvasFilter
from ..led_cube import *
from ..util.color import Color
from ..util.cube_util import *
import math
import time
import numpy as np
import colorsys

class LedZanzoCanvasFilter(LedCanvasFilter):

    def __init__(self, canvas):
        super(LedZanzoCanvasFilter, self).__init__(canvas)
        self.t = 0
        self.src = None
        self.q = []

    def get_new_canvas(self):
        return [[None for height in range(LED_HEIGHT)] for width in range(LED_WIDTH)]

    def pre_draw(self):
        self.src = self.get_new_canvas()
        self.q.insert(0, self.src)

        if len(self.q) > 8:
            del self.q[-1]

    def show(self, canvas = None):
        self.t += 0.3
        super(LedZanzoCanvasFilter, self).show(canvas)

    def set_led(self, xx, yy, z, color):
        if not is_in_cube(xx, yy, z):
            return

        x = int(round(xx))
        y = int(round(yy))

        if self.src[x][y] is None:
            self.src[x][y] = Color.object_to_color(color)  
        else:
            self.src[x][y] = self.src[x][y] | Color.object_to_color(color)  

    def post_draw(self):
        step = 1
        for z in range(len(self.q)):
            s = self.q[z]
            for x in range(LED_WIDTH):
                for y in range(LED_HEIGHT):
                    if s[x][y] is None:
                        continue
                    if z == 0:
                        self.canvas.set_led(x, y, z, s[x][y])
                    else:
                        h = (math.sin(self.t+z/step) + 1) /2
                        self.canvas.set_led(x, y, z, 
                            Color.rgbtapple_to_color(colorsys.hsv_to_rgb(h, 1.0, 1.0)))
