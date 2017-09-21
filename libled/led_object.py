import time
from abc import ABCMeta, abstractmethod

class LedObject:

    def __init__( self, lifetime = 0 ):
        self.born_at = time.time()
        self.lifetime = lifetime

    def elapsed(self):
        return time.time() - self.born_at

    def is_expired(self):
        if self.lifetime == 0:
            return False

        if self.lifetime < time.time() - self.born_at:
            return True

        return False

    @abstractmethod
    def draw(self, canvas):
        pass