from led_object import LedObject

class LedDotObject(LedObject):

    def __init__(self, x, y, z, color, lifetime = 0 ):
        super(LedDotObject, self).__init__(lifetime)
        self.x = x
        self.y = y
        self.z = z
        self.color = color

    def draw(self, canvas):
        canvas.set_led(self.x, self.y, self.z, self.color)