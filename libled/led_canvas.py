from led_cube import *
from i_led_canvas import ILedCanvas

class LedCanvas(ILedCanvas):

    def __init__(self):
        self.is_abort = False
        self.objects = []

    def set_led(self, x, y, z, color):
        led.SetLed(
            int(round(x)),
            int(round(y)),
            int(round(z)),
            int(color))

    def show(self, canvas=None):
        led.Clear()
        for obj in self.objects[:]:
            obj.will_draw()
            if obj.is_expired() or obj.is_abort:
                self.objects.remove(obj)
            else:
                if canvas is None:
                    obj.draw(self)
                else:
                    obj.draw(canvas)

        led.Show()
    
    def add_object(self, obj):
        self.objects.append(obj)

    def remove_object(self, obj):
        self.objects.remove(obj)

    def clear_object(self):
        self.objects = []

    def abort(self):
        self.is_abort = True
        for obj in self.objects[:]:
            obj.abort()

    def clear(self):
        for obj in self.objects[:]:
            obj.abort()
        self.objects = []
        led.Clear()
        led.Show()
