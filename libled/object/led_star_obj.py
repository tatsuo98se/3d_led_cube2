from led_bitmaps_obj import LedBitmapsObject

class LedStarObject(LedBitmapsObject):

    def __init__(self, lifetime = 0 ):
        super(LedStarObject, self).__init__(
            [
                None,
                'asset/image/star/star2.png',
                'asset/image/star/star3.png',
                'asset/image/star/star4.png',
                'asset/image/star/star4.png',
                'asset/image/star/star3.png',
                'asset/image/star/star2.png',
                None
            ],
            lifetime)