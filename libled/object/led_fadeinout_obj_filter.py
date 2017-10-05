from led_object_filter import LedObjectFilter
from ..filter.led_fadeinout_canvas_filter import LedFadeinoutCanvasFilter

class LedFadeinoutOjbectFilter(LedObjectFilter):

    def __init__(self, obj):
        super(LedFadeinoutOjbectFilter, self).__init__(obj)

    def draw(self, canvas):
        new_canvas = LedFadeinoutCanvasFilter(canvas, self)
        return self.obj.draw(new_canvas)

