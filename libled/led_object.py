import time
import sync
from abc import ABCMeta, abstractmethod

class LedObject(object):

    myLock = sync.create_lock()

    def __init__(self, lifetime=0):
        self.born_at = 0
        self.lifetime = lifetime
        self.is_abort = False

    def elapsed(self):
        return time.time() - self.born_at

    def is_expired(self):
        if self.lifetime == 0 or self.born_at == 0:
            return False

        if self.lifetime < time.time() - self.born_at:
            return True

        return False

    @abstractmethod
    def draw(self, canvas):
        pass

    @sync.synchronized(myLock)
    def abort(self):
        self.is_abort = True

    @sync.synchronized(myLock)
    def is_cancel(self):
        return self.is_abort

    def will_draw(self):
        if self.born_at == 0:
            self.born_at = time.time()


