from led_bitmaps_obj import LedBitmapsObject

class LedYachtObject(LedBitmapsObject):

    def __init__(self, lifetime = 0 ):
        super(LedYachtObject, self).__init__( \
            [
                'asset/image/yacht/yacht1.png',
                'asset/image/yacht/yacht2.png',
                'asset/image/yacht/yacht3.png',
                'asset/image/yacht/yacht4.png',
                'asset/image/yacht/yacht4.png',
                'asset/image/yacht/yacht3.png',
                'asset/image/yacht/yacht2.png',
                'asset/image/yacht/yacht1.png',
            ],
            lifetime)
