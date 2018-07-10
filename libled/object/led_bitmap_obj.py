from led_object import LedObject
from PIL import Image
from ..led_cube import *


class LedBitmapObject(LedObject):

    def __init__(self, image_data, x = 0, y = 0, z= 0, thick = 1, lifetime = 0):
        super(LedBitmapObject, self).__init__(lifetime)
        with Image.open(image_data) as image_raw:
            self.image = image_raw.convert('RGB')
        self.x = x
        self.y = y
        self.z = z
        self.thick = thick
        self.size = self.image.size
        self.X = self.size[0]
        self.Y = self.size[1]
        self.cache = [[0 for _ in range(self.Y)] for _ in range(self.X)]

        for x in range(self.X):
            for y in range(self.Y):
                self.cache[x][y] = self.image.getpixel((x,y))


    def draw(self, canvas):

        for x in range(self.X):
            for y in range(self.Y):
                for z in range(self.thick):
                    r,g,b = self.cache[x][y]
                    if r == 0 and g == 0 and b == 0:
                        continue
                    canvas.set_led(x + self.x, y + self.y, self.z + z, (r<<16)+(g<<8)+b)

    def did_detach(self):
        self.image.close()