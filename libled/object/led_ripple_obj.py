from led_object import LedObject
from ..util import led_draw_util
from ..util.color import Color

class LedRippleObject(LedObject):

    FIRST_R = 2
    SIZE = 5

    def __init__(self, x, y, color, lifetime = 0 ):
        super(LedRippleObject, self).__init__(lifetime)
        self.x = x
        self.y = y
        self.color = color
        self.produced = 0
        self.ripples = [LedRippleObject.FIRST_R]
        self.is_need_update = False
        self.set_timer(0.1)


    def is_expired(self, offset=0):
        return (self.produced != 0 and len(self.ripples) == 0)

    def on_timer(self):
        self.is_need_update = True

    def draw(self, canvas):

        if min(self.ripples) - 3 >= LedRippleObject.FIRST_R and self.produced < LedRippleObject.SIZE:
            self.ripples.append(LedRippleObject.FIRST_R)
            self.produced += 1

        new_ripples = []
        for r in self.ripples:
            if r > 32:
                continue
            else:
                led_draw_util.circle(canvas, self.x, self.y, 0,
                    Color(self.color.r, self.color.g, self.color.b), r)

            if self.is_need_update:
                new_ripples.append(r+1)
            else:
                new_ripples.append(r)
        
        self.ripples = new_ripples
        self.is_need_update = False