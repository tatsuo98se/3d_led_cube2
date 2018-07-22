# -*- coding: utf-8 -*-
import requests
import json
import logger


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
        res = SoundInterface.post(uri_, data_=data_)
        # logger.d('[{}]post play {} = {}'.format(id_, wav, res.status_code))

    @classmethod
    def pause(cls, id_=None):
        uri_ = SoundInterface.domain + 'pause'
        data_ = {
            'content_id': id_
        }
        res = SoundInterface.post(uri_, data_=data_)
        logger.d('post pause = {}'.format(res.status_code))

    @classmethod
    def resume(cls, id_=None):
        uri_ = SoundInterface.domain + 'resume'
        data_ = {
            'content_id': id_
        }
        res = SoundInterface.post(uri_, data_=data_)
        logger.d('post resume = {}'.format(res.status_code))

    @classmethod
    def stop(cls, id_=None):
        uri_ = SoundInterface.domain + 'stop'
        data_ = {
            'content_id': id_
        }
        res = SoundInterface.post(uri_, data_=data_)
        logger.d('post stop = {}'.format(res.status_code))

    @classmethod
    def volume(cls, id_=None, val=0.5):
        uri_ = SoundInterface.domain + 'volume'
        data_ = {
            'content_id': id_,
            'val': val
        }
        res = SoundInterface.post(uri_, data_=data_)
        logger.d('post stop = {}'.format(res.status_code))

    @classmethod
    def post(cls, uri_, data_):
        res = requests.post(
            uri_,
            json.dumps(data_),
            headers={'Content-Type': 'application/json'})
        return res
