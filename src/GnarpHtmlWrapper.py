#!/usr/bin/python

import G

from GnarpUtils import getkey
from GnarpGeneric import Generic

class HtmlWrapper(Generic):
    def __init__(self):
        super(GnarpObject, self).__init__()
        self.init()
    
    def post_upgrade(self):
        # Register me as wrapper
        G.info("Registering wrapper")
        self.globalvars['$Wrapper'] = self
        return
    
    ## @fn process
    #
    # Processes the template with data from the hashes. Builds a text representation
    # of the object using the templates.
    def process(self):
        template_name = getkey(self.arguments, 'template', self.object_name)
        template = getkey(self.globalvars['$Templates'], template_name)
        self.body = getkey(template, 'wrapper')
        self.pre_process()
        # Insert localvars
        for k in self.localvars:
            G.debug(''.join(['Replacing localvar: ',str(k),'.']))
            self.body = self.body.replace(''.join(['%',str(k),'%']),unicode(self.localvars[k])) 
        # Insert arguments
        for k in self.arguments:
            G.debug(''.join(['Replacing argument: ',str(k),'.']))
            self.body = self.body.replace(''.join(['%',str(k),'%']),unicode(self.arguments[k])) 
        # Insert globalvars
        for k in self.globalvars:
            if not k[0] == '$': # non-string start with $
                G.debug(''.join(['Replacing globalvar: ',str(k),'.']))
                self.body = self.body.replace(''.join(['%',str(k),'%']),unicode(self.globalvars[k])) 
        # Insert content
        G.debug(''.join(['Calculated body: ', self.body]))
