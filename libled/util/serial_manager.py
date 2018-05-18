import serial
import json
import time
from time import sleep
from threading import Thread

class ReadLineWorker(Thread):

    def __init__(self, ser):
        super(ReadLineWorker,self).__init__()
        self.ser = ser
        self.is_stop = False
        self.line = ''

    def readline(self, ser):
        line = ''
        ser.write("a")
        while ser.in_waiting :
            line = ser.readline()
        return line

    def run(self):
        while not self.is_stop:
            line = self.readline(self.ser)
            if line is not '':
        	    self.line = line
            time.sleep(0.2)
    
    def stop(self):
        self.is_stop = True

    def get_data(self):
        return self.line 

class SerialManager:
    _instance = None

    def __init__(self, port_name, port_number):
        self.serial = serial.Serial(port_name, port_number)
        self.worker = ReadLineWorker(self.serial)
        self.worker.start()

    @classmethod
    def init(cls, port_name, port_number):
        if cls._instance is None:
            try:
                cls._instance = cls(port_name, port_number)
            except serial.SerialException:
                pass

        return cls._instance

    @classmethod
    def get_serial_handle(cls):
        if cls._instance is not None:
            return cls._instance.__get_serial_handle()
        else:
            return None

    @classmethod
    def get_data(cls):
        if cls._instance is not None:
            return cls._instance.worker.get_data()
        else:
            return ''

    @classmethod
    def stop(cls):
        if cls._instance is not None:
            cls._instance.__stop()
            cls._instance = None

    def __get_serial_handle(self):
        return self.serial

    def __stop(self):
        if self.serial is not None:
            self.serial.close()
        self.worker.stop()
