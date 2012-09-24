#!/usr/bin/env python

from Generic import Generic
from Utils import getkey

class Link(Generic):
    def __init__(self):
        super(Link, self).__init__()
        self.init()

    def pre_process(self):
        self.localvars['url'] = getkey(self.arguments,'primary','about:blank');
        self.localvars['title'] = getkey(self.arguments,'title',False);
        if not self.localvars['title']:
            self.localvars['title'] = self.localvars['url']
