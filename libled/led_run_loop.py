# coding: UTF-8
from optparse import OptionParser
from led_framework import LedFramework
from libled.led_cube import *
import threading
from Queue import Queue
import time
import traceback
import socket
import json
import sys

class LedRunLoop(object):

    CONTINUE = 1
    EXIT = 2

    def __init__(self, parser = OptionParser()):
        self.message = Queue()
        self.aborted = False
        self.opt_parser = parser
 
    def run(self):
        self.opt_parser.add_option("-d", "--dest",
                        action="store", type="string", dest="dest", 
                        help="(optional) ip address of destination device which connect to real 3d cube.")

        options, _ = self.opt_parser.parse_args()

        if options.dest != None:
            print("External Connect To: " + (options.dest))
            led.SetUrl(options.dest)

        th = threading.Thread(name="message_receive_loop", target=self.message_receive_loop, args=(self.message,))
        th.setDaemon(True)
        th.start()

        try:
            while True:
                if self.aborted:
                    break

                if self.message.empty():
                    time.sleep(0.1)
                else:
                    msg = self.message.get()
                    msg[0](msg[1])


        except KeyboardInterrupt:
            print('keybord Ctrl+C')
            self.on_keyboard_interrupt()
        except:
            print("Unexpected error:", sys.exc_info()[0])
            print(traceback.format_exc())
            raise
        finally:
            self.aborted = True
            self.on_finish()
            th.join()
            print('finish main loop')

    def message_receive_loop(self, q):
        led_framework = LedFramework()

        try:
            while True:
                try:
                    self.on_pre_exec_runloop()

                    while True:

                        line = self.read_data()
                        if self.aborted:
                            return

                        if not line:
                            print("line is empty")
                            break
                        
                        if line.startswith('abort'):
                            print('abort canvas')
                            led_framework.abort()
                        elif line.startswith('show:'):
                            print('show by orders')
                            orders = line[len('show:'):].strip()

                            dic_orders = None
                            try:
                                dic_orders = json.loads(orders)
                            except ValueError:
                                print('invalid order:' + str(orders))
                                continue
                            
                            led_framework.abort()
                            q.put([led_framework.show, dic_orders])

                    self.on_post_exec_runloop()

                except Exception as exception:
                    ret = self.on_exception_at_runloop(exception)
                    if(ret == LedRunLoop.CONTINUE):
                        print("continue runloop")
                        continue
                    else:
                        print("Unexpected error:", sys.exc_info()[0])
                        print(traceback.format_exc())
                        print("exit runloop by exception")
                        return

        except:
            print("Unexpected error:", sys.exc_info()[0])
            print(traceback.format_exc())
            raise
        finally:
            self.run_loop_finished = True
            print('finish led order loop')


    def on_finish(self):
        pass

    def on_keyboard_interrupt(self):
        pass

    def on_exception_at_runloop(self, exception):
        return LedRunLoop.EXIT

    def read_data(self):
        return ""

    def on_pre_exec_runloop(self):
        pass

    def on_post_exec_runloop(self):
        pass

