# coding: UTF-8
from libled.led_run_loop import LedRunLoop
import socket

class LedTcpServer(LedRunLoop):

    def __init__(self):
        super(LedTcpServer, self).__init__()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("localhost", 80))
        hostname = s.getsockname()[0]
        s.close()
        print(hostname)
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.bind((hostname, 20000))
        self.serversocket.listen(1)
        self.sock = None
        self.sf = None


    def on_finish(self):
        self.serversocket.shutdown(socket.SHUT_RDWR)
        self.serversocket.close()

    def on_keyboard_interrupt(self):
        self.sf.close()
        self.sock.close()

    def on_exception_at_runloop(self, exception):
        if isinstance(exception, socket.timeout):
            return LedRunLoop.CONTINUE
        else:
            return LedRunLoop.EXIT

    def read_data(self):
        print('waiting data...')
        return self.sf.readline()

    def on_pre_exec_runloop(self):
        print('Waiting for connections...')
        self.sock, client_address = self.serversocket.accept() #接続されればデータを格納

        # ファイルオブジェクトを作成
        self.sf = self.sock.makefile()

    def on_post_exec_runloop(self):
        self.sock.close()
        print('disconnected.')

LedTcpServer().run()
