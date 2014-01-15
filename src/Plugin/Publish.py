#!/usr/bin/python

from subprocess import call

import G

from Utils import getkey
from Generic import Generic

class Publish(Generic):
    def __init__(self):
        super(Publish, self).__init__()
        self.init()

    def pre_process(self):
        if getkey(self.arguments, 'primary', '') != '':
            self.localvars['protocol'] = self.arguments['primary']

    def post_process(self):
        protocol = getkey(self.arguments, 'protocol', 'scp')
        G.debug(''.join(['Protocol for publishing is ', protocol]))
        if protocol == 'scp':
            src = getkey(self.globalvars, 'outputfile', False)
            dst = getkey(self.arguments, 'uri', False)
            if src and dst:
                G.info(''.join(['Doing scp from ',src,' to ',dst,'.']))
                call(['scp', src, dst])
                G.info('Done doing scp')
            else:
                G.error("You must specify a uri")

            # Also backup source if "src" param is specified
            src = getkey(self.globalvars, 'filename', False)
            dst = getkey(self.arguments, 'backup', False)
            if src and dst:
                G.info(''.join(['Doing scp from ',src,' to ',dst,'.']))
                call(['scp', src, dst])
                G.info('Done doing scp')
            else:
                G.info("Skipping source copy, missing src param")

        else:
            G.error("Only scp is currently supported")
