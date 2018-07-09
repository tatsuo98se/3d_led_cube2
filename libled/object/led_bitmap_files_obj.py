from led_object import LedObject
from ..led_cube import *
import os.path
from led_bitmap_obj import LedBitmapObject

class LedBitmapFilesObject(LedObject):

    def __init__(self, prefix, x=0, y=0, z=0, lifetime = 0 ):
        super(LedBitmapFilesObject, self).__init__(lifetime)
        self.x = x
        self.y = y
        self.z = z
        self.bitmaps = []
        self.init_images(prefix)

    def init_images(self, prefix):
        self.bitmaps = []
        for i in range(LED_DEPTH):

            filename = "asset/image/{0}/{0}{1}.png".format(prefix, i)
            if not os.path.isfile(filename):
                self.bitmaps.append(None)
            else:
                self.bitmaps.append(LedBitmapObject(filename, self.x, self.y, i+self.z, 1, self.lifetime))

    def draw(self, canvas):
        for bitmap in self.bitmaps:
            if bitmap is not None:
                bitmap.x = self.x
                bitmap.y = self.y
                bitmap.draw(canvas)
