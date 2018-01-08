# coding: UTF-8
import urllib2
from optparse import OptionParser
import traceback
import sys

parser = OptionParser()
parser.add_option("-H", "--host",
                action="store", type="string", dest="host", 
                help="(required) host name (or ip) with port number of content server.")

options, _ = parser.parse_args()

if not options.host:
    print("Error!: you have to specify options (-H (host name or ip with port) and -n (student number)")
    exit

try:
    while True:
        print('Press Enter...')
        order = raw_input('>>> ').strip()

        req = None
        if order.startswith('show:'):
            json = order[5:]
            req = urllib2.Request("http://" + options.host + "/api/show")
            req.add_header('Content-Type', 'application/json')
            urllib2.urlopen(req, json)
        elif order.startswith('abort'):
            req = urllib2.Request("http://" + options.host + "/api/abort")
            urllib2.urlopen(req, '')

except KeyboardInterrupt:
    print('keybord Ctrl+C')
    self.on_keyboard_interrupt()
except:
    print("Unexpected error:", sys.exc_info()[0])
    print(traceback.format_exc())
    raise
finally:
    pass

