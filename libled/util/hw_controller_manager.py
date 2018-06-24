import sys
import glob
import serial
import json
import time
from time import sleep
from threading import Thread
import logger

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

class HwControllerManager:
    _instance = None
    _port = None

    def __init__(self, port):
        self.serial = serial.Serial(port, 9600)
        self.worker = ReadLineWorker(self.serial)
        self.worker.start()

    @classmethod
    def __enum_serial_posts(cls):
        if sys.platform.startswith('win'):
            return ['COM%s' % (i + 1) for i in range(10)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            return glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            return glob.glob('/dev/tty.*')

        else:
            raise EnvironmentError('Unsupported platform')

    @classmethod
    def __find_controller_port(cls):
        ports = cls.__enum_serial_posts()
        for port in ports:
            s = None
            try:
                s = serial.Serial(port, 9600, timeout=0.5)
                line = ''
                for _ in xrange(3): # try 3 times
                    s.write("z")
                    line = s.readline()
                    if not line == '':
                        j = json.loads(line)
                        if j['version'] == '1.0':
                            return port
                    sleep(0.1)
            except (OSError, serial.SerialException, ValueError):
                pass
            finally:
                if s is not None:
                    s.close()

        return None


    @classmethod
    def init(cls):
        try:
            if cls._port is None:
                logger.i("searching controller....")
                cls._port = cls.__find_controller_port()

            if cls._instance is None and cls._port is not None:
                logger.i("find port: " + str(cls._port))
                try:
                    cls._instance = cls(cls._port)
                except serial.SerialException:
                    pass
            else:
                logger.w("controller is not connected.")
        except:
            logger.e('HwControllerManager.init() failed.' + str(sys.exc_info()[0]))


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
            return None

    @classmethod
    def get_data_as_json(cls, defaults=None):
        if cls._instance is None:
            return defaults

        while True:
            try:
                line = cls.get_data()
                return json.loads(line)
            except ValueError:
                time.sleep(0.2)
                continue
        

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
