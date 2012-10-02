#!/usr/bin/python

import re

from Utils import getkey
from Generic import Generic

class List(Generic):
    def __init__(self):
        super(List, self).__init__()
        self.init()

    def pre_process(self):
        if self.needs_rerun:
            self.needs_rerun = False
            return
        if not getkey(self.arguments, 'style'):
            self.arguments['style'] = getkey(self.arguments, 'primary', u'-') 

        bullet = '- '
        if self.arguments['style'] == u'-':
            bullet = '- '
        elif self.arguments['style'] == u'...':
            bullet = '...'
        
        if getkey(self.arguments, 'format', '') == 'snippet':
            if not 'bullet1' in self.arguments:
                self.arguments['bullet1'] = ''
            if not 'bullet2' in self.arguments:
                self.arguments['bullet2'] = ''
            if not 'bullet3' in self.arguments:
                self.arguments['bullet3'] = '__bullet1__'
            if not 'bullet4' in self.arguments:
                self.arguments['bullet4'] = '__bullet2__'

        # Defaults
        self.localvars['bullet1'] = getkey(self.arguments, 'bullet1', '__bullet1__') 
        self.localvars['bullet2'] = getkey(self.arguments, 'bullet2', '__bullet2__') 
        self.localvars['bullet3'] = getkey(self.arguments, 'bullet3', '__bullet3__') 
        self.localvars['bullet4'] = getkey(self.arguments, 'bullet4', '__bullet4__') 

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

        self.needs_rerun = not self.needs_rerun 
