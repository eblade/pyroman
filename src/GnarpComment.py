#!/usr/bin/python

from GnarpGeneric import Generic
from GnarpUtils import getkey

class Comment(Generic):
    def __init__(self):
        super(GnarpObject, self).__init__()
        self.init()

    def pre_process(self):
        if getkey(self.globalvars, 'state', 'draft') == 'final':
            self.removed = True
