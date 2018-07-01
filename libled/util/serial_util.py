import sys
import glob

def enum_serial_posts():
    if sys.platform.startswith('win'):
        return ['COM%s' % (i + 1) for i in range(10)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        return glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        return glob.glob('/dev/tty.*')

    else:
        raise EnvironmentError('Unsupported platform')
