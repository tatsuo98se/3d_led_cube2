from led_object import LedObject
from PIL import Image
from ..led_cube import *
from led_bitmap_obj import LedBitmapObject


class LedMarioRunObject(LedObject):

    def __init__(self, z, lifetime = 0 ):
        super(LedMarioRunObject, self).__init__(lifetime)
        self.mario1 = LedBitmapObject(Image.open('asset/image/s_mario_run_1.png'), 0, 0, z, lifetime)
        self.mario2 =  LedBitmapObject(Image.open('asset/image/s_mario_run_2.png'), 0, 0, z, lifetime)
        self.set_timer(0.1)
        self.mario = False

    def on_timer(self):
        self.mario = not self.mario

    def draw(self, canvas):

        if self.mario:
            self.mario1.draw(canvas)
        else:
            self.mario2.draw(canvas)
