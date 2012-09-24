#!/usr/bin/python

from Generic import Generic
from Utils import getkey

class Comment(Generic):
    def __init__(self):
        super(Comment, self).__init__()
        self.init()

    def pre_process(self):
        if getkey(self.globalvars, 'state', 'draft') == 'final':
            self.removed = True
