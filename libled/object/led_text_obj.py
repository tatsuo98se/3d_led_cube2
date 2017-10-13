# -*- encoding:utf8 -*-
from led_object import LedObject
from ..led_cube import *
from PIL import Image, ImageDraw, ImageFont


class LedTextObject(LedObject):

    def __init__(self, x, y, z, text, color, lifetime = 0 ):
        super(LedTextObject, self).__init__(lifetime)
        self.x = x
        self.y = y
        self.z = z
        self.color = color
        font = ImageFont.truetype("asset/font/migu-1p-regular.ttf", 20)
        self.image = Image.new('RGB', (LED_WIDTH, LED_HEIGHT))
        d = ImageDraw.Draw(self.image)
        d.text((1, 1), text, font=font, fill=(255, 0, 0))

    def draw(self, canvas):
        for x in range(LED_WIDTH):
            for y in range(LED_HEIGHT):
                r,g,b = self.image.getpixel((x,y))
                if r == 0 and g == 0 and b == 0:
                    continue
                canvas.set_led(x + self.x, y + self.y, self.z, (r<<16)+(g<<8)+b)

