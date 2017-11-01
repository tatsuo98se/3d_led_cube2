import time
import math
from led_object import LedObject
from ..led_cube import *

WAVE_DEPTH = 0.9

class LedWaveObject(LedObject):

    def __init__(self, yrange, color, lifetime = 0 ):
        super(LedWaveObject, self).__init__(lifetime)
        self.yrange = yrange
        self.color = color


    def draw(self, canvas):
        zwavelength = 2 * math.pi
        zwavedepth = WAVE_DEPTH
        zdot = zwavelength / LED_DEPTH
        zstart = (self.elapsed() * 2) * zdot

        xwavelength = 3 * math.pi
        xwavedepth = WAVE_DEPTH
        xdot = xwavelength / LED_WIDTH
        xstart = (self.elapsed() * 2) * xdot

        for x in range(LED_WIDTH):
            for y in self.yrange:
                for z in range(LED_DEPTH):
                  y0 = y + (xwavedepth + math.sin(xdot * x + xstart) * xwavedepth) + (zwavedepth + math.sin(zdot * z + zstart) * zwavedepth)
                  canvas.set_led(x, y0, z, self.color)


        