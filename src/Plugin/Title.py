#!/usr/bin/python

import G

from Utils import getkey
from Generic import Generic

class Title(Generic):
    def __init__(self):
        super(Title, self).__init__()
        self.init()

    def pre_process(self):
        # Export variables
        if (u'title' in self.arguments.keys() or not u'title' in self.globalvars.keys()):
            self.globalvars['title'] = getkey(self.arguments, u'title', 'Doc') 
        if (u'subtitle' in self.arguments.keys() or not u'subtitle' in self.globalvars.keys()):
            self.globalvars[u'subtitle'] = getkey(self.arguments, u'subtitle')
        if (u'author' in self.arguments.keys() or not u'author' in self.globalvars.keys()):
            self.globalvars[u'author'] = getkey(self.arguments, u'author')
        if (u'date' in self.arguments.keys() or not u'date' in self.globalvars.keys()):
            self.globalvars[u'date'] = getkey(self.arguments, u'date', getkey(self.globalvars,u'date',''))
