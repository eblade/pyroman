#!/usr/bin/python

import os
import sys
import io

sys.path.append('Plugin')

DEBUG = 10
INFO = 20
WARNING = 30
ERROR = 40
CRITICAL = 50

levels = {
        INFO: u'[INFO]',
        DEBUG: u'[DEBUG]',
        WARNING: u'[WARNING]',
        ERROR: u'[ERROR]',
        CRITICAL: u'[CRITICAL]',
        }

loglevel = DEBUG

# Ensure there is a logging directory
if not os.path.isdir(os.getenv('HOME')+'/.pyroman'):
    os.mkdir(os.getenv('HOME')+'/.pyroman')
if not os.path.isdir(os.getenv('HOME')+'/.pyroman/logs'):
    os.mkdir(os.getenv('HOME')+'/.pyroman/logs')

template_dir = ''.join([os.getenv('HOME'),'/.pyroman/templates/'])
log_dir = ''.join([os.getenv('HOME'),'/.pyroman/logs/'])

logfile = io.open(log_dir+'/pyroman.log','w')

# Set standard start lines (for standard setup of documents)
first_lines = {}
first_lines['html'] = [u'Input: common\n',u'\n',u'Input: html\n',u'\n']
first_lines['rst'] = [u'Input: common\n',u'\n',u'Input: rst\n',u'\n']
first_lines['no'] = [u'Input: common\n', u'\n' ]

def getid():
    getid.id += 1
    return getid.id
getid.id = 0

def getSafeLinkId():
    getSafeLinkId.id += 1
    return getSafeLinkId.id
getSafeLinkId.id = 0

def log(frame, level, message):
    caller = unicode(frame.f_back.f_globals['__name__'])
    message = unicode(message)
    if level >= loglevel:
        logfile.write(' '.join([levels[level],caller,u'::',message,'\n']))

def debug(s):
    frame = sys._current_frames().values()[0]
    log(frame, DEBUG, s)

def info(s):
    frame = sys._current_frames().values()[0]
    log(frame, INFO, s)

def warning(s):
    frame = sys._current_frames().values()[0]
    log(frame, WARNING, s)

def warn(s):
    frame = sys._current_frames().values()[0]
    log(frame, WARNING, s)
    print "WARNING:", s

def error(s):
    frame = sys._current_frames().values()[0]
    log(frame, ERROR, s)
    print "ERROR:", s

def critical(s):
    frame = sys._current_frames().values()[0]
    log(frame, CRITICAL, s)
    print "CRITICAL:", s

info("Initialisation of G is done")

def close_log():
    logfile.close()
