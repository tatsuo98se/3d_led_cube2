import urllib2
import json
import logger
import hw_controller_manager as hwc

def get_data_as_json(defaults=None, enable_controller=True):

    if not enable_controller:
        return defaults

    data =  hwc.HwControllerManager.get_data()
    if data is not None and data != '':
        return data
    else:
        return defaults
