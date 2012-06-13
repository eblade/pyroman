#!/usr/bin/python

import re

from GnarpUtils import getkey
from GnarpGeneric import Generic

class List(Generic):
    def __init__(self):
        super(GnarpObject, self).__init__()
        self.init()

    def pre_process(self):
        if not getkey(self.arguments, 'style'):
            self.arguments['style'] = getkey(self.arguments, 'primary', u'-') 

        bullet = '- '
        if self.arguments['style'] == u'-':
            bullet = '- '
        elif self.arguments['style'] == u'...':
            bullet = '...'
        
        items = []
        for line in self.content.split("\n"):
            re_def = '^(\*+) '
            m = re.match(re_def, line)
            if m:
                level = len(m.group(1))
                caption = unicode(line[level+1:].strip())
                items.append({'level': level, 'caption': caption, 'bullet': bullet})
            elif len(items): # broken lines should be appended to the last added item
                items[len(items)-1]['caption'] = ''.join([items[len(items)-1]['caption'], ' ', line.strip()])
        self.localvars['$Items'] = items 
