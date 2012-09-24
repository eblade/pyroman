#!/usr/bin/env python

import G

from Generic import Generic
class Dot(Generic):
    def __init__(self):
        super(Dot, self).__init__()
        self.init()

    def pre_process(self):
        # This function should run Dot on the contents and then
        # upgrade this to a Figure.
        pass
