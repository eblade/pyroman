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
        G.info('Exporting title page vars')
        if ('title' in self.arguments.keys() or not 'title' in self.globalvars.keys()):
            self.globalvars['title'] = getkey(self.arguments, 'title', 'Doc') 
        if ('subtitle' in self.arguments.keys() or not 'subtitle' in self.globalvars.keys()):
            self.globalvars['subtitle'] = getkey(self.arguments, 'subtitle')
        if ('author' in self.arguments.keys() or not 'author' in self.globalvars.keys()):
            self.globalvars['author'] = getkey(self.arguments, 'author')
        if ('date' in self.arguments.keys() or not 'date' in self.globalvars.keys()):
            self.globalvars['date'] = getkey(self.arguments, 'date', getkey(self.globalvars,'date',''))
