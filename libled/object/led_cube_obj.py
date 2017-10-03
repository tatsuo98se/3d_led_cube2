from led_object import LedObject
from ..util import vectors_util as Vectors


class LedCubeObject(LedObject):

    def __init__(self, lifetime=0):
        super(LedCubeObject, self).__init__(lifetime)
        self.ix = 0

    def draw(self, canvas):
        framework_wait_time = 20
        speed = 1
        N = self.lifetime * framework_wait_time * speed
        Vectors.concentric(canvas, self.ix, N,
                           lambda dx, dy, dz, t: Vectors.max3(abs(dx), abs(dy), abs(dz)))
        self.ix += speed
