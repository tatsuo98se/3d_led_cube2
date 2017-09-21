from led_cube import *

class LedCanvas:

    def __init__(self):
        self.objects = []

    def set_led(self, x, y, z, color):
        led.SetLed(round(x), round(y), round(z), color)
        
    def show(self):
        led.Clear()
        for obj in self.objects[:]:
            if obj.is_expired():
                self.objects.remove(obj)
            else:
                obj.draw(self)
        
        led.show()

    def add_object(self, obj):
        self.objects.append(obj)
    
    def clear_object(self):
        self.objects = []