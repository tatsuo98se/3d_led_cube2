from led_object import LedObject
from ..led_cube import *
from ..util.color import Color

class LedFillObject(LedObject):

    def __init__(self, color, lifetime = 0 ):
        super(LedFillObject, self).__init__(lifetime)
        self.color = Color.object_to_color(color)

    def draw(self, canvas):
        new_color = self.color/2
        for x in range(0, LED_WIDTH):
            for y in range(0, LED_HEIGHT):
                for z in range(0, LED_DEPTH):
                    canvas.set_led(x, y, z, new_color)
