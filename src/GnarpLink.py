#!/usr/bin/python

from GnarpGeneric import Generic
from GnarpUtils import getkey

class Link(Generic):
    def __init__(self):
        super(GnarpObject, self).__init__()
        self.init()

    def pre_process(self):
        self.localvars['url'] = getkey(self.arguments,'primary','about:blank');
        self.localvars['title'] = getkey(self.arguments,'title',False);
        if not self.localvars['title']:
            self.localvars['title'] = self.localvars['url']
