from ..i_led_canvas import ILedCanvas

class LedCanvasFilter(ILedCanvas):

    def __init__(self, canvas):
        self.canvas = canvas

    def set_led(self, x, y, z, color):
        self.canvas.set_led(x, y, z, color)

    def show(self, canvas=None):
        self.canvas.show(self)

    def add_object(self, obj):
        self.canvas.add_object(obj)

    def clear_object(self):
        self.canvas.clear_object()

    def abort(self):
        self.canvas.abort()

