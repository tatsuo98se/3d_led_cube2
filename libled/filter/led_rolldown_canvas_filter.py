from led_canvs_filter import LedCanvasFilter
from ..led_cube import *
from ..util.cube_util import *
import time

class LedRollDownCanvasFilter(LedCanvasFilter):

    def __init__(self, canvas):
        super(LedRollDownCanvasFilter, self).__init__(canvas)
        self.offset = 0
        self.born_at = time.time()

    def pre_draw(self):
        self.offset = int(round(time.time() * 10 - self.born_at * 10))
        
    def set_led(self, x, y, z, color):
        if not is_in_cube(x, y, z):
            return
        new_y = (y + self.offset) % LED_HEIGHT

        self.canvas.set_led(x, new_y, z, color)
