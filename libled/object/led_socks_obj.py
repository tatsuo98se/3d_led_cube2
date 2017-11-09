from led_object import LedObject
from led_bitmap_obj import LedBitmapObject
from ..filter.led_skewed_canvas_filter import LedSkewedCanvasFilter
from ..filter.led_zoom_in_out_canvas_filter import LedZoomInOutCanvasFilter
from ..filter.led_spiral_canvas_filter import LedSpiralCanvasFilter

class LedSocksObject(LedObject):

    def __init__(self, lifetime = 0 ):
        super(LedSocksObject, self).__init__(lifetime)

    def draw(self, canvas):
        bitmap = None
        filter_for_back = [LedSkewedCanvasFilter, LedZoomInOutCanvasFilter, LedSpiralCanvasFilter]
        if canvas.has(filter_for_back):
            bitmap = LedBitmapObject(\
                    'asset/image/socks/socks1.png', 0, 0, 3, 2, self.lifetime) 
        else:
            bitmap = LedBitmapObject(\
                    'asset/image/socks/socks1.png', 0, 0, 0, 2, self.lifetime) 
        
        bitmap.draw(canvas)