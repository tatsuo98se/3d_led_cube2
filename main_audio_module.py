# -*- encoding:utf-8 -*-
'''
音楽再生モジュール
別プロセスで音楽を再生するために作成

使い方
localhost:5701/apiに対して次のRESTをPOSTする。
 ※全てに共通の項目
  content_id='コンテンツのID'
   '00'を指定すると全てのプレイヤーへ操作を行う
   指定のIDが存在しない場合、playのみ新しいプレイヤーを作成して再生を開始する
 /play
  wav='wavファイル名'
   指定のファイル名に.wavを足したものを再生する。
  loop=True/False
   ループ再生する。
   デフォルトはFalse
  and_stop=True/False
   pause状態でプレイヤーを作成する。
   デフォルトはFalse。pause状態で開始するためresumeで再開する。
 /stop
  プレイヤーで再生中のすべての音楽を停止してプレイヤーを破棄する。（再開不可）
 /volume
  プレイヤーで再生中のすべての音楽の音量を変える。
  val=0.0 - 1.0
 /pause
  プレイヤーで再生中のすべての音楽を一時停止する。（再開可）
 /resume
  プレイヤーで再生中のすべての音楽を再開する。
'''

import time
import json
from flask import Flask, request
from Queue import Queue
from libled.simple_run_loop import SimpleRunLoop
from libled.util.flask_on_thread import FlaskOnThread
from libled.util.sound_player import SoundPlayer as sp
import libled.util.logger as logger

# import pdb

# 本体


class SoundPlayingServer(SimpleRunLoop):

    def __init__(self):
        super(SoundPlayingServer, self).__init__()
        # player tuple layout: id, player
        self.players = []

    def on_exception_at_runloop(self, exception):
        self.all_stop()
        return SimpleRunLoop.EXIT

    def on_start_runloop(self):
        logger.d('start runloop')
        pass

    def on_do_function(self):
        if not q.empty():
            message = q.get()
            logger.d(message)

        time.sleep(0.01)

    def on_finish_runloop(self):
        self.all_stop()
        logger.d('finish runloop')

    def all_stop(self):
        map(lambda t: t.player.do_stop(), self.players)

    def play(self, args):
        pass

    def stop(self, args):
        pass

    def volume(self, args):
        pass

    def pause(self, args):
        pass

    def resume(self, args):
        pass

# server
# リクエストデータ(json)をパースしてobjectとしてキューに格納するまでを行う。
# リクエスト処理はなる早で返す。SoundPlayerの実行結果は返さない。


app = Flask(__name__)
tcp_port = 5701
q = Queue()
s = SoundPlayingServer()


def run():
    flask = FlaskOnThread(app, port=tcp_port)
    flask.daemon = True
    flask.start()
    s.run()


@app.route('/')
def hello_world():
    return 'Hello Audio module!'


@app.route('/api/play', methods=['POST'])
def play():
    logger.d('call play rest-api audio module.\n' + str(request.data))
    req = get_request()
    args = (req.get('content_id'),
            req.get('wav'),
            req.get('loop', False),
            req.get('and_stop', False))
    q.put(s.play, args)
    return ""


@app.route('/api/stop', methods=['POST'])
def stop():
    logger.d('call stop rest-api audio module.\n' + str(request.data))
    req = get_request()
    msg = req.get('content_id')
    q.put(s.stop, msg)
    return ""


@app.route('/api/volume', methods=['POST'])
def vol():
    logger.d('call volume rest-api audio module.\n' + str(request.data))
    req = get_request()
    q.put(s.stop,
          (req.get('content_id'), req.get('val', 0.5)))
    return ""


@app.route('/api/pause', methods=['POST'])
def pause():
    logger.d('call pause rest-api audio module.\n' + str(request.data))
    return ""


@app.route('/api/resume', methods=['POST'])
def resume():
    logger.d('call resume rest-api audio module.\n' + str(request.data))
    return ""


def get_request():
    return json.loads(request.data)


# run module
run()
