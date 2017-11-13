from led_bitmaps_obj import LedBitmapsObject
from ..led_cube import *
from ..filter.led_swaying_canvas_filter import LedSwayingCanvasFilter
from ..filter.led_bk_wave_object_canvas_filter import LedWaveObjectCanvasFilter

class LedYachtObject(LedBitmapsObject):

    def __init__(self, x=0, y=0, z=0, lifetime = 0 ):
        super(LedYachtObject, self).__init__( \
            [
                'asset/image/yacht/yacht1.png',
                'asset/image/yacht/yacht2.png',
                'asset/image/yacht/yacht3.png',
                'asset/image/yacht/yacht4.png',
                'asset/image/yacht/yacht4.png',
                'asset/image/yacht/yacht3.png',
                'asset/image/yacht/yacht2.png',
                'asset/image/yacht/yacht1.png',
            ],
            x, y, z, 
            lifetime)
        self.new_canvas = None

    def draw(self, canvas):
        if self.new_canvas is None:
            if canvas.has(LedWaveObjectCanvasFilter):
                self.new_canvas = LedSwayingCanvasFilter(canvas, LED_WIDTH/2, LED_HEIGHT*0.75, 0.008)
            else:
                self.new_canvas = canvas
 
        for bitmap in self.bitmaps:
            if bitmap is not None:
                bitmap.x = self.x
                bitmap.y = self.y
                bitmap.draw(self.new_canvas)
