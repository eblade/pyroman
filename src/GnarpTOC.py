#!/usr/bin/python

from GnarpGeneric import Generic
from GnarpUtils import SyntaxSugarDefinition, safe_link, getkey

class TOC(Generic):
    def __init__(self):
        super(GnarpObject, self).__init__()
        self.init()
    
    def pre_process(self):
        if not getkey(self.arguments, 'caption',False):
            self.localvars['caption'] = getkey(self.arguments,'primary','Table of Contents');
        self.globalvars['toc_depth'] = getkey(self.arguments, 'depth', 3)
        self.needs_rerun = not self.needs_rerun
        return True

    def setup(self):
        self.globalvars['toc_depth'] = '3'
        return
