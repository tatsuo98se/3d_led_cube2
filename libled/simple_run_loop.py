# -*- coding:utf-8 -*-
import sys
import time
import traceback
import threading
import libled.util.logger as logger


class SimpleRunLoop(object):
    CONTINUE = 1
    EXIT = 2

    def __init__(self):
        self.aborted = False
        self.run_loop_finished = False

    def run(self):
        self.run_async()

        try:
            while True:
                if self.aborted:
                    break
                time.sleep(0.5)

        except KeyboardInterrupt:
            logger.d('keyboard Ctrl+C in simple_run_loop.run()')
            self.on_keyboard_interrupt()
            raise
        except Exception:
            logger.e('Unexpected error: {}'.format(str(sys.exc_info()[0])))
            logger.e(traceback.format_exc())
            raise
        finally:
            self.aborted = True
            logger.i('finish run')

    def run_async(self):
        th = threading.Thread(name='message_loop',
                              target=self.__message_loop)
        th.start()

    def __message_loop(self):
        try:
            logger.d('start runloop')
            self.on_start_runloop()
            while True:
                try:
                    if self.aborted:
                        return

                    self.on_do_function()

                except Exception as exception:
                    ret = self.on_exception_at_runloop(exception)
                    if (ret == SimpleRunLoop.CONTINUE):
                        logger.d('continue runloop')
                        continue
                    else:
                        logger.e('Unexpected error: {}'.format(
                            str(sys.exc_info()[0])))
                        logger.e(traceback.format_exc())
                        logger.e('exit runloop by exception')
                        return

        finally:
            self.run_loop_finished = True
            self.on_finish_runloop()
            logger.d('finished runloop')

    def on_keyboard_interrupt(self):
        pass

    def on_exception_at_runloop(self, exception):
        pass

    def on_start_runloop(self):
        pass

    def on_finish_runloop(self):
        pass

    def on_do_function(self):
        pass
