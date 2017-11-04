from led_object import LedObject
from ..util import led_draw_util
from ..util.color import Color
from ..led_cube import *
from led_twinkle_star_obj import LedTwinkleStarObject
import math
import colorsys
import random

class LedShootingStarObject(LedObject):


    def __init__(self, x, y, z, lifetime = 0 ):
        super(LedShootingStarObject, self).__init__(lifetime)
        self.x = x
        self.y = y
        self.z = z
        self.set_timer(0.05)
#        self.color = self.get_star_color()
        self.color = Color.int_to_color(0xffffff)

    def on_timer(self):
        self.x -= 1
        self.y += 1

    def get_star_color(self):
        return Color.rgbtapple_to_color( colorsys.hsv_to_rgb(random.uniform(0.5, 0.8), random.uniform(0.1, 0.5), 1))

    def is_expired(self):
        return self.x < 0 or self.y < 0

    def draw(self, canvas):

        for i in range(LED_WIDTH):
            if self.x-i < 0:
                break

            canvas.set_led(self.x + i, self.y - i, self.z, self.color/(i+1))



