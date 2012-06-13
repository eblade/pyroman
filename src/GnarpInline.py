#!/usr/bin/python

import G

from GnarpUtils import getkey
from GnarpGeneric import Generic

class Inline(Generic):
    def __init__(self):
        super(GnarpObject, self).__init__()
        self.init()
    
    def post_upgrade(self):
        # Register me as wrapper
        G.info('Registering myself as inline subprocessor')
        sp = getkey(self.globalvars, '$Subprocessors', [])
        sp.append(self)
        self.globalvars('$Subprocessors') = sp
        self.localvars('$Accepts') = ['Paragraph']
        return
    
    def process(self):
        pass

    def run(self, _object):
        return []
        # FIXME subprocess code here
