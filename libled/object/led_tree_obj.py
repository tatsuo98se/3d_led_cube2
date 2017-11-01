from led_bitmaps_obj import LedBitmapsObject

class LedTreeObject(LedBitmapsObject):

    def __init__(self, lifetime = 0 ):
        super(LedTreeObject, self).__init__( \
            [
                'asset/image/tree/tree1.png',
                'asset/image/tree/tree2.png',
                'asset/image/tree/tree3.png',
                'asset/image/tree/tree4.png',
                'asset/image/tree/tree3.png',
                'asset/image/tree/tree2.png',
                'asset/image/tree/tree1.png',
                None,
            ],
            lifetime)
