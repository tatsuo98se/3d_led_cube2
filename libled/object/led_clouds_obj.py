import random
from led_object import LedObject
from ..led_cube import *
from led_cloud_obj import LedCloudObject
import random

class LedCloudsObject(LedObject):

    def __init__(self, lifetime = 0 ):
        super(LedCloudsObject, self).__init__(lifetime)
        self.set_timer(0.3)
        self.is_need_update = False

    def on_timer(self): 
        self.is_need_update = True if random.randint(0, 3) == 0 else False

    def draw(self, canvas):
        if self.is_need_update:
            canvas.add_object(LedCloudObject())
            self.is_need_update = False

