from led_bitmaps_obj import LedBitmapsObject

class LedRocketObject(LedBitmapsObject):

    def __init__(self, x=0, y=0, z=0, lifetime = 0 ):
        super(LedRocketObject, self).__init__( \
            [
                'asset/image/rocket/rocket1.png',
                'asset/image/rocket/rocket2.png',
                'asset/image/rocket/rocket3.png',
                'asset/image/rocket/rocket4.png',
                'asset/image/rocket/rocket4.png',
                'asset/image/rocket/rocket3.png',
                'asset/image/rocket/rocket2.png',
                'asset/image/rocket/rocket1.png',
            ],
            x, y, z,
            lifetime)
