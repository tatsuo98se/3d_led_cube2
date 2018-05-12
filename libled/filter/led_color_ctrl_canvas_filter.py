from led_canvs_filter import LedCanvasFilter
from ..led_cube import *
import math
import colorsys
from ..util.color import Color
from ..util.serial_manager import SerialManager
import json

class LedColorCtrlCanvasFilter(LedCanvasFilter):

    def __init__(self, canvas):
        super(LedColorCtrlCanvasFilter, self).__init__(canvas)
        self.ser = SerialManager.get_serial_handle()

    def get_color_from_serial(self, ser):
        while True:
            try:
                line = SerialManager.get_data()
                color = json.loads(line)
                print(line)
                return Color(color['r'], color['g'], color['b'])
            except ValueError:
                print('value error retry')
                continue

    def pre_draw(self):
        super(LedColorCtrlCanvasFilter, self).pre_draw()
        self.color = self.get_color_from_serial(self.ser)

    def set_led(self, x, y, z, color):
        self.canvas.set_led(x, y, z, self.color)
