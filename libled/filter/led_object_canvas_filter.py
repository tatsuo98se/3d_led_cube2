from led_canvs_filter import LedCanvasFilter

class LedObjectCanvasFilter(LedCanvasFilter):

    def __init__(self, canvas, obj):
        super(LedObjectCanvasFilter, self).__init__(canvas)
        self.obj = obj
    
    def pre_draw(self):
        super(LedObjectCanvasFilter, self).pre_draw()
        if self.obj is not None:
            self.obj.will_draw()
            self.obj.draw(self)

            if self.obj.is_expired():
                self.obj = None

