from led_object_canvas_filter import LedObjectCanvasFilter
from ..object.led_wave_obj import LedWaveObject

class LedWaveObjectCanvasFilter(LedObjectCanvasFilter):

    def __init__(self, canvas):
        super(LedWaveObjectCanvasFilter, self).__init__(canvas, LedWaveObject(range(28, 50), int(0x0000ff)))
    