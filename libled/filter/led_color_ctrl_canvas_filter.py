from led_canvs_filter import LedCanvasFilter
import math
import colorsys
from ..util.color import Color
from ..util.hw_controller_bridge import get_data_as_json
import json
import time

class LedColorCtrlCanvasFilter(LedCanvasFilter):

    def __init__(self, canvas):
        super(LedColorCtrlCanvasFilter, self).__init__(canvas)
        self.c = 0
        self.born_at = time.time()

    def get_color_from_serial(self):
        while True:
            try:
                color = get_data_as_json(defaults={'a0':0.5, 'a1':0.5, 'a2':0.5})
                return Color(color['a0'], color['a1'], color['a2'])
            except ValueError:
                return Color(0,0,0)

    def pre_draw(self):
        super(LedColorCtrlCanvasFilter, self).pre_draw()
        self.color = self.get_color_from_serial()

    def set_led(self, x, y, z, color):
        self.canvas.set_led(x, y, z, self.color)
