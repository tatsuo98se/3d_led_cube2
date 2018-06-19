import datetime

def i(msg):
    log('INFO', msg)

def w(msg):
    log('WARN', msg)

def e(msg):
    log('ERR', msg)

def log(tag, msg):
    print("[{0}] {1}: {2}".format(tag, datetime.datetime.today(),  msg))