import sys
import traceback
import threading
from flask import Flask, request
import logger

class FlaskOnThread(threading.Thread):

    def __init__(self, flask_app, host='0.0.0.0', port=5000):
        super(FlaskOnThread, self).__init__()
        if not isinstance(flask_app, Flask):
            raise ValueError(Flask)
        self.flask_app = flask_app
        self.host = host
        self.port = port
        self.errors = []
        self.lock = threading.Lock()

    
    def run(self):
        try:
            logger.i("flask server has started. host:{0}, port:{1}".format(self.host, self.port))
            self.flask_app.run(
                debug=False,
                host=self.host,
                port=int(self.port)
            )
        except Exception as e:
            logger.e("Unexpected error:" + str(sys.exc_info()[0]))
            logger.e(traceback.format_exc())
            self.lock.acquire()            
            self.errors.append(e)
            self.lock.release()            

    def has_error(self):
        try:
            self.lock.acquire()            
            return len(self.errors)
        finally:
            self.lock.release()            

    def check_error(self):
        if self.has_error():
            raise self.errors[-1]
        
    def shut_down(self):
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()