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
import util.logger as logger
from libled.util.sound_interface import SoundInterface

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

        self.opt_parser.add_option("-r", "--rs",
                        action="store", type="string", dest="rs", default="localhost",
                        help="(optional) ip address of realsense module.")

        self.opt_parser.add_option("-c", "--ctrl",
                        action="store", type="string", dest="ctrl", default="localhost",
                        help="(optional) ip address of hw controller module.")

        self.opt_parser.add_option("-m", "--hide-simulator",
                        action="store_true", dest="hide_simulator", default=False,
                        help="(optional) hide simulator window")

        options, _ = self.opt_parser.parse_args()

        if options.dest != None:
            logger.i("External Connect To: " + (options.dest))
            led.SetUrl(options.dest)
        
        led.EnableSimulator(not options.hide_simulator)

        th = threading.Thread(name="message_receive_loop", target=self.message_receive_loop, args=(self.message, options))
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
            logger.i('keybord Ctrl+C')
            self.on_keyboard_interrupt()
        except:
            logger.e("Unexpected error:" + str(sys.exc_info()[0]))
            logger.e(traceback.format_exc())
            raise
        finally:
            self.aborted = True
            self.on_finish()
            th.join()
            logger.i('finish main loop')

    def message_receive_loop(self, q, options):
#        led_framework = LedFramework()
        with LedFramework(rs_host=options.rs, hwctrl_host=options.ctrl) as led_framework:
            try:
                while True:
                    try:
                        self.on_pre_exec_runloop()

                        while True:

                            line = self.read_data()
                            if self.aborted:
                                return

                            if not line:
                                print('')
                                logger.w("line is empty")
                                break
                            
                            if line.startswith('abort'):
                                logger.i('abort canvas')
                                led_framework.abort()
                            elif line.startswith('show:'):
                                logger.i('show by orders')
                                orders = line[len('show:'):].strip()

                                dic_orders = None
                                try:
                                    dic_orders = json.loads(orders)
                                except ValueError:
                                    logger.w('invalid order:' + str(orders))
                                    continue
                                
                                led_framework.abort()
                                q.put([led_framework.show, dic_orders])

                        self.on_post_exec_runloop()

                    except Exception as exception:
                        ret = self.on_exception_at_runloop(exception)
                        if(ret == LedRunLoop.CONTINUE):
                            logger.i("continue runloop")
                            continue
                        else:
                            logger.e("Unexpected error:" + str(sys.exc_info()[0]))
                            logger.e(traceback.format_exc())
                            logger.e("exit runloop by exception")
                            return

            except:
                logger.e("Unexpected error:" + str(sys.exc_info()[0]))
                logger.e(traceback.format_exc())
                raise
            finally:
                self.run_loop_finished = True
                SoundInterface.stop()
                logger.i('finish led order loop')


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

