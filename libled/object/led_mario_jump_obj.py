from led_object import LedObject
from PIL import Image
from led_bitmap_obj import LedBitmapObject

MARGIN_Y = 15
UP = 0
DOWN = 1


class LedMarioJumpObject(LedObject):

    def __init__(self, z, y, lifetime=0):
        super(LedMarioJumpObject, self).__init__(lifetime)
        self.marioj = LedBitmapObject(Image.open(
            'asset/image/s_mario_jump.png'), z, lifetime)
        self.y = MARGIN_Y - y if y < 0 else MARGIN_Y if y > MARGIN_Y else 0
        self.direction = UP

    def draw(self, canvas):

        if self.y >= MARGIN_Y:
            self.direction = UP
        elif self.y <= 0:
            self.direction = DOWN

        if self.direction == UP:
            self.y -= 1
        elif self.direction == DOWN:
            self.y += 1

        self.marioj.start_y = self.y
        self.marioj.draw(canvas)
