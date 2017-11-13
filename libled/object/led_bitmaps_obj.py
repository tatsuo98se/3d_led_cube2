from led_object import LedObject
from ..led_cube import *
from led_bitmap_obj import LedBitmapObject

class LedBitmapsObject(LedObject):

    def __init__(self, filenames, x=0, y=0, z=0, lifetime = 0 ):
        super(LedBitmapsObject, self).__init__(lifetime)
        self.x = x
        self.y = y
        self.z = z
        self.bitmaps = []
        self.init_images(filenames)

    def init_images(self, filenames):
        if not isinstance(filenames, list):
            return
        if len(filenames) < LED_DEPTH:
            return

        self.bitmaps = []
        for i in range(LED_DEPTH):
            if filenames[i] is None:
                self.bitmaps.append(None)
            else:
                self.bitmaps.append(LedBitmapObject(filenames[i], self.x, self.y, i+self.z, 1, self.lifetime))

    def draw(self, canvas):
        for bitmap in self.bitmaps:
            if bitmap is not None:
                bitmap.x = self.x
                bitmap.y = self.y
                bitmap.draw(canvas)
