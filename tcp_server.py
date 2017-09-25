# coding: UTF-8
import sys
import traceback
import socket

# Hostnameを取るための仮接続
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("0.0.0.0", 80))
hostname = s.getsockname()[0]
s.close()
print(hostname)

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    serversocket.bind((hostname, 20000))
    serversocket.listen(1)

    while True:
        print('Waiting for connections...')
        sock, client_address = serversocket.accept() #接続されればデータを格納

        # ファイルオブジェクトを作成
        sf = sock.makefile()

        # 1行読み取る場合
        while True:
            line = sf.readline()
            if not line:
                break
            
            # 読み取った行を処理する
            print(line)

        sock.close()
        print('disconnected.')
except:
    print("Unexpected error:", sys.exc_info()[0])
    print(traceback.format_exc())
    raise
finally:
    serversocket.close()
    print('finish')
