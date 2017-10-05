from led_object import LedObject

class LedObjectFilter(LedObject):

    def __init__(self, obj):
        self.obj = obj
        self.born_at = obj.born_at
        self.lifetime = obj.lifetime

    def elapsed(self):
        return self.obj.elapsed()

    def is_expired(self, offset = 0):
        return self.obj.is_expired(offset)

    def draw(self, canvas):
        return self.obj.draw(canvas)

    def abort(self):
        return self.obj.abort()

    def is_cancel(self):
        return self.obj.is_cancel()

    def will_draw(self):
        return self.obj.will_draw()


