from led_object import LedObject
from ..led_cube import *

class LedOverlappedObject(LedObject):

    def __init__(self, obj):
        super(LedOverlappedObject, self).__init__()
        self.obj = obj
        self.obj_added = False

    def is_expired(self, offset = 0):
        return self.obj_added


    def draw(self, canvas):
        if self.obj_added:
            return

        self.obj_added = True
        canvas.add_object(self.obj)

