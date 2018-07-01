from led_canvs_filter import LedCanvasFilter
from ..led_cube import *
from ..util.color import Color
from ..util.hw_controller_util import get_data_as_json
import math
import time

class LedZSkewedCtrlCanvasFilter(LedCanvasFilter):

    def __init__(self, canvas):
        super(LedZSkewedCtrlCanvasFilter, self).__init__(canvas)
        self.t = 0
        self.last_update = time.time()

    def pre_draw(self):
        super(LedZSkewedCtrlCanvasFilter, self).pre_draw()
        param = get_data_as_json(defaults={'a0':0.2, 'a1':0.5})
        direction = (param['a0'] - 0.5)
        speed = param['a1'] / 5
        self.t += direction * speed

    def set_led(self, x0, y0, z, color):
        T = 4
        s = math.sin(self.t*3.14*T)
        c = math.cos(self.t*3.14*T)
        dx = LED_WIDTH / 2
        dy = LED_HEIGHT / 4 * 3
        x = ((x0 - dx)*c + (y0 - dy)*s) + dx
        y = (-(x0 - dx)*s + (y0 - dy)*c) + dy
        self.canvas.set_led(x, y, z, color)
