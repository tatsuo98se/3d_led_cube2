from led_canvs_filter import LedCanvasFilter
from ..led_cube import *
from ..util.led_draw_util import *
from ..util.cube_util import *
from ..util.color import Color
import math
import numpy as np
import random

import time

class LedZoomInOutCanvasFilter(LedCanvasFilter):

    def __init__(self, canvas):
        super(LedZoomInOutCanvasFilter, self).__init__(canvas)
        self.last_update = time.time()
        self.zoomin = False
        self.scale = 1.0
        self.src = self.get_new_canvas()
        self.dst = self.get_new_canvas()

    def get_new_canvas(self):
       return np.array([[[ [[0]*4] * LED_DEPTH] * LED_HEIGHT ] * LED_WIDTH ] , dtype = np.uint8)

    def pre_draw(self):
        super(LedZoomInOutCanvasFilter, self).pre_draw()
        self.scale = math.sin(time.time()) / 2 + 1.0 

        self.src = self.get_new_canvas()
        self.dst = self.get_new_canvas()

    def set_led(self, x, y, z, color):
        ix, iy, iz = rounds(x, y, z)
        if not is_in_cube(ix, iy, iz):
            return

        self.src[0, ix, iy, iz] = Color.object_to_color(color).to_rgba255()


 
    def post_draw(self):
        super(LedZoomInOutCanvasFilter, self).post_draw()

        scale = self.scale
        for z in range(LED_DEPTH):
            src = self.src[0, :, :, z]
            np_scaled = get_scled_image(src.astype('uint8'), scale, scale)
            pos = (int(round((src.shape[0] - np_scaled.shape[0])/2.0)), src.shape[1] - np_scaled.shape[1])
            new_src = resize2(np_scaled, (LED_WIDTH, LED_HEIGHT), pos, [[0]*4])
            self.dst[0, :, :, z] = new_src

        
        for x in range(LED_WIDTH):
            src = self.dst[0, x, :, :]
            np_scaled = get_scled_image(src.astype('uint8'), scale, 1)
            pos = (src.shape[0] - np_scaled.shape[0], src.shape[1] - np_scaled.shape[1])
            dx, dy, sx, sy, w, h = get_copy_positions(np_scaled.shape, src.shape, pos)
            new_src = resize2(np_scaled, (LED_HEIGHT, LED_DEPTH), pos, [[0]*4])
            self.dst[0, x, :, :] = new_src



        for x in range(LED_WIDTH):
            for y in range(LED_HEIGHT):
                for z in range(LED_DEPTH):
                    if np.count_nonzero(self.dst[0, x, y, z]):
                        self.canvas.set_led(x, y, z, self.dst[0, x, y, z])

