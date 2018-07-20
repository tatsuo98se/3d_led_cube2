from led_object import LedObject
from led_bitmaps_obj import LedBitmapsObject
from ..filter.led_explosion_canvas_filter import LedExplosionCanvasFilter


class LedStickmanObject(LedObject):

    def __init__(self, x=0, y=0, z=0, lifetime = 0):
        super(LedStickmanObject, self).__init__(lifetime)
        self.x = x
        self.y = y
        self.z = z

    def draw(self, canvas):

        bitmaps = None
        if canvas.has(LedExplosionCanvasFilter):
            bitmaps = LedBitmapsObject(\
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
                self.x, self.y, self.z, 
                self.lifetime)
        else:
            bitmaps = LedBitmapsObject(\
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
                self.x, self.y, self.z,
                self.lifetime)

        
        bitmaps.draw(canvas)
