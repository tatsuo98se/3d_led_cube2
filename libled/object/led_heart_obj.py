from led_object import LedObject
from ..led_cube import *
from led_bitmap_obj import LedBitmapObject

class LedHeartObject(LedObject):

    def __init__(self, lifetime = 0 ):
        super(LedHeartObject, self).__init__(lifetime)
        self.heart = [
            LedBitmapObject('asset/image/heart1.png', 0, 0, 0, lifetime),
            LedBitmapObject('asset/image/heart2.png', 0, 0, 1, lifetime),
            LedBitmapObject('asset/image/heart3.png', 0, 0, 2, lifetime),
            LedBitmapObject('asset/image/heart4.png', 0, 0, 3, lifetime),
            LedBitmapObject('asset/image/heart4.png', 0, 0, 4, lifetime),
            LedBitmapObject('asset/image/heart3.png', 0, 0, 5, lifetime),
            LedBitmapObject('asset/image/heart2.png', 0, 0, 6, lifetime),
            LedBitmapObject('asset/image/heart1.png', 0, 0, 7, lifetime)
        ]

    def draw(self, canvas):

        for bitmap in self.heart:
            bitmap.draw(canvas)
