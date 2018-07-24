# -*- coding: utf-8 -*-
import zmq
import requests
import threading
import json
import logger
from sound_pool import SoundPool

# debug
# import logging
# logging.basicConfig(level=logging.DEBUG)


class SoundInterface(object):
    def __new__(cls):
        raise NotImplementedError('Cant call this Constructor.')

    domain = 'http://localhost:5701/api/'
    content_id = ''

    pool = SoundPool(1)

    @classmethod
    def close(cls):
        SoundInterface.stop()
        SoundInterface.pool.abort = True
        SoundInterface.pub.close()

    @classmethod
    def play(cls, id_=None, wav='', loop=False, stop=False):
        if id_ is None:
            id_ = SoundInterface.content_id
        func = 'play'
        data_ = {
            'content_id': id_,
            'wav': wav,
            'loop': loop,
            'and_stop': stop
        }
        SoundInterface.post(func, data_=data_)

    @classmethod
    def pause(cls, id_=None):
        func = 'pause'
        data_ = {
            'content_id': id_
        }
        SoundInterface.post(func, data_=data_)

    @classmethod
    def resume(cls, id_=None):
        func = 'resume'
        data_ = {
            'content_id': id_
        }
        SoundInterface.post(func, data_=data_)

    @classmethod
    def stop(cls, id_=None):
        func = 'stop'
        data_ = {
            'content_id': id_
        }
        SoundInterface.post(func, data_=data_)

    @classmethod
    def volume(cls, id_=None, val=0.5):
        func = 'volume'
        data_ = {
            'content_id': id_,
            'val': val
        }
        SoundInterface.post(func, data_=data_)

    @classmethod
    def post(cls, func, data_):
        SoundInterface.pool.put({'domain': SoundInterface.domain,
                                 'func': func,
                                 'data': data_})

    @classmethod
    def __post_threading(cls, func, data_, on_complated):
        th = threading.Thread(target=SoundInterface.__post_requests,
                              args=(
                                  SoundInterface.domain + func,
                                  data_,
                                  on_complated,
                              ))
        th.start()

    @classmethod
    def __post_requests(cls, arg):
        uri_ = arg.get('domain') + arg.get('func')
        data_ = arg.get('data')
        proxies = {
            'http': '',
            'https': '',
        }
        timeout = 0.1
        res = requests.post(
            uri_,
            json.dumps(data_),
            headers={'Content-Type': 'application/json'},
            proxies=proxies,
            timeout=timeout)
        return res

    @classmethod
    def __post_pub(cls, arg):
        SoundInterface.pub.send_json(arg)

    @classmethod
    def _init_pool(cls):
        SoundInterface.pool.set_work(SoundInterface.__post_pub)
        SoundInterface.pool.set_complated(
            lambda x: logger.d('post result = {}'.format(x)))

    @classmethod
    def _init_pub(cls):
        ctx = zmq.Context()
        SoundInterface.pub = ctx.socket(zmq.PUB)
        SoundInterface.pub.bind('tcp://*:5751')


SoundInterface.pool.run_async()
SoundInterface._init_pool()
SoundInterface._init_pub()
