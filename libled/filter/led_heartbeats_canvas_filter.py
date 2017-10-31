from led_canvs_filter import LedCanvasFilter
from ..led_cube import *
from ..util.led_draw_util import *
from ..util.cube_util import *
from ..util.color import Color
import math
import numpy as np
import random

import time

class LedHeartsBeatsCanvasFilter(LedCanvasFilter):

    def __init__(self, canvas):
        super(LedHeartsBeatsCanvasFilter, self).__init__(canvas)
        self.last_update = time.time()
        self.need_update = False
        self.src = self.get_new_canvas()
        self.dst = self.get_new_canvas()

    def get_new_canvas(self):
#        return np.zeros((LED_WIDTH, LED_HEIGHT, LED_DEPTH))
#        return np.array(LED_DEPTH * LED_HEIGHT * LED_WIDTH).reshape(LED_WIDTH, LED_HEIGHT, LED_DEPTH)
       return np.array([[[ [[0]*4] * LED_DEPTH] * LED_HEIGHT ] * LED_WIDTH ] , dtype = np.uint8)

    def pre_draw(self):
        T = time.time() - self.last_update
        if T > 0.5:
            self.need_update = True
            self.last_update = time.time()
        else:
            self.need_update = False

        self.src = self.get_new_canvas()
        self.dst = self.get_new_canvas()

    def set_led(self, x, y, z, color):
        ix, iy, iz = rounds(x, y, z)
        if not is_in_cube(ix, iy, iz):
            return

        self.src[0, ix, iy, iz] = Color.object_to_color(color).to_rgba255()

    def post_draw(self):

        if self.need_update:
            scale = random.uniform(1.1 ,1.5)
            for z in range(LED_DEPTH):
                image = Image.fromarray(self.src[0, :, :, z].astype('uint8'), 'RGBA')
                nw = int(round(image.width * scale))
                nh = int(round(image.height * scale))
                scaled = image.resize((nw, nh))
                scaled = scaled.rotate(Image.ROTATE_90)
                np_scaled = np.asarray(scaled)

                sw = sh = dw = dh= dx = dy = sx = sy = 0
                if scale > 1.0:
                    sx = int(round((np_scaled.shape[0] - LED_WIDTH)/2.0))
                    sy = np_scaled.shape[1] - LED_HEIGHT
                    sw = LED_WIDTH + sx
                    sh = LED_HEIGHT + sy
                    dw = LED_WIDTH
                    dh = LED_HEIGHT
                else:
                    dx = int(round((LED_WIDTH - np_scaled.shape[0])/2.0))
                    dy = LED_HEIGHT - np_scaled.shape[1]
                    dw = np_scaled.shape[0] + dx
                    dh = np_scaled.shape[1] + dy
                    dw = np_scaled.shape[0]
                    dh = np_scaled.shape[1]
                self.dst[0,0+dx:dw, 0+dy:dh ,z] = np_scaled[0+sx:sw, 0+sy:sh]
        else:
            self.dst = self.src

        for x in range(LED_WIDTH):
            for y in range(LED_HEIGHT):
                for z in range(LED_DEPTH):
                    if np.count_nonzero(self.dst[0, x, y, z]):
                        self.canvas.set_led(x, y, z, self.dst[0, x, y, z])
