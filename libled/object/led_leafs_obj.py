import random
from led_object import LedObject
from ..led_cube import *
from led_leaf_obj import LedLeafObject

class LedLeafsObject(LedObject):

    def __init__(self, color, lifetime = 0 ):
        super(LedLeafsObject, self).__init__(lifetime)
        self.color = color
        self.set_timer(1)
        self.is_need_update = False

    def on_timer(self):
        self.is_need_update = True

    def draw(self, canvas):
        if self.is_need_update:
            canvas.add_object(LedLeafObject(self.color))
            self.is_need_update = False

