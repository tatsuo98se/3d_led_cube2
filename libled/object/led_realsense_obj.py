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
        ranges = [16, 32, 48, 64, 80, 96, 112, 128]
        for x in range(LED_WIDTH):
            for y in range(LED_HEIGHT):
                for z in range(LED_DEPTH):
                    color = d[x,y]
                    if (1 < color[3]) & (color[3] < ranges[z]):
                        canvas.set_led(x, y, z, Color.rgbtapple255_to_color((color[0],color[1],color[2])))

