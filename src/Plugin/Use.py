#!/usr/bin/python

import G

from Utils import getkey
from Generic import Generic

# Use is the class that creates a first dummy object of something so that it's
# setup function gets called and setups global vars such as default values and
# syntax sugar entries.
class Use(Generic):
    def __init__(self):
        super(Use, self).__init__()
        self.init()
    
    # A Use Object creates this dummy object in post_upgrade phase.
    def post_upgrade(self):
        primary = getkey(self.arguments, 'primary')
        if not primary == '':
            G.info(''.join(['Creating a dummy object of type ', primary]))
            obj = Generic(
                    self.globalvars,
                    [''.join([primary,':'])] + self.lines[1:]
                    )
            obj.setup()
            G.debug('\n'.join(['DUMPING DUMMY OBJECT', obj.dump()]))
        else:
            G.critical(''.join('Missing argument: primary'))
        self.removed = True # This object's purpose is done
    
    def get_text():
        return ''
