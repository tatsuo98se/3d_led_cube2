from led_bitmaps_obj import LedBitmapsObject

class LedSabotenObject(LedBitmapsObject):

    def __init__(self, x=0, y=0, z=0, lifetime = 0 ):
        super(LedSabotenObject, self).__init__( \
            [
                'asset/image/saboten/saboten0.png',
                'asset/image/saboten/saboten1.png',
                'asset/image/saboten/saboten2.png',
                'asset/image/saboten/saboten3.png',
                'asset/image/saboten/saboten3.png',
                'asset/image/saboten/saboten2.png',
                'asset/image/saboten/saboten1.png',
                'asset/image/saboten/saboten0.png',
            ],
            x, y, z, 
            lifetime)
