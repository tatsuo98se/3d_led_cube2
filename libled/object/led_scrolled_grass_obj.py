from led_scrolled_bitmaps_obj import LedScrolledBitmapsObject
from ..filter.led_bk_snows_object_canvas_filter import LedSnowsObjectCanvasFilter
from ..led_cube import *

class LedScrolledGrassObject(LedScrolledBitmapsObject):

    def __init__(self,  mode = None, lifetime = 0 ):
        super(LedScrolledGrassObject, self).__init__(None, 0, 0, 0, [2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.0], lifetime)
        self.mode = mode

    def init_images(self, image_data, canvas):

        filenames = [None for i in range(LED_DEPTH)]

        if self.mode == 's' or canvas.has(LedSnowsObjectCanvasFilter):
           filenames = \
            [
                'asset/image/grass/grass1-s.png',
                'asset/image/grass/grass2-s.png',
                'asset/image/grass/grass1-s.png',
                'asset/image/grass/grass2-s.png',
                'asset/image/grass/grass1-s.png',
                'asset/image/grass/grass3-s.png',
                None,
                None,
                
            ]
        else:
            filenames = \
            [
                'asset/image/grass/grass1.png',
                'asset/image/grass/grass2.png',
                'asset/image/grass/grass1.png',
                'asset/image/grass/grass2.png',
                'asset/image/grass/grass1.png',
                'asset/image/grass/grass3.png',
                None,
                None,
            ]

        super(LedScrolledGrassObject, self).init_images(filenames, canvas)
