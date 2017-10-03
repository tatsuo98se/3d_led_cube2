from led_object import LedObject
from ..util import vectors_util as Vectors
import math


class LedSphereObject(LedObject):

    def __init__(self, lifetime=0):
        super(LedSphereObject, self).__init__(lifetime)
        self.ix = 0

    def draw(self, canvas):
        framework_wait_time = 20
        speed = 1
        N = self.lifetime * framework_wait_time * speed
        Vectors.concentric(canvas, self.ix, N,
                           lambda dx, dy, dz, t:
                           math.sqrt(dx * dx + dy * dy + dz * dz))
        self.ix += speed
