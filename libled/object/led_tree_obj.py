from led_object import LedObject
from led_bitmaps_obj import LedBitmapsObject
from ..filter.led_bk_snows_object_canvas_filter import LedSnowsObjectCanvasFilter
from ..filter.led_bk_sakura_object_canvas_filter import LedSakuraObjectCanvasFilter

class LedTreeObject(LedObject):

    def __init__(self, x=0, y=0, z=0, mode = None, lifetime = 0):
        super(LedTreeObject, self).__init__(lifetime)
        self.snow = mode == 's'
        self.sakura = mode == 'c'
        self.x = x
        self.y = y
        self.z = z

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
                self.x, self.y, self.z, 
                self.lifetime)
        elif canvas.has(LedSakuraObjectCanvasFilter) or self.sakura:
            bitmaps = LedBitmapsObject(\
                [
                    'asset/image/tree/c_tree1.png',
                    'asset/image/tree/c_tree2.png',
                    'asset/image/tree/c_tree3.png',
                    'asset/image/tree/c_tree4.png',
                    'asset/image/tree/c_tree4.png',
                    'asset/image/tree/c_tree3.png',
                    'asset/image/tree/c_tree2.png',
                    'asset/image/tree/c_tree1.png',
                ],
                self.x, self.y, self.z,
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
                self.x, self.y, self.z, 
                self.lifetime)
        
        bitmaps.draw(canvas)
