from led_object_canvas_filter import LedObjectCanvasFilter
from ..object.led_leafs_obj import LedLeafsObject

class LedSakuraObjectCanvasFilter(LedObjectCanvasFilter):

    def __init__(self, canvas):
        super(LedSakuraObjectCanvasFilter, self).__init__(canvas, \
            LedLeafsObject(int(0xffcccc)))
    