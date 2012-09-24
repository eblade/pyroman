#!/usr/bin/env python

import base64

import G

from Utils import safe_link, getkey, varsub
from Utils import counter_create, counter_tick
from Generic import Generic

class Figure(Generic):
    def __init__(self):
        super(Figure, self).__init__()
        self.init()

    def pre_process(self):
        if not getkey(self.arguments, 'file'):
            self.arguments['file'] = getkey(self.arguments, 'primary', u'') 
        filename = getkey(self.arguments, 'file')
        if not getkey(self.arguments, 'mode'):
            self.arguments['mode'] = getkey(self.globalvars['$Figure'], 'mode',u'')
        self.arguments['caption'] = getkey(self.arguments, 'caption', u'')
        self.localvars['title'] = getkey(self.arguments, 'caption', 'Untitled')

        # Caching
        # TODO This caching should be stored in css instead as well
        if not filename in getkey(self.globalvars,'$Base64Data',{}):
            f = open(filename, 'r') # FIXME: TRY
            indata = f.read()
            data = base64.b64encode(indata)
            self.globalvars['$Base64Data'][filename] = data

        self.localvars['data'] = self.globalvars['$Base64Data'][filename]
        parts = filename.split('.')
        extension = parts[-1].lower()
        if extension == 'png':
            self.localvars['format'] = 'png'
        elif extension == 'jpg' or extension == 'jpeg':
            self.localvars['format'] = 'jpeg'
        elif extension == 'gif':
            self.localvars['format'] = 'gif'
        elif extension == 'svg':
            self.localvars['format'] = 'svg'
        else:
            G.warn('Unknown image format: '+extension)
            self.localvars['format'] = extension 

        # Store title to TOC
        self.localvars['safe_title'] = 'figure_'+safe_link(
                getkey(self.localvars,'title','untitled'))
        counter_tick(self.globalvars['$Counters'], 'figure')
                     
        tocitem = { 'safe_title': self.localvars['safe_title'],
                    'title': getkey(self.localvars, 'title', 'Untitled'),
                    'level': 1,
                    'section': '!!toc1!!',
                    'numbering': varsub('%numberingfigure%', [self.globalvars], [])
                  }
        self.localvars['numbering'] = tocitem['numbering']

        self.globalvars['$TOF'].append(tocitem)


    def setup(self):
        if '$Figure' in self.globalvars:
            G.info("Figure already setup.")
            return
        G.info("Setting up Figure.")
        # Set defaults
        self.globalvars['$Figure'] = {
                'mode': 'base64',
                }
        self.globalvars['$Base64Data'] = {}
        # Init TOF list
        self.globalvars['$TOF'] = []
        counter_create(self.globalvars['$Counters'], 'figure', None)
        self.globalvars['numberingfigure'] = '!!figure!!.'
