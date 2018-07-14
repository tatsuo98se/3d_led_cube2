from led_bitmaps_obj import LedBitmapsObject

class LedPenguinObject(LedBitmapsObject):

    def __init__(self, x=0, y=0, z=0, lifetime = 0 ):
        super(LedPenguinObject, self).__init__( \
            [
                'asset/image/penguin/penguin1.png',
                'asset/image/penguin/penguin2.png',
                'asset/image/penguin/penguin3.png',
                'asset/image/penguin/penguin4.png',
                'asset/image/penguin/penguin4.png',
                'asset/image/penguin/penguin4.png',
                'asset/image/penguin/penguin5.png',
                'asset/image/penguin/penguin6.png',
            ],
            x, y, z, 
            lifetime)
