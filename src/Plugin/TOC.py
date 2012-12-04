#!/usr/bin/python

from Generic import Generic
from Utils import SyntaxSugarDefinition, safe_link, getkey
import G

class TOC(Generic):
    def __init__(self):
        super(TOC, self).__init__()
        self.init()
    
    def pre_process(self):
        if (getkey(self.arguments, 'primary', '') == u'figures'):
            self.localvars['caption'] = u'__table_of_figures__'
            self.localvars['tocname'] = 'TOF'
        elif (getkey(self.arguments, 'primary', '') == u'tables'):
            self.localvars['caption'] = u'__table_of_tables__'
            self.localvars['tocname'] = 'TOT'
        elif (getkey(self.arguments, 'primary', '') == u'alt'):
            self.localvars['caption'] = u'__table_of_tables__'
            self.localvars['tocname'] = 'ALTTOC'
            self.globalvars['alt_toc_depth'] = getkey(self.arguments, 'depth', 3)
        else:
            self.localvars['caption'] = u'__table_of_contents__'
            self.localvars['tocname'] = 'TOC';
            self.globalvars['toc_depth'] = getkey(self.arguments, 'depth', 3)
        if self.arguments.get('caption',False):
            self.localvars['caption'] = self.arguments.get('caption',False);
        self.needs_rerun = not self.needs_rerun
        return True

    def setup(self):
        self.globalvars['toc_depth'] = '3'
        self.globalvars['alt_toc_depth'] = '3'
        return
