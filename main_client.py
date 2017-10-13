# coding: UTF-8
import urllib2
from optparse import OptionParser
from libled.led_run_loop import LedRunLoop

class LedHttpClient(LedRunLoop):

    def __init__(self, parser, host, student):
        super(LedHttpClient, self).__init__(parser)
        self.host = host
        self.student = student

    def on_finish(self):
        pass

    def on_keyboard_interrupt(self):
        pass

    def on_exception_at_runloop(self, exception):
        if isinstance(exception, urllib2.HTTPError):
            print("Server may not be running: " + str(exception))
            return LedRunLoop.CONTINUE
        else:
            return LedRunLoop.EXIT

    def read_data(self):
        print('Press Enter...')
        _ = raw_input('>>> ')

        content_url = "http://" + self.host + "/api/content/" + str(self.student)
        return urllib2.urlopen(content_url).read()
 

    def on_pre_exec_runloop(self):
        pass

    def on_post_exec_runloop(self):
        pass


parser = OptionParser()
parser.add_option("-H", "--host",
                action="store", type="string", dest="host", 
                help="(required) host name (or ip) with port number of content server.")

parser.add_option("-n", "--student",
                action="store", type="string", dest="student", 
                help="(required) student no.")

options, _ = parser.parse_args()

if options.host and options.student:
    LedHttpClient(parser, options.host, options.student).run()
else:
    print("Error!: you have to specify options (-H (host name or ip with port) and -n (student number)")
