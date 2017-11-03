from led_bitmaps_obj import LedBitmapsObject

class LedSnowmanObject(LedBitmapsObject):

    def __init__(self, lifetime = 0 ):
        super(LedSnowmanObject, self).__init__( \
            [
                'asset/image/snowman/snowman1.png',
                'asset/image/snowman/snowman2.png',
                'asset/image/snowman/snowman3.png',
                'asset/image/snowman/snowman2.png',
                'asset/image/snowman/snowman4.png',
                None,
                None,
                None,
            ],
            lifetime)
