from led_object import LedObject
from ..led_cube import *
from ..util.vectors_util import *
import random


class LedBallsObject(LedObject):

    def __init__(self, lifetime = 0 ):
        super(LedBallsObject, self).__init__(lifetime)
        self.ix = 0
        self.ps = []
        for i in range(1, 7):
            self.ps.append(
                [
                Xyz_t(0 if i & 1 else LED_WIDTH,
                0 if i & 1 else LED_HEIGHT,
                0 if i & 1 else LED_DEPTH),
                Xyz_t(),
                (0xff0000 if i & 1 else 0) + (0xff00 if i & 2 else 0) + (0xff if i & 4 else 0)
                ]
            )

    def draw(self, canvas):

        for p in self.ps:
            if not can_show(p[0]) or p[1].len() == 0:
                while True:
                    dest = Xyz_t(random.randrange(LED_WIDTH), random.randrange(LED_HEIGHT), random.randrange(LED_DEPTH))
                    dir = dest - p[0]
                    if  dir.len() != 0:
                        break

                p[1] = dir *(1.0 / dir.len()*2)

            p[0] += p[1]
            for i in range(125):
                delta = Xyz_t(i % 5 - 2, (i / 5) % 5 - 2, (i / 25) % 5 - 2)
                if delta.len() < 2.5:
                    pos = p[0] + delta
                    if can_show(pos):
                        canvas.set_led(pos.x, pos.y, pos.z, int(p[2]))
                        