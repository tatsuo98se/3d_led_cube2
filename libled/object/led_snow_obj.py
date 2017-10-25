import random
from led_object import LedObject
from ..led_cube import *

class LedSnowObject(LedObject):

    def __init__(self, lifetime = 0 ):
        super(LedSnowObject, self).__init__(lifetime)
        self.x = random.randrange(0, LED_WIDTH)
        self.z = random.randrange(0, LED_DEPTH)
        self.y = 0
        self.gravity = random.uniform(0.5, 2)
        self.set_timer(0.1)

    def is_expired(self, offset=0):
        if(self.y > LED_HEIGHT):
            return True
        return super(LedSnowObject, self).is_expired(offset)

    def on_timer(self):
        self.y += self.gravity

    def draw(self, canvas):
        canvas.set_led(self.x, self.y, self.z, int(0xffffff))