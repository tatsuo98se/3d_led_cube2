from led_canvs_filter import LedCanvasFilter
from ..led_cube import *
from ..util.color import Color
from ..util.cube_util import *
from ..util.common_util import *
import math
import time
import numpy as np
import colorsys

class Led3DZanzoCanvasFilter(LedCanvasFilter):

    def __init__(self, canvas):
        super(Led3DZanzoCanvasFilter, self).__init__(canvas)
        self.t = 0
        self.buffer = None
        self.q = []
        for _ in range(LED_DEPTH):
            self.q.append(self.get_new_canvas())

    def get_new_canvas(self):
        return create_nested_dict(2)

    def pre_draw(self):
        super(Led3DZanzoCanvasFilter, self).pre_draw()
        self.buffer = create_nested_dict(3)

    def show(self, canvas = None):
        self.t += 0.3
        super(Led3DZanzoCanvasFilter, self).show(canvas)

    def set_led(self, xx, yy, zz, color):
        if not is_in_cube(xx, yy, zz):
            return

        x = int(round(xx))
        y = int(round(yy))
        z = int(round(zz))

        if z < LED_DEPTH - 1:
            self.q[z+1][x][y] = True
        self.buffer[x][y][z] = color


    def post_draw(self):
        super(Led3DZanzoCanvasFilter, self).post_draw()

        for x in range(LED_WIDTH):
            for y in range(LED_HEIGHT):
                for z in range(LED_DEPTH):
                    if self.q[z][x][y] is True:
                        h = (math.sin(self.t-z) + 1) /2
                        self.canvas.set_led(x, y, z, 
                            Color.rgbtapple_to_color(colorsys.hsv_to_rgb(h, 1.0, 1.0)))
                        self.canvas.set_led(x, y, z, self.buffer[x][y][z])

        self.q.insert(0, self.get_new_canvas())


