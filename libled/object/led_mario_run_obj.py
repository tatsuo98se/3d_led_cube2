from led_object import LedObject
from PIL import Image
from ..led_cube import *
from led_bitmap_obj import LedBitmapObject


class LedMarioRunObject(LedObject):

    def __init__(self, z, lifetime = 0 ):
        super(LedMarioRunObject, self).__init__(lifetime)
        self.mario1 = LedBitmapObject(Image.open('contents/s_mario_run_1.png'), 0, lifetime)
        self.mario2 =  LedBitmapObject(Image.open('contents/s_mario_run_2.png'), 0, lifetime)
        self.last_update = 0.0
        self.mario = False

    def draw(self, canvas):

        if self.last_update == 0:
            self.last_update = self.elapsed()
            
        if self.elapsed() - self.last_update > 0.1:
            self.last_update = self.elapsed()
            self.mario = not self.mario


        if self.mario:
            self.mario1.draw(canvas)
        else:
            self.mario2.draw(canvas)
