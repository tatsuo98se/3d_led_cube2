from led_object import LedObject
from ..led_cube import *
from led_bitmap_obj import LedBitmapObject

class LedBitmapsObject(LedObject):

    def __init__(self, filenames, lifetime = 0 ):
        super(LedBitmapsObject, self).__init__(lifetime)
        self.bitmaps = []
        for i in range(LED_DEPTH):
            if filenames[i] is None:
                self.bitmaps.append(None)
            else:
                self.bitmaps.append(LedBitmapObject(filenames[i], 0, 0, i, lifetime))

    def draw(self, canvas):
        for bitmap in self.bitmaps:
            if bitmap is not None:
                bitmap.draw(canvas)
