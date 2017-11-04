from led_object import LedObject
from ..util import led_draw_util
from ..led_cube import *
from ..util.color import Color
import math
import random
import colorsys

class LedTwinkleStarObject(LedObject):

    def __init__(self, x, y, z, size, lifetime = 0 ):
        super(LedTwinkleStarObject, self).__init__(lifetime)
        self.x = x
        self.y = y
        self.z = z
        self.size = size
        self.color = self.get_star_color()
        self.offset = random.randrange(1,4)
        self.zerocount = 0
        self.first_0 = False

    def is_expired(self):
        return self.zerocount > 4

    def get_star_color(self):
        return Color.rgbtapple_to_color( colorsys.hsv_to_rgb(random.uniform(0.5, 0.8), random.uniform(0.3, 0.8), 1))


    def draw(self, canvas):

        style = int(round((math.cos(self.elapsed() + self.offset * 4) + 1) * self.size))

        if not self.first_0:
            if style == 0:
                self.first_0 = True
            else:
                return

        if style == 0:
            self.zerocount += 1
            self.draw_star1(canvas, 
                Color(self.color.r, self.color.g, self.color.b, self.color.a/2))
        elif style == 1:
            self.draw_star1(canvas, 
                Color(self.color.r, self.color.g, self.color.b, self.color.a/2))
        elif style == 2:
            self.draw_star1(canvas, self.color)
            self.draw_star2(canvas, 
                Color(self.color.r, self.color.g, self.color.b, self.color.a/2))
        else:
            self.draw_star1(canvas, self.color)
            self.draw_star2(canvas, self.color)

    def draw_star1(self, canvas, color):
        canvas.set_led(self.x, self.y, self.z, color)

    def draw_star2(self, canvas, color):
        for offsetx, offsety, offsetz in [[-1, 0, 0],[1, 0, 0],[0, -1, 0], [0, 1, 0], [0, 0, 1], [0, 0, -1]]:
            canvas.set_led(self.x + offsetx, self.y + offsety, self.z + offsetz, color)

