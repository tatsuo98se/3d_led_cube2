import urllib2
import json
import logger


def get_data_as_json(defaults=None):
    try:
        response = urllib2.urlopen('http://localhost:5303/api/parameter')
        return json.loads(response.read())
    except:
        return defaults
