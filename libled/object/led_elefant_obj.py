from led_bitmaps_obj import LedBitmapsObject

class LedElefantObject(LedBitmapsObject):

    def __init__(self, x=0, y=0, z=0, lifetime = 0 ):
        super(LedElefantObject, self).__init__( \
            [
                'asset/image/elefant/elefant1.png',
                'asset/image/elefant/elefant2.png',
                'asset/image/elefant/elefant3.png',
                'asset/image/elefant/elefant4.png',
                'asset/image/elefant/elefant3.png',
                'asset/image/elefant/elefant2.png',
                'asset/image/elefant/elefant1.png',
                None,
            ],
            x, y, z,
            lifetime)
