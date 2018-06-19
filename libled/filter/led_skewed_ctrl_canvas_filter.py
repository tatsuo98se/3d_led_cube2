from led_canvs_filter import LedCanvasFilter
from ..led_cube import *
from ..util.color import Color
from ..util.serial_manager import SerialManager
import math
import time

class LedSkewedCtrlCanvasFilter(LedCanvasFilter):

    def __init__(self, canvas):
        super(LedSkewedCtrlCanvasFilter, self).__init__(canvas)
        self.t = 0
        self.last_update = time.time()

    def pre_draw(self):
        super(LedSkewedCtrlCanvasFilter, self).pre_draw()
        param = SerialManager.get_data_as_json(defaults={'a0':0.5, 'a1':0.5})
        direction = (param['a0'] - 0.5)
        speed = param['a1'] / 5
        self.t += direction * speed

    def set_led(self, x0, y, z0, color):
        T = 4
        s = math.sin(self.t*3.14*T)
        c = math.cos(self.t*3.14*T)
        dx = LED_WIDTH / 2
        dz = LED_DEPTH / 2
        x = ((x0 - dx)*c + (z0 - dz)*s) + dx
        z = (-(x0 - dx)*s + (z0 - dz)*c) + dz
        self.canvas.set_led(x, y, z, color)
