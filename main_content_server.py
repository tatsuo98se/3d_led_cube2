from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/api/content/<content_id>')
def get_content(content_id):
	return open("./log/order_history/"+ str(content_id) + ".log").read()

