#!/usr/bin/python

from Generic import Generic
from Utils import pyroman2rst

class Paragraph(Generic):
    def __init__(self):
        super(Paragraph, self).__init__()
        self.init()

    def pre_process(self):
        self.needs_rerun = not self.needs_rerun 
        content, links = pyroman2rst(self.content, self.globalvars)
        self.localvars['rst_content'] = links + ('\n\n' if links else '') + content

        if not self.content:
            G.warn("Empty Paragraph object at %s +%d! Perhaps it starts with xxxx: Then add a - separator line before content." % (self.filepath, self.lineno))
            return
