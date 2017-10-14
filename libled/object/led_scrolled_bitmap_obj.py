from led_object import LedObject
from PIL import Image
from ..led_cube import *


class LedScrolledBitmapObject(LedObject):

    def __init__(self, image, x = 0, y = 0, z= 0, cycle = 5.0, lifetime = 0 ):
        super(LedScrolledBitmapObject, self).__init__(lifetime)
        self.image = image.convert('RGB')
        self.x = x
        self.y = y
        self.z = z
        self.start = 0
        self.size = self.image.size
        self.set_timer(float(cycle if cycle else 5.0)/self.size[0])

    def on_timer(self):
        self.start += 1

    def get_pixel(self, image, x, y):
        return self.image.getpixel((x % self.size[0] ,y % self.size[1]))

    def draw(self, canvas):

        for x in range(LED_WIDTH):
            for y in range(LED_HEIGHT):
                r,g,b = self.get_pixel(self.image, x + self.start ,y)
                if r == 0 and g == 0 and b == 0:
                    continue
                canvas.set_led(x + self.x, y + self.y, self.z, (r<<16)+(g<<8)+b)

