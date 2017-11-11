from led_object import LedObject
from ..led_cube import *
from led_scrolled_bitmap_obj import LedScrolledBitmapObject

class LedScrolledBitmapsObject(LedObject):

    def __init__(self, image_datas, x = 0, y = 0, z= 0, cycles = [5.0]*LED_DEPTH, lifetime = 0):
        super(LedScrolledBitmapsObject, self).__init__(lifetime)
        self.add = [0] * LED_DEPTH
        self.x = x
        self.y = y
        self.z = z
        self.cycles = cycles
        self.scrooled_bitmaps = []
        self.set_timer(0.1)
        self.image_datas = image_datas
        self.is_init = False

    def on_timer(self):
        for i in range(LED_DEPTH):
            if self.scrooled_bitmaps[i] is not None:
                self.scrooled_bitmaps[i].start += self.add[i]

    def init_images(self, image_datas, canvas=None):

        if not isinstance(image_datas, list):
            return
        if len(image_datas) < LED_DEPTH:
            return
        if self.is_init:
            return

        self.scrooled_bitmaps = []
        for i in range(LED_DEPTH):
            if image_datas[i] is None:
                self.scrooled_bitmaps.append(None)
            else:
                bitmap = LedScrolledBitmapObject(image_datas[i], self.x, self.y, i+self.z, self.cycles[i], self.lifetime)
                self.scrooled_bitmaps.append(bitmap)
                self.add[i] = 0.1 / (float(self.cycles[i] if self.cycles[i] else 5.0)/bitmap.size[0])
                self.is_init = True

    def draw(self, canvas):
        self.init_images(self.image_datas, canvas)
        for bitmap in self.scrooled_bitmaps:
            if bitmap is not None:
                bitmap.draw(canvas)
