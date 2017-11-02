from led_object import LedObject
from led_bitmaps_obj import LedBitmapsObject
from ..filter.led_bk_snows_object_canvas_filter import LedSnowsObjectCanvasFilter

class LedTreeObject(LedObject):

    def __init__(self, s = False, lifetime = 0):
        super(LedTreeObject, self).__init__(lifetime)
        self.snow = s

    def draw(self, canvas):

        bitmaps = None
        if canvas.has(LedSnowsObjectCanvasFilter) or self.snow:
            bitmaps = LedBitmapsObject(\
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
                self.lifetime)
        else:
            bitmaps = LedBitmapsObject(\
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
                self.lifetime)
        
        bitmaps.draw(canvas)
