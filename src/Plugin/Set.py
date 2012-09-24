#!/usr/bin/python

import G

from Utils import getkey
from Generic import Generic

class Set(Generic):
    def __init__(self):
        super(Set, self).__init__()
        self.init()

    def pre_process(self):
        # Export variables
        G.info('Exporting global vars')
        for varname in self.arguments.keys():
            G.debug(''.join(['Preparing "',varname,'" = "',self.arguments[varname],'".']))
            if (varname != 'primary' and not (self.arguments['primary'] == 'no-overwrite' and varname in self.globalvars.keys())):
                G.debug(''.join(['Copying "',varname,'" = "',self.arguments[varname],'" to globals.']))
                self.globalvars[varname] = self.arguments[varname]
