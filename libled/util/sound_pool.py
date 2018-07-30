# -*- coding:utf-8 -*-

from multiprocessing.pool import ThreadPool as Pool
from multiprocessing import cpu_count
import Queue

import sys
import time
import traceback
import logger


class SoundPool(object):

    def __init__(self, pool_num=0):
        self.pool_num_ = pool_num if pool_num > 0 else cpu_count()
        self.q = Queue.Queue()
        self.__work = None
        self.__complated = None
        self.abort = False
        logger.d('set pool = {}'.format(self.pool_num_))

    def set_work(self, func=None):
        self.__work = func

    def do_work(self, arg=None):
        if self.__work is None:
            return
        try:
            if arg is None:
                res = self.__work()
            else:
                res = self.__work(arg)
            self.do_complated(res)
        except Exception:
            logger.e('Unexpected error: {}'.format(str(sys.exc_info()[0])))
            logger.e(traceback.format_exc())
        except KeyboardInterrupt:
            logger.d('keyboard Ctrl+C in sound_pool.do_work()')
            self.abort = True
            raise

    def set_complated(self, func=None):
        self.__complated = func

    def do_complated(self, res):
        if self.__complated is None:
            return
        self.__complated(res)

    def __worker(self):
        while True:
            # logger.d('queue size = {}'.format(self.q.qsize()))
            try:
                if self.abort:
                    return

                req = self.q.get(timeout=3)
                self.do_work(req)
                logger.d('kick work = {}'.format(req))
                self.q.task_done()
            except Queue.Empty:
                time.sleep(0.05)
            except Queue.Full:
                continue
            except KeyboardInterrupt:
                self.abort = True
                raise
            except Exception:
                raise

    def put(self, item, block=True, timeout=None):
        self.q.put(item, block, timeout)
        logger.d('put {}'.format(item))

    def run(self):
        p = Pool(self.pool_num_)
        p.apply(self.__worker)
        logger.d('closing sound pool.')
        p.close()
        p.terminate()
        p.join()
        logger.d('closed sound pool.')

    def run_async(self):
        import threading
        worker = threading.Thread(target=self.run, name='sound pool worker')
        worker.start()
