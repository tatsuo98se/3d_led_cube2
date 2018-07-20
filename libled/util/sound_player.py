# -*- coding: utf-8 -*-
import pyaudio
import wave
import threading
import time
import sound_effects as fx

import logger

# defines
CHUNK = 1024


class SoundPlayer(object):
    # __instance = None
    # __lock = threading.Lock()

    def __new__(cls):
        raise NotImplementedError('Cant call this Constructor.')

    @classmethod
    def __internal_new__(cls):
        return super(SoundPlayer, cls).__new__(cls)

    @classmethod
    def instance(cls):
        inst = cls.__internal_new__()
        inst.__internal_init__()
        return inst
        # if not cls.__instance:
        #     with cls.__lock:
        #         if not cls.__instance:
        #             cls.__instance = cls.__internal_new__()
        #             cls.__instance.__internal_init__()
        # return cls.__instance

    @classmethod
    def show_wavinfo(self, wfinfo):
        logger.d(wfinfo)
        logger.d('wave file info')
        logger.d('channels = {}'.format(wfinfo[0]))
        logger.d('sampling width = {} byte'.format(wfinfo[1]))
        logger.d('frame rate = {} Hz'.format(wfinfo[2]))
        logger.d('frame count = {}'.format(wfinfo[3]))
        logger.d('sound time = {} s'.format((int)(wfinfo[3] / wfinfo[2])))

    def __internal_init__(self):
        # flags
        # self._loop = False

        # event flags
        self._event_pause = threading.Event()
        self._event_stop = threading.Event()
        self.__event_init()

        # effect params
        # self._mod_samplingrate = 1.0
        # 0 < volume < 1
        self._mod_volume = 0.5

    def __event_init(self):
        self._event_pause.clear()
        self._event_stop.clear()

    __pa_lock = threading.Lock()

    def __playsound(self, wavfile, loop=False):
        if (wavfile == ""):
            logger.d('empty sound file.')
            return

        # open file
        logger.d('open file = {}'.format(wavfile))
        wf = wave.open(wavfile, 'rb')
        self.wfinfo = wf.getparams()
        self.show_wavinfo(self.wfinfo)
        try:
            with SoundPlayer.__pa_lock:
                p = pyaudio.PyAudio()
                s = p.open(format=p.get_format_from_width(self.wfinfo[1]),
                           channels=self.wfinfo[0],
                           rate=self.wfinfo[2],
                           output=True)

            # play stream
            input_data = wf.readframes(CHUNK)
            logger.d('started blocking sound play.')
            while len(input_data) > 0:
                if self.__ctrl_sound():
                    break
                s.write(self.__mod_sound(input_data))
                input_data = wf.readframes(CHUNK)
                # loop
                if loop and len(input_data) == 0:
                    wf.rewind()
                    input_data = wf.readframes(CHUNK)

        finally:
            # close stream
            with SoundPlayer.__pa_lock:
                s.stop_stream()
                s.close()
                wf.close()
                p.terminate()
            logger.d('finished sound play.')

    def __ctrl_sound(self):
        is_brake = False

        # stop action
        if self._event_stop.is_set():
            logger.d('stop sound.')
            is_brake = True
        # pause action
        if self._event_pause.is_set():
            logger.d('pause sound.')
            while self._event_pause.is_set():
                time.sleep(0.1)
                if self._event_stop.is_set():
                    # finish
                    break
            is_brake = False

        return is_brake

    def __mod_sound(self, input_data):
        data = fx.get_buffer(input_data, self.wfinfo[1])

        # mod sampling
        # if self._mod_samplingrate != 1.0:
        #     data = fx.resamplingrate(data,
        #                              self.wfinfo[2],
        #                              self.wfinfo[2] * self._mod_samplingrate)

        # mod volume
        if self._mod_volume != 0.5:
            data = fx.gain(data, self._mod_volume)
        return fx.set_buffer(data)

    def do_play(self, wavfile, loop=False):
        # clear event flags
        # self.__event_init()
        # threading
        threading.Thread(target=self.__playsound, args=(wavfile, loop,)) \
                 .start()

    def do_pause(self):
        self._event_pause.set()

    def do_resume(self):
        self._event_pause.clear()

    def do_stop(self):
        self._event_stop.set()
        self._event_pause.clear()

    # def set_samplingrate(self, rate):
    #     if rate > 0:
    #         self._mod_samplingrate = rate
    #     logger.d('set sampling rate = {}'.format(rate))

    def set_volume(self, val):
        if val < 0:
            val = 0
        elif val > 1:
            val = 1
        self._mod_volume = val
        logger.d('set volume = {}'.format(val))

    # def set_loop(self, val, id):
    #     self._loop = val
    #     logger.d('set loop play = {}'.format(val))


'''
def myhelp():
    print(u'これはサウンドプレイヤーです。')
    print(u'')
    print(u'Usage: ')
    print(u'  play (ファイル) : 指定のファイルを再生する')
    print(u'  pause           : 一時停止')
    print(u'  resume          : 再生を再開する')
    print(u'  stop            : 再生を停止する')
    print(u'  ')
    # print(u'  rate            : サンプリング周波数を変更する')
    print(u'  vol             : 音量を変更する(0 - 1.0、default:0.5)')
    print(u'  ')
    print(u'  help            : ヘルプを表示')
    print(u'  exit            : 終了する')


if __name__ == '__main__':
    # file = sys.argv[1]
    player = SoundPlayer()
    dicmd = {'play': player.do_play,
             'pause': player.do_pause,
             'resume': player.do_resume,
             'stop': player.do_stop,
             'rate': (lambda r: player.set_samplingrate(float(r))),
             'vol': (lambda r: player.set_volume(float(r))),
             'help': myhelp,
             'exit': sys.exit}
    # sys.stdout = codecs.getw_piter('utf_8')(sys.stdout)
    sys.stdout = codecs.getwriter('shift_jis')(sys.stdout)

    myhelp()
    while True:
        try:
            userinput = raw_input('audio interface >> ').lower()
        except KeyboardInterrupt:
            # ctrl + c
            dicmd['stop']()
            dicmd['exit']()
        logger.d('thread count = {}'.format(threading.active_count()))
        # enter only
        if len(userinput) == 0:
            continue

        cmds = userinput.split(' ')
        if cmds[0] not in dicmd:
            continue
        cmd = dicmd[cmds[0]]
        if len(cmds) > 1:
            cmd(cmds[1])
        else:
            cmd()
'''
