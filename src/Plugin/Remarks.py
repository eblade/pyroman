#!/usr/bin/python

from Generic import Generic

class Remarks(Generic):
    def __init__(self):
        super(Remarks, self).__init__()
        self.init()
    
    def pre_process(self):
        self.needs_rerun = not self.needs_rerun 
