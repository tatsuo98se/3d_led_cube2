# -*- coding: utf-8 -*-
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

    @classmethod
    def play(cls, id_=None, wav='', loop=False, stop=False):
        if id_ is None:
            id_ = SoundInterface.content_id
        uri_ = SoundInterface.domain + 'play'
        data_ = {
            'content_id': id_,
            'wav': wav,
            'loop': loop,
            'and_stop': stop
        }
        SoundInterface.post(uri_, data_=data_)

    @classmethod
    def pause(cls, id_=None):
        uri_ = SoundInterface.domain + 'pause'
        data_ = {
            'content_id': id_
        }
        SoundInterface.post(uri_, data_=data_)

    @classmethod
    def resume(cls, id_=None):
        uri_ = SoundInterface.domain + 'resume'
        data_ = {
            'content_id': id_
        }
        SoundInterface.post(uri_, data_=data_)

    @classmethod
    def stop(cls, id_=None):
        uri_ = SoundInterface.domain + 'stop'
        data_ = {
            'content_id': id_
        }
        SoundInterface.post(uri_, data_=data_)

    @classmethod
    def volume(cls, id_=None, val=0.5):
        uri_ = SoundInterface.domain + 'volume'
        data_ = {
            'content_id': id_,
            'val': val
        }
        SoundInterface.post(uri_, data_=data_)

    @classmethod
    def post(cls, uri_, data_):
        SoundInterface.pool.put({'uri': uri_, 'data': data_})

    @classmethod
    def __post_threading(cls, uri_, data_, on_complated):
        th = threading.Thread(target=SoundInterface.__post,
                              args=(
                                  uri_,
                                  data_,
                                  on_complated,
                              ))
        th.start()

    @classmethod
    def __post_requests(cls, arg):
        uri_ = arg.get('uri')
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
    def _init_pool(cls):
        SoundInterface.pool.set_work(SoundInterface.__post)
        SoundInterface.pool.set_complated(
            lambda x: logger.d('post result = {}'.format(x)))


SoundInterface.pool.run_async()
SoundInterface._init_pool()
