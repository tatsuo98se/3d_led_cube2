import random
from led_object import LedObject
from ..led_cube import *
from ..util.color import Color
import math

DOWN_SPEED_START = -1
DOWN_SPEED_END = 0.1
SLIDE_SPEED_START = 0

class LedLeafObject(LedObject):

    def __init__(self, color, lifetime = 0 ):
        super(LedLeafObject, self).__init__(lifetime)
        self.color = color
        self.x = random.randrange(0, LED_WIDTH)
        self.z = random.randrange(0, LED_DEPTH)
        self.y = 0
        self.down_speed = DOWN_SPEED_START
        self.gravity = random.uniform(0.2, 0.6)
        self.slide_speed = SLIDE_SPEED_START
        self.wind = random.uniform(1, 1.5)
        self.yoffset = self.y
        self.xoffset = self.x
        self.xdirection = True
        self.set_timer(0.1)
        self.lastdot = None

    def is_expired(self, offset=0):
        if(self.y > LED_HEIGHT):
            return True
        return super(LedLeafObject, self).is_expired(offset)

    def on_timer(self):
        self.y = self.down_speed ** 2 + DOWN_SPEED_START ** 2 + self.yoffset
        move = math.sqrt(self.slide_speed)
        if not self.xdirection:
            move = -move
        self.x = move + self.xoffset

        if(self.down_speed > DOWN_SPEED_END):
            self.down_speed = DOWN_SPEED_START
            self.yoffset = self.y
            self.slide_speed = SLIDE_SPEED_START
            self.xoffset = self.x
            self.xdirection = not self.xdirection
        else:
            self.down_speed += self.gravity
            self.slide_speed += self.wind


    def draw(self, canvas):
        if self.lastdot is not None:
            canvas.set_led(self.lastdot[0], self.lastdot[1], self.lastdot[2], self.lastdot[3]/2)            
        self.lastdot = [self.x, self.y, self.z, Color.object_to_color(self.color)]
        canvas.set_led(self.x, self.y, self.z, self.color)