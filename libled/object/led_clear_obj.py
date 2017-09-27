from led_object import LedObject

class LedClearObject(LedObject):

    def __init__(self, lifetime = 0 ):
        super(LedClearObject, self).__init__(lifetime)

    def draw(self, canvas):
        canvas.clear()
