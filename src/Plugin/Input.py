#!/usr/bin/python

import os
import sys

import G

from Utils import getkey
from Generic import Generic
import Processor

class Input(Generic):
    def __init__(self):
        super(Input, self).__init__()
        self.init()
    
    # An Input Object must load all subobjects so that they can be included
    # in the main object list.
    def pre_process(self):
        G.debug(''.join(['Doing post upgrade when globalvars = ',str(self.globalvars)]))
        filename = getkey(self.arguments,'primary', False)
        if not filename:
            G.error('No filename specified, skipping Input')
            return
        G.info(''.join(['Inserting ', filename]))
        p = None
        if os.path.isfile(getkey(self.globalvars,'root')+filename):
            p = Processor.Processor(getkey(self.globalvars,'root'), filename, _is_main_file=False)
        if os.path.isfile(getkey(self.globalvars,'root')+'conf/'+filename):
            p = Processor.Processor(getkey(self.globalvars,'root')+'conf/', filename, _is_main_file=False)
        elif os.path.isfile(getkey(self.globalvars,'templatedir')+filename):
            p = Processor.Processor(getkey(self.globalvars,'templatedir'), filename, _is_main_file=False)
        elif os.path.isfile(G.template_dir+filename):
            p = Processor.Processor(G.template_dir, filename, _is_main_file=False)
        else:
            G.error('Could not find file requested by Input: '+filename)
            return

        # Use the uppermost globalvars dictionary
        p.globalvars = self.globalvars

        # Load the objects
        if p.init_file():
            p.load_objects()
            p.close_file()
        
        # Copy objects from the processor to the object
        self.sub_objects = p.objects
        G.debug(''.join(['Input objects are: ', p.get_objects_as_string()]))

        self.removed = True

    def get_text():
        return ''
