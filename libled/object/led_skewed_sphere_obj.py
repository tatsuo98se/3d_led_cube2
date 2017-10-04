from led_object import LedObject
from ..util import vectors_util as Vectors
import math


class LedSkewedSphereObject(LedObject):

    def __init__(self, lifetime=0):
        super(LedSkewedSphereObject, self).__init__(lifetime)
        self.ix = 0

    def draw(self, canvas):
        framework_wait_time = 20
        speed = 1
        N = self.lifetime * framework_wait_time * speed
        Vectors.concentric(canvas, self.ix, N, self.draw_core)
        self.ix += speed

    def draw_core(self, dx0, dy, dz0, t):
       dx, dz = Vectors.skewed(dx0, dy, dz0, t)
       return math.sqrt(dx * dx + dy * dy + dz * dz)
