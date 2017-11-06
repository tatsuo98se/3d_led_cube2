from led_bitmaps_obj import LedBitmapsObject

class LedElefantObject(LedBitmapsObject):

    def __init__(self, lifetime = 0 ):
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
            lifetime)
