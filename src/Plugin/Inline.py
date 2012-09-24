#!/usr/bin/python

import G

from Utils import getkey
from Generic import Generic

class Inline(Generic):
    def __init__(self):
        super(Inline, self).__init__()
        self.init()
    
    def post_upgrade(self):
        # I am not sure this is needed, they can be treated as normal objects,
        # as long as they possible to look up.
        # Register me as subprocessor
        G.info('Registering myself as inline subprocessor')
        sp = getkey(self.globalvars, '$Subprocessors', [])
        sp.append(self)
        self.globalvars['$Subprocessors'] = sp
        self.localvars['$Accepts'] = ['Paragraph'] # is this the right place?
        return
    
    def process(self):
        pass

    def run(self, _object):
        return []
        # FIXME subprocess code here
