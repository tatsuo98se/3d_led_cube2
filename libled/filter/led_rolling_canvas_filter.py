from led_canvs_filter import LedCanvasFilter
from ..led_cube import *
from ..util.cube_util import *
import time
from ..util.sound_player import SoundPlayer as sp

class LedRollingCanvasFilter(LedCanvasFilter):

    def __init__(self, canvas, down=True, enable_controller=False):
        super(LedRollingCanvasFilter, self).__init__(canvas, enable_controller)
        self.offset = 0
        self.last_update = time.time()
        self.direction_value = 0.6 if down else 0.4
        self.wav_d = 'asset/audio/se_rolldown.wav'
        self.wav_u = 'asset/audio/se_rollup.wav'
        self.last_count = 0

    def pre_draw(self):
        super(LedRollingCanvasFilter, self).pre_draw()
        param = self.get_param_from_controller(defaults={'a0':self.direction_value, 'a1':0.5})
        direction = (param['a0'] - 0.5) * 2
        speed = param['a1'] * 200

        now = time.time()
        add = now - self.last_update
        self.last_update = now
        self.offset += add * direction * speed

        count = int(self.offset) // LED_HEIGHT
        if count > self.last_count:
            self.last_count = count
            if param['a0']  > 0.5:
                sp.instance().do_play(self.wav_d)
            else:
                sp.instance().do_play(self.wav_u)
        
    def set_led(self, x, y, z, color):
        new_y = (y + self.offset) % LED_HEIGHT

        self.canvas.set_led(x, new_y, z, color)
