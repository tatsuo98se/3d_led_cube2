from led_bitmaps_obj import LedBitmapsObject

class LedHeartObject(LedBitmapsObject):

    def __init__(self, x=0, y=0, z=0, lifetime = 0 ):
        super(LedHeartObject, self).__init__( \
            [
                'asset/image/heart/heart1.png',
                'asset/image/heart/heart2.png',
                'asset/image/heart/heart3.png',
                'asset/image/heart/heart4.png',
                'asset/image/heart/heart4.png',
                'asset/image/heart/heart3.png',
                'asset/image/heart/heart2.png',
                'asset/image/heart/heart1.png',
            ],
            x, y, z, 
            lifetime)
