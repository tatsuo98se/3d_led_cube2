# coding: UTF-8
import json
from flask import request
from flask import Flask
from libled.util.hw_controller_manager import HwControllerManager

HwControllerManager.init()
app = Flask(__name__)

@app.route('/api/parameter')
def api_filter():
    return HwControllerManager.get_data()

app.run(debug=False, host='0.0.0.0', port=5303)

HwControllerManager.stop()