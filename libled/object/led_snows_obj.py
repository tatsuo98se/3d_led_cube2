import random
from led_object import LedObject
from ..led_cube import *

class LedSnowObject(LedObject):

    def __init__(self, lifetime = 0 ):
        super(LedSnowObject, self).__init__(lifetime)
        self.x = random.randrange(0, LED_WIDTH)
        self.z = random.randrange(0, LED_DEPTH)
        self.y = 0
        self.gravity = random.uniform(0.3, 0.5)
        self.set_timer(0.1)

    def is_expired(self, offset=0):
        if(self.y > LED_HEIGHT):
            return True
        return super(LedSnowObject, self).is_expired(offset)

    def on_timer(self):
        self.y += self.gravity

    def draw(self, canvas):
        canvas.set_led(self.x, self.y, self.z, int(0xffffff))


class LedSnowsObject(LedObject):

    def __init__(self, lifetime = 0 ):
        super(LedSnowsObject, self).__init__(lifetime)
        self.set_timer(0.1)
        self.is_need_update = False

    def on_timer(self):
        self.is_need_update = True

    def draw(self, canvas):
        if self.is_need_update:
            canvas.add_object(LedSnowObject())
            self.is_need_update = False

