#!/usr/bin/env python

import base64, re

import G

from Utils import safe_link, getkey, varsub
from Utils import counter_create, counter_tick
from Generic import Generic

class Table(Generic):
    def __init__(self):
        super(Figure, self).__init__()
        self.init()

    def pre_process(self):
        self.needs_rerun = not self.needs_rerun 

        self.arguments['caption'] = getkey(self.arguments, 'caption', u'')
        self.localvars['title'] = getkey(self.arguments, 'caption', 'Untitled')

        if not getkey(self.arguments, 'file'):
            self.arguments['file'] = getkey(self.arguments, 'primary', u'') 
        filename = getkey(self.arguments, 'file')
        if not getkey(self.arguments, 'mode'):
            self.arguments['mode'] = getkey(self.globalvars.get('$Table', {}), 'mode',u'')
        mode = self.arguments['mode']
        self.localvars['headers'] = self.arguments.get('headers', False) or self.globalvars.get('$Table', {}).get('headers', 'yes')

        # Store title to TOT (Table of Tables)
        self.localvars['safe_title'] = 'table_'+safe_link(
                getkey(self.localvars,'title','untitled'))
        counter_tick(self.globalvars['$Counters'], 'table')
                     
        tocitem = { 'safe_title': self.localvars['safe_title'],
                    'link': '#%s' % self.localvars['safe_title'],
                    'title': getkey(self.localvars, 'title', 'Untitled'),
                    'level': 1,
                    'section': '!!toc1!!',
                    'numbering': varsub('%numberingtable%', [self.globalvars], [])
                  }
        self.localvars['numbering'] = tocitem['numbering']

        self.globalvars['$TOT'].append(tocitem)

        data = ''
        # Caching
        # TODO This caching should be stored in css instead as well
        if mode == 'normal':
            try:
                f = open(filename, 'r')
                data = f.read()
            except IOError:
                G.error(''.join(['The image file "',filename,'" could not be opened.']))
        elif mode == 'inline':
            data = self.content 

        if not 'width' in self.arguments and 'width' in self.globalvars.get('$Table', []):
            self.localvars['width'] = self.globalvars.get('$Table', []).get('width')

        splitter = re.compile("[ ]{2,}")
        rows = []
        for (nr, line) in enumerate(data.splitlines()):
            if nr == 0:
                pass
            elif nr == 1 and self.localvars.get('headers', False) in ('1', 'yes'):
                headers = []
                for header in splitter.split(line):
                    headers.append({'text': header})
                self.localvars['$Headers'] = headers
            else:
                cells = []
                for cell in splitter.split(line):
                    cells.append({'text': cell})
                rows.append({'$Cells': cells})
        self.localvars['$Rows'] = rows
            
    def setup(self):
        if '$Table' in self.globalvars:
            G.info("Table already setup.")
            return
        G.info("Setting up Table.")
        # Set defaults
        self.globalvars['$Table'] = {
            'mode': 'inline',
            'headers': 'yes',
                }
        # Init TOT (Table of Tables)  list
        self.globalvars['$TOT'] = []
        counter_create(self.globalvars['$Counters'], 'table', None)
        self.globalvars['numberingtable'] = '!!table!!.'
