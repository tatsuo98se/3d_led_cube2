import urllib2
import json
import logger
import hw_controller_manager as hwc

def get_data_as_json(defaults=None):

    data =  hwc.HwControllerManager.get_data()
    if data is not None and data != '':
        return data
    else:
        return defaults
