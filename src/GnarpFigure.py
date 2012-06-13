#!/usr/bin/python

import base64

import G

from GnarpUtils import getkey
from GnarpGeneric import Generic

class Figure(Generic):
    def __init__(self):
        super(GnarpObject, self).__init__()
        self.init()

    def pre_process(self):
        if not getkey(self.arguments, 'file'):
            self.arguments['file'] = getkey(self.arguments, 'primary', u'') 
        filename = getkey(self.arguments, 'file')
        if not getkey(self.arguments, 'mode'):
            self.arguments['mode'] = getkey(self.globalvars['$Figure'], 'mode',u'')

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
        elif extension == 'jpg' or extensiont == 'jpeg':
            self.localvars['format'] = 'jpeg'
        elif extension == 'gif':
            self.localvars['format'] = 'gif'
        elif extension == 'svg':
            self.localvars['format'] = 'svg'
        else:
            G.warn('Unknown image format: '+extension)
            self.localvars['format'] = extension 


    def setup(self):
        if '$Figure' in self.globalvars:
            G.info("Heading already setup.")
            return
        G.info("Setting up Figure.")
        # Set defaults
        self.globalvars['$Figure'] = {
                'mode': 'base64',
                }
        self.globalvars['$Base64Data'] = {}
