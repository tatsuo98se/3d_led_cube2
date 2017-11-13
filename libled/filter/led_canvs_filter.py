from ..i_led_canvas import ILedCanvas

class LedCanvasFilter(ILedCanvas):

    def __init__(self, canvas):
        self.canvas = canvas

    def set_led(self, x, y, z, color):
        self.canvas.set_led(x, y, z, color)

    def show(self, canvas=None):
        if canvas is None:
            self.canvas.show(self)
        else:
            self.canvas.show(canvas)

    def pre_draw(self):
        self.canvas.pre_draw()
    
    def post_draw(self):
        self.canvas.post_draw()

    def add_object(self, obj):
        self.canvas.add_object(obj)

    def remove_object(self, obj):
        self.canvas.remove_object(obj)
        
    def clear_object(self):
        self.canvas.clear_object()

    def abort(self):
        self.canvas.abort()

    def clear(self):
        self.canvas.clear()

    def get_object_count(self):
        self.canvas.get_object_count()

    def has(self, target_filters):
        
        canvas = self
        
        while True:
            if not isinstance(canvas, LedCanvasFilter):
                return False

            if isinstance(target_filters, list):
                for filter in target_filters:
                    if type(canvas) == filter:
                        return True
            else:
                if type(canvas) == target_filters:
                    return True

            canvas = canvas.canvas

        
            
