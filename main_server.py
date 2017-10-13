# coding: UTF-8
import os.path
import time
import threading
from Queue import Queue
from libled.led_run_loop import LedRunLoop
from flask import Flask
from flask import request

app = Flask(__name__)
q = Queue()

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/api/content/<content_id>')
def get_content(content_id):
    logfile = "./log/order_history/"+ str(content_id) + ".log"
    if os.path.isfile(logfile):
    	return open(logfile).read()
    else:
        return "(no contents)"


@app.route('/api/show', methods=['POST'])
def show():
    print('body:' + str(request.data))
    q.put('show:' + str(request.data))
    return ""

@app.route('/api/abort', methods=['POST'])
def abort():
    q.put('abort')
    return ""


class LedTcpServer(LedRunLoop):

    def __init__(self):
        super(LedTcpServer, self).__init__()

    def on_exception_at_runloop(self, exception):
        return LedRunLoop.EXIT

    def read_data(self):
        print("waiting data.")
        while True:
            if self.aborted:
                break

            if q.empty():
                time.sleep(0.1)
            else:
                return q.get()


class FlaskThread(threading.Thread):

    def __init__(self, app, host='0.0.0.0', port=5000):
        super(FlaskThread, self).__init__()
        self.app = app
        self.host = host
        self.port = port
    
    def run(self):
        self.app.run(
            debug=False,
            host=self.host,
            port=int(self.port)
        )
        

flask = FlaskThread(app)
flask.daemon = True
flask.start()

LedTcpServer().run()
