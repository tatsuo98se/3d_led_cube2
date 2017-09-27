# coding: UTF-8
from optparse import OptionParser
from libled.led_cube import *
import importlib
import os.path
from led_framework import LedFramework
import threading
from Queue import Queue
import time
import traceback
import socket
import json

# Hostnameを取るための仮接続
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("0.0.0.0", 80))
hostname = s.getsockname()[0]
s.close()
print(hostname)


parser = OptionParser()
parser.add_option("-d", "--dest",
                  action="store", type="string", dest="dest", 
                  help="(optional) ip address of destination device which connect to real 3d cube.")

(options, args) = parser.parse_args()

if options.dest != None:
    led.SetUrl(options.dest)

message = Queue()
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((hostname, 20000))
serversocket.listen(1)
sock = None
sf = None


def message_receive_loop(q):
    global sock
    global sf
    led_framework = LedFramework()

    try:
        while True:
            try:
                print('Waiting for connections...')
                sock, client_address = serversocket.accept() #接続されればデータを格納

                # ファイルオブジェクトを作成
                sf = sock.makefile()

                # 1行読み取る場合
                while True:
                    print('waiting data...')
                    line = sf.readline()
                    print('receive in thread: ' + line)
                    if not line:
                        break
                    
                    if line.startswith('abort'):
                        print('abort canvas')
                        led_framework.abort()
                    elif line.startswith('show:'):
                        print('show by orders')
                        orders = line[len('show:'):].strip()

                        dic_orders = None
                        try:
                            dic_orders = json.loads(orders)
                        except ValueError:
                            print('invalid order:' + str(orders))
                            continue
                        
                        led_framework.abort()
                        q.put([led_framework.show, {"led":led, "orders":dic_orders}])

                sock.close()
                print('disconnected.')

            except socket.timeout:
                continue

    except:
        print("Unexpected error:", sys.exc_info()[0])
        print(traceback.format_exc())
        raise
    finally:
        print('finish')


th = threading.Thread(name="message_receive_loop", target=message_receive_loop, args=(message,))
th.setDaemon(True)
th.start()

try:
    while True:
        if message.empty():
            time.sleep(0.1)
        else:
            msg = message.get()
            msg[0](msg[1])

except KeyboardInterrupt:
    print('keybord Ctrl+C')
    sf.close()
    sock.close()
except:
    print("Unexpected error:", sys.exc_info()[0])
    print(traceback.format_exc())
    raise
finally:
    serversocket.shutdown(socket.SHUT_RDWR)
    serversocket.close()
    th.join()
    print('finish')
