import random
from led_bitmaps_obj import LedBitmapsObject
from ..led_cube import *

class LedCloudObject(LedBitmapsObject):

    def __init__(self, lifetime = 0 ):
        super(LedCloudObject, self).__init__(
                        [
                            None,
                            'asset/image/cloud/cloud2.png',
                            'asset/image/cloud/cloud3.png',
                            'asset/image/cloud/cloud4.png',
                            'asset/image/cloud/cloud4.png',
                            'asset/image/cloud/cloud3.png',
                            'asset/image/cloud/cloud2.png',
                            None
                        ],
                        LED_WIDTH, 
                        0,
                        random.randrange(2, LED_DEPTH-2), lifetime)
        self.wind = random.uniform(1, 1.5)
        self.set_timer(0.1)

    def is_expired(self, offset=0):
        if(self.x < -LED_WIDTH):
            return True
        return super(LedCloudObject, self).is_expired(offset)

    def on_timer(self):
        self.x -= self.wind

