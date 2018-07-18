from led_canvs_filter import LedCanvasFilter
import math
import colorsys
from ..util.color import Color
import json
import time
from ..util.sound_player import SoundPlayer as sp

SPEED = 8 # speed of moving color gradient
GRAD = 5.0 # small -> steep, large -> low  color gradient


class LedRainbowCanvasFilter(LedCanvasFilter):

    def __init__(self, canvas, enable_controller=False):
        super(LedRainbowCanvasFilter, self).__init__(canvas, enable_controller)
        self.c = 0
        self.born_at = time.time()
        self.wav = 'asset/audio/se_rainbow.wav'
        sp.instance().do_play(self.wav)

    def get_color_from_serial(self):
        color = self.get_param_from_controller(defaults={'a0':0.6, 'a1':0.0, 'a2':0.0})
        return Color(color['a0'], color['a1'], color['a2'])

    def pre_draw(self):
        super(LedRainbowCanvasFilter, self).pre_draw()
        self.color = self.get_color_from_serial()
        p = 8
        self.c += ((p//2) - self.color.r * p)

    def set_led(self, x, y, z, color):
#        self.canvas.set_led(x, y, z, self.color)

        speed, g, b = self.color.r, self.color.g, self.color.b

        src_color = Color.object_to_color(color)
#        c = (speed * 8 + x + z + y ) / GRAD
        d = (g-0.5)*2
        e = (b-0.5)*2
        c = (self.c + x * d + z + y * e ) / GRAD
#        c = ((self.born_at - time.time()) * speed * 64 + x + z + y ) / GRAD
#        c = ((self.born_at - time.time()) * speed * 16 + x + z + (y * (b * 2 - 1)) ) / GRAD
#        c += (speed * 16 + x + z + (y * (b * 2 - 1)))  / GRAD
#        self.c += 300
        h = (math.sin(c) + 1) /2
        self.canvas.set_led(x, y, z,
                            Color.rgbtapple_to_color(colorsys.hsv_to_rgb(h, 1.0, 1.0), src_color.a))
