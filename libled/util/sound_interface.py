# -*- coding: utf-8 -*-
import requests
import threading
import json
import logger

# debug
# import logging
# logging.basicConfig(level=logging.DEBUG)


class SoundInterface(object):
    def __new__(cls):
        raise NotImplementedError('Cant call this Constructor.')

    domain = 'http://localhost:5701/api/'
    content_id = ''

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
        SoundInterface.post(uri_,
                            data_=data_,
                            on_complated=lambda res:
                            logger.d('[{}]post play {} = {}'.format(id_,
                                                                    wav,
                                                                    res.status_code)))

    @classmethod
    def pause(cls, id_=None):
        uri_ = SoundInterface.domain + 'pause'
        data_ = {
            'content_id': id_
        }
        SoundInterface.post(uri_,
                            data_=data_,
                            on_complated=lambda res:
                            logger.d('post pause = {}'.format(res.status_code)))

    @classmethod
    def resume(cls, id_=None):
        uri_ = SoundInterface.domain + 'resume'
        data_ = {
            'content_id': id_
        }
        SoundInterface.post(uri_,
                            data_=data_,
                            on_complated=lambda res:
                            logger.d('post resume = {}'.format(res.status_code)))

    @classmethod
    def stop(cls, id_=None):
        uri_ = SoundInterface.domain + 'stop'
        data_ = {
            'content_id': id_
        }
        SoundInterface.post(uri_,
                            data_=data_,
                            on_complated=lambda res:
                            logger.d('post stop = {}'.format(res.status_code)))

    @classmethod
    def volume(cls, id_=None, val=0.5):
        uri_ = SoundInterface.domain + 'volume'
        data_ = {
            'content_id': id_,
            'val': val
        }
        SoundInterface.post(uri_,
                            data_=data_,
                            on_complated=lambda res:
                            logger.d('post stop = {}'.format(res.status_code)))

    @classmethod
    def post(cls, uri_, data_, on_complated):
        th = threading.Thread(target=SoundInterface.__post,
                              args=(
                                  uri_,
                                  data_,
                                  on_complated,
                              ))
        th.start()

    @classmethod
    def __post(cls, uri_, data_, on_complated):
        proxies = {
            'http': '',
            'https': '',
        }
        timeout = 0.005
        res = requests.post(
            uri_,
            json.dumps(data_),
            headers={'Content-Type': 'application/json'},
            proxies=proxies,
            timeout=timeout)
        on_complated(res)
