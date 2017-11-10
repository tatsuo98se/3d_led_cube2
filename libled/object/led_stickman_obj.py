from led_bitmaps_obj import LedBitmapsObject

class LedStickmanObject(LedBitmapsObject):

    def __init__(self, x=0, y=0, z=0, lifetime = 0 ):
        super(LedStickmanObject, self).__init__( \
            [
                None,
                'asset/image/stickman/stickman2.png',
                'asset/image/stickman/stickman3.png',
                'asset/image/stickman/stickman4.png',
                'asset/image/stickman/stickman4.png',
                'asset/image/stickman/stickman5.png',
                'asset/image/stickman/stickman2.png',
                None
            ],
            x, y, z, 
            lifetime)
