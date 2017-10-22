# -*- encoding:utf8 -*-
from led_object import LedObject
from ..led_cube import *
from PIL import Image, ImageDraw, ImageFont
from ..util.color import Color


class LedTextObject(LedObject):

    def __init__(self, x=LED_WIDTH-1, y=0, z=0, text="", fontsize=26, color="#ff0000", lifetime=0):
        super(LedTextObject, self).__init__(lifetime)
        self.x = x
        self.y = y
        self.z = z
        self.color = color

        # font 2 text
        font = ImageFont.truetype("asset/font/migu-1p-regular.ttf", fontsize)
        size = font.getsize(text)
        offset = font.getoffset(text)
        self.image = Image.new(
            'RGB', (max(size[0], LED_WIDTH), max(size[1], LED_HEIGHT)))
        d = ImageDraw.Draw(self.image)
        d.text((offset[0], -offset[1]), text=text, font=font, fill=self.color)

        # moving
        self.set_timer(0.03)
        self.posx = 0

    def is_expired(self, offset=0):
        return abs(self.posx) >= self.image.size[0]

    def on_timer(self):
        self.left()

    def draw(self, canvas):
        for x in range(LED_WIDTH):
            px = x + abs(self.posx)
            for y in range(LED_HEIGHT):
                for z in range(LED_DEPTH):
                    if px < 0:
                        continue
                    if px >= self.image.size[0]:
                        continue

                    r, g, b = self.image.getpixel((px, y))
                    if r == 0 and g == 0 and b == 0:
                        continue
                    canvas.set_led(x + self.x, y + self.y, z + self.z,
                                   (r << 16) + (g << 8) + b)

        if self.x > 0:
            self.x -= 1

    def left(self):
        if self.x <= 0:
            self.posx -= 1
