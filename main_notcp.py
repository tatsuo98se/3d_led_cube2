# coding: UTF-8
from led_framework import LedFramework
import threading
from Queue import Queue
import time
import traceback
import json

message = Queue()


def message_receive_loop(q):
    led_framework = LedFramework()

    try:
        while True:
            print('Please input order...')
            input_word = raw_input('>>> ')

            line = input_word
            if not line:
                continue

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
                    print('invalid order: ' + str(orders))
                    continue

                led_framework.abort()
                q.put([led_framework.show, dic_orders])
    except:
        pass
    finally:
        print('finished.')


th = threading.Thread(name="message_receive_loop",
                      target=message_receive_loop,
                      args=(message, ))
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

except:
    print('Unexpected error: ', sys.exc_info()[0])
    print(traceback.format_exc())
    raise

finally:
    th.join()
    print('finished.')
