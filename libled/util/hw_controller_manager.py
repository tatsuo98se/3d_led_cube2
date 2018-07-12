import sys
import glob
import serial
import json
import time
import urllib2
import traceback
from time import sleep
from threading import Thread
import logger
from serial_util import *
import zmq

class ReadLineWorker(Thread):

    def __init__(self, event, initial_data):
        super(ReadLineWorker,self).__init__()

        self.context = zmq.Context()
        self.socket = context.socket(zmq.SUB)
        logger.i("Collecting updates from gamepad server...")
        self.socket.connect("tcp://localhost:5602")
        self.socket.setsockopt(zmq.SUBSCRIBE, '')

        self.is_stop = False
        self.line = initial_data
        self.event = event

    def run(self):
        try:
            while not self.is_stop:
                try:
                    self.event()
                    self.line = self.socket.recv_json()
                except ValueError:
                    logger.w("HwController recive unexpected data format.")
                    continue
        finally:
            if self.socket is not None:
                self.socket.close()
            if self.context is not None:
                self.context.term()
         

    def stop(self):
        self.is_stop = True

    def get_data(self):
        return self.line 

class HwControllerManager:
    _instance = None
    _port = None
    _observers = []

    def __init__(self):
        initial_data = None
        self.worker = None
        while True:
            try:
                initial_data = urllib2.urlopen('http://localhost:5601/api/gamepad').read()
                self.worker = ReadLineWorker(lambda: HwControllerManager.event(), json.loads(initial_data))
                self.worker.start()
                break
            except urllib2.HTTPError as e:
                if e.code == 503:
                    sleep(3)
                    continue
                else:
                    raise
            except:
                raise

    @classmethod
    def event(cls):
        for observer in cls._observers:
            observer.update(cls.get_data())

    @classmethod
    def add_observer(cls,observer):
        cls._observers.append(observer)

    @classmethod
    def remove_observer(cls, observer):
        cls._observers.remove(observer)

    @classmethod
    def init(cls):
        if cls._instance is None:
            try:
                cls._instance = cls()
                logger.i("initialize gamepad is successfull.")
            except:
                logger.e("initialize gamepad failed.:" + str(sys.exc_info()[0]))
                logger.e(traceback.format_exc())
        return cls._instance

    @classmethod
    def get_data(cls):
        if cls._instance is not None and cls._instance.worker is not None:
            return cls._instance.worker.get_data()
        else:
            return None

    @classmethod
    def stop(cls):
        if cls._instance is not None:
            cls._instance.__stop()
            cls._instance = None

    def __stop(self):
        self.worker.stop()
