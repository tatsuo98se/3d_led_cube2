import random
from led_object import LedObject
from ..led_cube import *
from ..util.realsense_manager import RealsenseManager
import colorsys
from ..util.color import Color
import numpy as np

class LedRealsenseObject(LedObject):

    def __init__(self, lifetime = 0 ):
        super(LedRealsenseObject, self).__init__(lifetime)

    def draw(self, canvas):
        d = RealsenseManager.get_data()
        if d is None:
            return
        td = d[:,:,0]
        ranges = [16, 32, 48, 64, 80, 96, 112, 128]
        for z in range(LED_DEPTH):
            target = np.where( (1 < td) & (td < ranges[z]), Color(1,1,1), Color(0,0,0))
            for x in range(LED_WIDTH):
                for y in range(LED_HEIGHT):

#                    color = Color.rgbtapple_to_color(colorsys.hsv_to_rgb(np.average(d[x][y]), 1.0, 1.0))
#                    color = Color.rgbtapple255_to_color(d[x][y])
#                    canvas.set_led(x, y, 0, color)
                     canvas.set_led(x, y, z, target[x][y])

