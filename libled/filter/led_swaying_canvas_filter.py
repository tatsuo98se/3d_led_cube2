from led_canvs_filter import LedCanvasFilter
from ..led_cube import *
from ..util.color import Color
import math
import time
from ..util.sound_interface import SoundInterface


class LedSwayingCanvasFilter(LedCanvasFilter):

    def __init__(self, canvas, dx = LED_WIDTH/2, dy = LED_HEIGHT, enable_controller=False):
        super(LedSwayingCanvasFilter, self).__init__(canvas, enable_controller)
        self.born_at = time.time()
        self.dx = dx
        self.dy = dy
        self.wav = 'asset/audio/se_wind.wav'
        SoundInterface.play(wav=self.wav, loop=True)


    def set_led(self, x0, y0, z, color):
        self.param = self.get_param_from_controller({'a0': 0.15, 'a1':0.5})
        swaying = math.cos((time.time() - self.born_at) * 4) * (self.param['a0'] * 0.1)
        T = 4 * (0.5 + self.param['a1'])
        s = math.sin(swaying*3.14*T)
        c = math.cos(swaying*3.14*T)
        x = ((x0 - self.dx)*c + (y0 - self.dy)*s) + self.dx
        y = (-(x0 - self.dx)*s + (y0 - self.dy)*c) + self.dy
        self.canvas.set_led(x, y, z, color)
