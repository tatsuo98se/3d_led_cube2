from led_bitmaps_obj import LedBitmapsObject
from ..led_cube import *

class LedGhostObject(LedBitmapsObject):

    def __init__(self, mode = None, lifetime = 0 ):
        super(LedGhostObject, self).__init__(None, lifetime)

        filenames = [None for i in range(LED_DEPTH)]

        if mode == 'n':
            filenames[0] = 'asset/image/ghost/n_ghost1.png'
        elif mode == 's':
            filenames[0] = 'asset/image/ghost/s_ghost1.png'
        else:
            filenames = \
            [
                'asset/image/ghost/ghost1.png',
                'asset/image/ghost/ghost2.png',
                'asset/image/ghost/ghost3.png',
                'asset/image/ghost/ghost4.png',
                'asset/image/ghost/ghost4.png',
                'asset/image/ghost/ghost3.png',
                'asset/image/ghost/ghost2.png',
                'asset/image/ghost/ghost5.png',
            ]

        self.init_images(filenames)
