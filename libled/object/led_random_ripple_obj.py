from ..led_cube import *
import random
import colorsys
from led_object import LedObject
from ..util.led_draw_util import *
from led_ripple_obj import LedRippleObject
from ..util.color import Color

class LedRandomRippleObject(LedObject):

    DISTANCE = 1.5 #sec

    def __init__(self, lifetime = 0 ):
        super(LedRandomRippleObject, self).__init__(lifetime)
        self.last_update = 0

    def draw(self, canvas):

        is_need_update = False
        if self.last_update == 0:
            self.last_update = self.elapsed()

        if self.elapsed() - self.last_update > LedRandomRippleObject.DISTANCE:
            self.last_update = self.elapsed()
            ripple = LedRippleObject(random.randint(0, LED_WIDTH-1), 
                                random.randint(0, LED_HEIGHT-1), 
                                Color.rgbtapple_to_color( colorsys.hsv_to_rgb(random.random(), 1, 1)))
            canvas.add_object(ripple)

