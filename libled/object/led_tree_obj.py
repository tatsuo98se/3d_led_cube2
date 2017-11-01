from led_bitmaps_obj import LedBitmapsObject

class LedTreeObject(LedBitmapsObject):

    def __init__(self, s = False, lifetime = 0):
        if s:
            super(LedTreeObject, self).__init__( \
                [
                    'asset/image/tree/s_tree1.png',
                    'asset/image/tree/s_tree2.png',
                    'asset/image/tree/s_tree3.png',
                    'asset/image/tree/s_tree4.png',
                    'asset/image/tree/s_tree5.png',
                    'asset/image/tree/s_tree3.png',
                    'asset/image/tree/s_tree2.png',
                    'asset/image/tree/s_tree1.png',
                ],
                lifetime)
        else:
            super(LedTreeObject, self).__init__( \
                [
                    'asset/image/tree/tree1.png',
                    'asset/image/tree/tree2.png',
                    'asset/image/tree/tree3.png',
                    'asset/image/tree/tree4.png',
                    'asset/image/tree/tree5.png',
                    'asset/image/tree/tree3.png',
                    'asset/image/tree/tree2.png',
                    'asset/image/tree/tree1.png',
                ],
                lifetime)
