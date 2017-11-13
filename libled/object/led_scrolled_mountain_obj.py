from led_scrolled_bitmaps_obj import LedScrolledBitmapsObject
from ..filter.led_bk_snows_object_canvas_filter import LedSnowsObjectCanvasFilter
from ..led_cube import *

class LedScrolledMountainObject(LedScrolledBitmapsObject):

    def __init__(self,  mode = None, lifetime = 0 ):
        super(LedScrolledMountainObject, self).__init__(None, 0, 0, 0, [10.0]*8, lifetime)
        self.mode = mode

    def init_images(self, image_data, canvas):

        filenames = [None for i in range(LED_DEPTH)]
        if self.mode == 's' or canvas.has(LedSnowsObjectCanvasFilter):
           filenames = \
            [
                None,
                None,
                None,
                None,
                None,
                None,
                'asset/image/mountain/mountain2-s.png',
                'asset/image/mountain/mountain1-s.png',
                
            ]
        else:
            filenames = \
            [
                None,
                None,
                None,
                None,
                None,
                None,
                'asset/image/mountain/mountain2.png',
                'asset/image/mountain/mountain1.png',
            ]

        super(LedScrolledMountainObject, self).init_images(filenames, canvas)
