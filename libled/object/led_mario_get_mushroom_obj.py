from led_object import LedObject
from ..led_cube import *
from led_bitmap_obj import LedBitmapObject


class LedMarioGetMushroomObject(LedObject):

    def __init__(self, z):
        super(LedMarioGetMushroomObject, self).__init__(0)
        mario = LedBitmapObject('asset/image/mario.png', 0, 0, z)
        m_mario=  LedBitmapObject('asset/image/m_mario.png', 0, 0, z)
        s_mario=  LedBitmapObject('asset/image/s_mario.png', 0, 0, z)
        self.set_timer(0.05)
        self.anime = [mario, m_mario, mario, m_mario, mario, m_mario, s_mario, mario, m_mario, s_mario, mario, s_mario, s_mario, s_mario, s_mario]
        self.index = 0
        #s(state)-s-m-s-m-s-m-l-s-m-l-s-l(state)

    def is_expired(self, offset = 0):
        return self.index >= len(self.anime)

    def on_timer(self):
        self.index += 1

    def draw(self, canvas):

        if self.index >= len(self.anime):
            return

        self.anime[self.index].draw(canvas)
