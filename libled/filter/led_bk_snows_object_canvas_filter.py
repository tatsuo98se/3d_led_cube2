from led_object_canvas_filter import LedObjectCanvasFilter
from ..object.led_snows_obj import LedSnowsObject

class LedSnowsObjectCanvasFilter(LedObjectCanvasFilter):

    def __init__(self, canvas):
        super(LedSnowsObjectCanvasFilter, self).__init__(canvas, LedSnowsObject())
    