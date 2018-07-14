from led_bitmaps_obj import LedBitmapsObject

class LedTulipObject(LedBitmapsObject):

    def __init__(self, x=0, y=0, z=0, lifetime = 0 ):
        super(LedTulipObject, self).__init__( \
            [
                None,
                'asset/image/tulip/tulip1.png',
                'asset/image/tulip/tulip2.png',
                'asset/image/tulip/tulip3.png',
                'asset/image/tulip/tulip3.png',
                'asset/image/tulip/tulip4.png',
                'asset/image/tulip/tulip5.png',
                None,
            ],
            x, y, z, 
            lifetime)
