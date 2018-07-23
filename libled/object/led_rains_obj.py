import random
from led_object import LedObject
from ..util.color import Color
from ..led_cube import *
import colorsys
from ..util.sound_interface import SoundInterface


class LedRainObject(LedObject):

    def __init__(self, lifetime = 0 ):
        super(LedRainObject, self).__init__(lifetime)
        self.x = random.randrange(0, LED_WIDTH)
        self.z = random.randrange(0, LED_DEPTH)
        self.y = 0
        self.gravity = random.uniform(3.0, 6.0)
        self.set_timer(0.1)

    def is_expired(self, offset=0):
        if(self.y > LED_HEIGHT):
            return True
        return super(LedRainObject, self).is_expired(offset)

    def on_timer(self):
        self.y += self.gravity

    def draw(self, canvas):
        for i in range(5):
            color = colorsys.hsv_to_rgb(0.6, 1.0, 1.0/(i+1))
            canvas.set_led(self.x, self.y-i, self.z, color)

class LedRainsObject(LedObject):

    def __init__(self, lifetime = 0 ):
        super(LedRainsObject, self).__init__(lifetime)
        self.set_timer(0.05)
        self.is_need_update = False
        self.wav = 'asset/audio/se_rain.wav'
        SoundInterface.play(wav=self.wav, loop=True)

    def on_timer(self):
        self.is_need_update = True

    def draw(self, canvas):
        if self.is_need_update:
            canvas.add_object(LedRainObject())
            self.is_need_update = False

