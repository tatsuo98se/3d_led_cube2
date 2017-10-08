import time
from .util import sync
from abc import ABCMeta, abstractmethod

class ILedCanvas(object):

    @abstractmethod
    def set_led(self, x, y, z, color):
        pass

    @abstractmethod
    def show(self, canvas=None):
        pass

    @abstractmethod
    def add_object(self, obj):
        pass

    @abstractmethod
    def remove_object(self, obj):
        pass

    @abstractmethod
    def clear_object(self):
        pass

    @abstractmethod
    def abort(self):
        pass

    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def get_object_count(self):
        pass

