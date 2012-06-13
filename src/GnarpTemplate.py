#!/usr/bin/python

import G

from GnarpUtils import getkey
from GnarpGeneric import Generic

class Template(Generic):
    def __init__(self):
        super(GnarpObject, self).__init__()
        self.init()
    
    # The template object defines a template into the globalvars['$Templates'] dictionary.
    def post_upgrade(self):
        template = getkey(self.arguments, 'primary')
        G.info(''.join(['Reading template object ', template]))
        
        if not template in self.globalvars['$Templates']:
            self.globalvars['$Templates'][template] = {}

        output = getkey(self.arguments, 'output', getkey(self.globalvars, 'output', 'html'))
        place = getkey(self.arguments, 'place', 'body')

        if output == getkey(self.globalvars, 'output', 'html'):
            G.info(''.join(['Loading template object as ', template, '/', output, '/', place]))
            self.globalvars['$Templates'][template][place] = self.content

        self.removed = True

    def get_text():
        return ''
