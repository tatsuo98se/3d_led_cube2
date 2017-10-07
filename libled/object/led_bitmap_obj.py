from led_object import LedObject
from PIL import Image
from ..led_cube import *


class LedBitmapObject(LedObject):

    def __init__(self, image, x = 0, y = 0, z= 0, lifetime = 0 ):
        super(LedBitmapObject, self).__init__(lifetime)
        self.image = image.convert('RGB')
        self.x = x
        self.y = y
        self.z = z

    def draw(self, canvas):

        size = self.image.size

        X = min(size[0], LED_WIDTH)
        Y = min(size[1], LED_HEIGHT)

        for x in range(X):
            for y in range(Y):
                r,g,b = self.image.getpixel((x,y))
                if r == 0 and g == 0 and b == 0:
                    continue
                canvas.set_led(x + self.x, y + self.y, self.z, (r<<16)+(g<<8)+b)
