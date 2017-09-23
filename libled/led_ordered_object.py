from object.led_object import LedObject

class LedDotObject(LedObject):

    def __init__(self, objects, lifetime = 0 ):
        super(LedDotObject, self).__init__(lifetime)
        self.objects = objects
        self.index = 0

    def draw(self, canvas):
        obj = self.objects[self.index]
        if self.is_cancel():
            return

        if obj.is_expired():
            self.index += 1

        if(self.index > len(self.objects)):
            return

        obj.draw(canvas)         
            
       
