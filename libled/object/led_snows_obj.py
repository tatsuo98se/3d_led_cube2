import random
from led_object import LedObject
from ..led_cube import *
from led_snow_obj import LedSnowObject

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

