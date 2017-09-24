from led_object import LedObject
from ..led_cube import *

class LedFillObject(LedObject):

    def __init__(self, color, lifetime = 0 ):
        super(LedFillObject, self).__init__(lifetime)
        self.color = color

    def draw(self, canvas):
        for i in range(0, LED_WIDTH):
            for j in range(0, LED_HEIGHT):
                canvas.set_led(i, j, 0, self.color)
