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
        self.set_timer(LedRandomRippleObject.DISTANCE)
        self.is_need_update = False
    
    def on_timer(self):
        self.is_need_update = True

    def draw(self, canvas):

        if self.is_need_update:
            ripple = LedRippleObject(random.randint(0, LED_WIDTH-1), 
                                random.randint(0, LED_HEIGHT-1), 
                                Color.rgbtapple_to_color( colorsys.hsv_to_rgb(random.random(), 1, 1)))
            canvas.add_object(ripple)
            self.is_need_update = False

