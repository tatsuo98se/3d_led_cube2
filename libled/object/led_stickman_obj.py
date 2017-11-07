from led_bitmaps_obj import LedBitmapsObject

class LedStickmanObject(LedBitmapsObject):

    def __init__(self, lifetime = 0 ):
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
            lifetime)
