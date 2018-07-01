import threading
from flask import Flask, request

class FlaskOnThread(threading.Thread):

    def __init__(self, flask_app, host='0.0.0.0', port=5301):
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
            self.flask_app.run(
                debug=False,
                host=self.host,
                port=int(self.port)
            )
        except Exception as e:
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