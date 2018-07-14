from led_object import LedObject
from ..led_cube import *
from ..util.color import Color
from ..util.paint_manager import PaintManager

class LedPaintingObject(LedObject):

    def __init__(self, lifetime = 0 ):
        super(LedPaintingObject, self).__init__(lifetime)

    def draw(self, canvas):
        for x in range(0, LED_WIDTH):
            for y in range(0, LED_HEIGHT):
                c = PaintManager.get_instance().get_color(x,y)
                if c.is_black():
                    continue
                canvas.set_led(x, y, 0, c)
