#!/usr/bin/python

import G

from GnarpUtils import SyntaxSugarDefinition, getkey
from GnarpGeneric import Generic

class SyntaxSugar(Generic):
    def __init__(self):
        super(GnarpObject, self).__init__()
        self.init()
    
    # An Input Object must load all subobjects so that they can be included
    # in the main object list.
    def post_upgrade(self):
        G.info(''.join(['Doing post upgrade when globalvars = ',str(self.globalvars)]))
        G.info(''.join(['Content -> output will be: ',self.content]))
        ss = SyntaxSugarDefinition(
                getkey(self.arguments, 'pattern'),
                getkey(self.arguments, 'params').split(','),
                self.content
                )
        if not ss.broken:
            self.globalvars['$SyntaxSugar'].append(ss)
            G.info('Added SyntaxSugar.')
        else:
            G.warn('SyntaxSugar was broken.')
    
    def get_text():
        return ''
