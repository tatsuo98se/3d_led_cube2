from led_bitmaps_obj import LedBitmapsObject

class LedSnowmanObject(LedBitmapsObject):

    def __init__(self, x=0, y=0, z=0, lifetime = 0 ):
        super(LedSnowmanObject, self).__init__( \
            [
                'asset/image/snowman/snowman1.png',
                'asset/image/snowman/snowman2.png',
                'asset/image/snowman/snowman3.png',
                'asset/image/snowman/snowman3.png',
                'asset/image/snowman/snowman3.png',
                'asset/image/snowman/snowman3.png',
                'asset/image/snowman/snowman4.png',
                'asset/image/snowman/snowman5.png',
            ],
            x, y, z, 
            lifetime)
