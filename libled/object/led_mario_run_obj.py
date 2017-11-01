from led_object import LedObject
from ..led_cube import *
from led_bitmap_obj import LedBitmapObject


class LedMarioRunObject(LedObject):

    def __init__(self, z, lifetime = 0 ):
        super(LedMarioRunObject, self).__init__(lifetime)
        self.mario1 = LedBitmapObject('asset/image/mario_run_1.png', 0, 0, z, 1, lifetime)
        self.mario2 =  LedBitmapObject('asset/image/mario_run_2.png', 0, 0, z, 1, lifetime)
        self.set_timer(0.1)
        self.mario = False

    def on_timer(self):
        self.mario = not self.mario

    def draw(self, canvas):

        if self.mario:
            self.mario1.draw(canvas)
        else:
            self.mario2.draw(canvas)
