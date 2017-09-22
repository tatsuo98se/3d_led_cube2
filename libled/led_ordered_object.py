from led_object import LedObject

class LedDotObject(LedObject):

    objects = []

    def __init__(self, objects, lifetime = 0 ):
        super(LedDotObject, self).__init__(lifetime)
        self.objects = objects

    def draw(self, canvas):
        for obj in self.objects:
            
       
