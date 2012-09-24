#!/usr/bin/env python

import G

from Utils import getkey
from Generic import Generic

class Translate(Generic):
    def __init__(self):
        super(Translate, self).__init__()
        self.init()

    def pre_process(self):
        _from = getkey(self.arguments, 'primary', False)
        _to = getkey(self.arguments, 'to', False)
        _lang = getkey(self.arguments, 'language', 'en')
        if (not _from and _to):
            G.error('Translate must have both from and to arguments')
            return
        if (not _lang in getkey(self.globalvars, '$i18n', {})):
            self.globalvars['$i18n'][_lang] = {_from: _to}
        else:
            self.globalvars['$i18n'][_lang][_from] = _to
    
    def setup(self):
        if '$i18n' in self.globalvars:
            G.info("Translate already setup.")
            return
        G.info("Setting up Translate.")
        self.globalvars['$i18n'] = {}
