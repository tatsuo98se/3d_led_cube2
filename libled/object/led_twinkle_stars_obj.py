from ..led_cube import *
import random
import colorsys
from led_object import LedObject
from ..util.led_draw_util import *
from led_twinkle_star_obj import LedTwinkleStarObject
from led_shooting_star_obj import LedShootingStarObject
from ..util.color import Color

STAR_COUNT = 15

class LedTwinkleStartsObject(LedObject):

    def __init__(self, lifetime = 0 ):
        super(LedTwinkleStartsObject, self).__init__(lifetime)
        self.stars = []
    
    def draw(self, canvas):

        for star in self.stars:
            if star.is_expired():
                self.stars.remove(star)

        add_starcount = STAR_COUNT - len(self.stars)

        for i in range(add_starcount):
            star = LedTwinkleStarObject(
                            random.randint(0, LED_WIDTH-1), 
                            random.randint(0, LED_HEIGHT/2), 
                            random.randint(LED_DEPTH/2, LED_DEPTH-1),
                            random.randrange(0,3))

            self.stars.append(star)
            canvas.add_object(star)
        
        if random.randint(0,100) == 1:
            canvas.add_object(LedShootingStarObject(
                random.randint(0, LED_WIDTH/2), 
                random.randint(0, LED_HEIGHT/4),
                random.randint(LED_DEPTH/2, LED_DEPTH-1)
            ))

