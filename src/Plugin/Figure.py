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
        if not filename:
            mode = 'inline'
        else:
            mode = 'normal'
        self.arguments['caption'] = getkey(self.arguments, 'caption', u'')
        self.localvars['title'] = getkey(self.arguments, 'caption', 'Untitled')

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

        parts = filename.split('.')
        extension = parts[-1].lower()
        if self.arguments.get('format', False):
            self.localvars['format'] = self.arguments.get('format') 
        elif extension == 'png':
            self.localvars['format'] = 'image/png;base64'
        elif extension == 'jpg' or extension == 'jpeg':
            self.localvars['format'] = 'image/jpeg;base64'
        elif extension == 'gif':
            self.localvars['format'] = 'image/gif;base64'
        elif extension == 'svg':
            self.localvars['format'] = 'image/svg+xml;base64'
        else:
            G.warn('Unknown image format: '+extension)
            self.localvars['format'] = extension 

        indata = ''
        if not filename in getkey(self.globalvars,'$Base64Data',{}):
            # Caching
            # TODO This caching should be stored in css instead as well
            if mode == 'normal':
                try:
                    f = open(filename, 'r')
                    indata = f.read()
                except IOError:
                    G.error(''.join(['The image file "',filename,'" could not be opened.']))
            elif mode == 'inline':
                filename = self.localvars.get('safe_title')
                if not filename in getkey(self.globalvars,'$Base64Data',{}):
                    indata = self.content 
            if 'base64' in self.localvars.get('format'):
                data = base64.b64encode(indata)
            else:
                data = ''.join([s for s in indata.splitlines() if s])
            self.globalvars['$Base64Data'][filename] = data

        self.localvars['data'] = self.globalvars['$Base64Data'][filename]

        if not 'width' in self.arguments:
            self.localvars['width'] = self.globalvars['$Figure']['width']


    def setup(self):
        if '$Figure' in self.globalvars:
            G.info("Figure already setup.")
            return
        G.info("Setting up Figure.")
        # Set defaults
        self.globalvars['$Figure'] = {
                'mode': 'base64',
                'width': '100%',
                }
        self.globalvars['$Base64Data'] = {}
        # Init TOF list
        self.globalvars['$TOF'] = []
        counter_create(self.globalvars['$Counters'], 'figure', None)
        self.globalvars['numberingfigure'] = '!!figure!!.'
