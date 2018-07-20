from led_bitmaps_obj import LedBitmapsObject

class LedColorCubeObject(LedBitmapsObject):

    def __init__(self, x=0, y=0, z=0, lifetime = 0 ):
        super(LedColorCubeObject, self).__init__( \
            [
                'asset/image/cube/cube1.png',
                'asset/image/cube/cube2.png',
                'asset/image/cube/cube3.png',
                'asset/image/cube/cube3.png',
                'asset/image/cube/cube3.png',
                'asset/image/cube/cube3.png',
                'asset/image/cube/cube2.png',
                'asset/image/cube/cube1.png',
            ],
            x, y, z,
            lifetime)
