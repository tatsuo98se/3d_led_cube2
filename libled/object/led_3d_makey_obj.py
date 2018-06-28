from led_bitmaps_obj import LedBitmapsObject

class Led3DMakeyObject(LedBitmapsObject):

    def __init__(self, x=0, y=0, z=0, lifetime = 0 ):
        super(Led3DMakeyObject, self).__init__( \
            [
                'asset/image/makey/makey_3d_1.png',
                'asset/image/makey/makey_3d_2.png',
                'asset/image/makey/makey_3d_3.png',
                'asset/image/makey/makey_3d_4.png',
                'asset/image/makey/makey_3d_3.png',
                'asset/image/makey/makey_3d_5.png',
                'asset/image/makey/makey_3d_6.png',
                None,
            ],
            x, y, z,
            lifetime)
