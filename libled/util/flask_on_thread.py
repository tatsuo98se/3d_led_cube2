import threading
from flask import Flask

class FlaskOnThread(threading.Thread):

    def __init__(self, flask_app, host='0.0.0.0', port=5301):
        super(FlaskOnThread, self).__init__()
        if not isinstance(flask_app, Flask):
            raise ValueError(Flask)
        self.flask_app = flask_app
        self.host = host
        self.port = port
    
    def run(self):
        self.flask_app.run(
            debug=False,
            host=self.host,
            port=int(self.port)
        )
        
