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
import traceback
import sys
import zmq
from flask import Flask, request
from Queue import Queue
from libled.simple_run_loop import SimpleRunLoop
from libled.util.flask_on_thread import FlaskOnThread
from libled.util.sound_player import SoundPlayer as sp
import libled.util.logger as logger
from multiprocessing.pool import ThreadPool as Pool


class SoundPlayingServer(SimpleRunLoop):

    def __init__(self):
        super(SoundPlayingServer, self).__init__()
        # player tuple layout: id, player
        self._players = {}

    def on_exception_at_runloop(self, exception):
        self.all_stop()
        return SimpleRunLoop.CONTINUE

    def on_start_runloop(self):
        logger.d('start runloop')
        pass

    def on_do_function(self):
        if not q.empty():
            try:
                req = q.get()
                cmd = req.get('cmd')
                args = req.get('args')
                cmd(args)
            except Exception:
                logger.e('Unexpected do function on message loop.')
                logger.e(traceback.format_exc())

        time.sleep(0.1)

    def on_finish_runloop(self):
        self.all_stop()
        logger.d('finish runloop')

    def all_stop(self):
        map(lambda t: t.do_stop(), self._players.values())

    def get_player(self, player_id, creatable=False):
        if player_id is None:
            return None
        elif player_id in self._players.keys():
            return self._players[player_id]
        elif creatable:
            player = sp.instance()
            self._players[player_id] = player
            return player
        else:
            return None

    def play(self, args):
        # get player
        player = self.get_player(args['content_id'], True)
        if player is None:
            logger.w('null argument content id.')
            return

        # do play
        wav = args['wav']
        if wav is None:
            logger.w('null argument wavefile = ')
            return
        loop = args['loop']

        and_stop = args['and_stop']
        if and_stop:
            player.do_pause()

        player.do_play(wav, loop)
        logger.i('[{}]play {}, loop({})'.format(args['content_id'], wav, loop))

    def stop(self, args):
        if args['content_id'] is None:
            self.all_stop()
            return

        # get player
        player = self.get_player(args['content_id'])
        if player is None:
            logger.w('not founded content id({}).'.format(args['content_id']))
            return

        player.do_stop()
        logger.i('[{}]stop'.format(args['content_id']))

    def volume(self, args):
        # get player
        player = self.get_player(args['content_id'], True)
        if player is None:
            logger.w('not founded content id({}).'.format(args['content_id']))
            return

        player.set_volume(args['val'])
        logger.i('[{}]volume = {}'.format(args['content_id'], args['val']))

    def pause(self, args):
        # get player
        logger.i(type(args))
        player = self.get_player(args['content_id'], True)
        if player is None:
            logger.w('not founded content id({}).'.format(args['content_id']))
            return

        player.do_pause()
        logger.i('[{}]pause'.format(args[0]))

    def resume(self, args):
        # get player
        player = self.get_player(args['content_id'])
        if player is None:
            logger.w('not founded content id({}).'.format(args['content_id']))
            return

        player.do_resume()
        logger.i('[{}]resume'.format(args['content_id']))

# server
# リクエストデータ(json)をパースしてobjectとしてキューに格納するまでを行う。
# リクエスト処理はなる早で返す。SoundPlayerの実行結果は返さない。


app = Flask(__name__)
tcp_port = 5701
pull_port = 5751
q = Queue()
s = SoundPlayingServer()
ctx = zmq.Context()
pull = ctx.socket(zmq.PULL)
logger.i("Collecting updates from audio server...")
abort = False


def run():
    # run_flask()
    run_pull()


def run_pull():
    logger.d('connecting tcp://localhost:{}'.format(pull_port))
    pull.bind('tcp://*:{}'.format(pull_port))
    pool = Pool(1)
    pool.apply_async(parse)
    s.run()  # block
    logger.d('block out pool.')
    pool.close()
    pool.terminate()
    pool.join()
    pull.close()


def parse():
    while True:
        if abort:
            return
        try:
            msg = pull.recv_json()
            logger.d('pull received message = {}'.format(msg))

            func = msg.get('func')
            if func == 'play':
                q.put({'cmd': s.play, 'args': msg.get('data')})
            elif func == 'stop':
                q.put({'cmd': s.stop, 'args': msg.get('data')})
            elif func == 'volume':
                q.put({'cmd': s.volume, 'args': msg.get('data')})
            elif func == 'pause':
                q.put({'cmd': s.pause, 'args': msg.get('data')})
            elif func == 'resume':
                q.put({'cmd': s.resume, 'args': msg.get('data')})
            else:
                logger.w('not found function.')

        except KeyboardInterrupt:
            raise
        except Exception:
            logger.e('Unexpected error: {}'.format(str(sys.exc_info()[0])))
            logger.e(traceback.format_exc())


def run_flask():
    flask = FlaskOnThread(app, port=tcp_port)
    flask.daemon = True
    flask.start()
    s.run()


@app.route('/')
def hello_world():
    return 'Hello Audio module!'


@app.route('/api/play', methods=['POST'])
def play():
    logger.i('call play rest-api audio module.\n' + str(request.data))
    req = get_request()
    args = {'content_id': req.get('content_id'),
            'wav': req.get('wav'),
            'loop': req.get('loop', False),
            'and_stop': req.get('and_stop', False)}
    q.put({'cmd': s.play, 'args': args})
    return ""


@app.route('/api/stop', methods=['POST'])
def stop():
    logger.i('call stop rest-api audio module.\n' + str(request.data))
    req = get_request()
    q.put({'cmd': s.stop,
           'args': {'content_id': req.get('content_id')}
           })
    return ""


@app.route('/api/volume', methods=['POST'])
def vol():
    logger.i('call volume rest-api audio module.\n' + str(request.data))
    req = get_request()
    q.put({'cmd': s.volume,
           'args': {'content_id': req.get('content_id'),
                    'val': req.get('val', 0.5)}
           })
    return ""


@app.route('/api/pause', methods=['POST'])
def pause():
    logger.i('call pause rest-api audio module.\n' + str(request.data))
    req = get_request()
    q.put({'cmd': s.pause,
           'args': {'content_id': req.get('content_id')}
           })
    return ""


@app.route('/api/resume', methods=['POST'])
def resume():
    logger.i('call resume rest-api audio module.\n' + str(request.data))
    req = get_request()
    q.put({'cmd': s.resume,
           'args': {'content_id': req.get('content_id')}
           })
    return ""


def get_request():
    return json.loads(request.data)


# run module
run()
