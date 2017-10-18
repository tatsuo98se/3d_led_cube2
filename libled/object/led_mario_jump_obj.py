from led_object import LedObject
from led_bitmap_obj import LedBitmapObject

MARGIN_Y = -15
UP = 0
DOWN = 1


class LedMarioJumpObject(LedObject):

    def __init__(self, y, z, lifetime=0):
        super(LedMarioJumpObject, self).__init__(lifetime)
        self.marioj = LedBitmapObject('asset/image/s_mario_jump.png', 0, 0, z, lifetime)
        self.direction = UP

    def draw(self, canvas):

        if self.marioj.y <= MARGIN_Y:
            self.direction = DOWN
        elif self.marioj.y >= 0:
            self.direction = UP

        if self.direction == UP:
            self.marioj.y -= 1
        elif self.direction == DOWN:
            self.marioj.y += 1

        self.marioj.draw(canvas)
