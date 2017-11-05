from led_bitmaps_obj import LedBitmapsObject

class LedSocksObject(LedBitmapsObject):

    def __init__(self, lifetime = 0 ):
        super(LedSocksObject, self).__init__( \
            [
                'asset/image/socks/socks1.png',
                'asset/image/socks/socks1.png',
                None,
                None,
                None,
                None,
                None,
                None,
            ],
            lifetime)
