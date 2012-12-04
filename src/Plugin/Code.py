#!/usr/bin/python

import G

from Utils import getkey, varsub
from Generic import Generic

from Utils import counter_create, counter_tick

try:
    from pygments import highlight
    from pygments.lexers import (get_lexer_by_name, get_lexer_for_filename, get_lexer_for_mimetype)
    from pygments.lexers import guess_lexer, guess_lexer_for_filename
    from pygments.formatters import HtmlFormatter
    from pygments.util import ClassNotFound
except ImportError:
    have_pygment = False
    G.critical("Could not load Pygment.")
else:
    have_pygment = True
    G.info("Loaded Pygment.")
    
class Code(Generic):
    def __init__(self):
        super(Code, self).__init__()
        self.init()
 
    def pre_process(self):
        if not 'language' in self.arguments:
            self.arguments['language'] = getkey(self.arguments, 'primary', u'?') 
        self.arguments['caption'] = getkey(self.arguments, 'caption', u'')
        self.arguments['linenumbers'] = getkey(self.arguments, 'linenumbers', u'no')
        self.arguments['highlight'] = getkey(self.arguments, 'highlight', '')
        self.arguments['wrap'] = getkey(self.arguments, 'wrap', 'yes')
 
        self.localvars['id'] = 'code%i' % G.getid()
        
        if not self.content:
            G.warn("Empty Code object at %s +%d! Perhaps it starts with xxxx: Then add a - separator line before content." % (self.filepath, self.lineno))
            return
        
        if have_pygment:
            if getkey(self.arguments, 'language', u'') == u'':
                lexer = guess_lexer(self.content)
            else:
                try:
                    lexer = get_lexer_by_name(getkey(self.arguments, 'language', 'text'))
                except ClassNotFound:
                    G.error('Cound not find class %s at %s +%d' % (getkey(self.arguments, 'language', 'text'), self.filepath, self.lineno))
                    lexer = get_lexer_by_name('text')
            G.debug(u''.join(['Lexer is ',str(lexer)]))
 
            linenumbers = True if self.arguments['linenumbers'] == 'yes' else False
            wrap = True if self.arguments['wrap'] == 'yes' else False
            highlight_lines = self.arguments['highlight'].split(',')
 
            formatter = HtmlFormatter(
                linenos = linenumbers,
                nowrap = not wrap,
                hl_lines = highlight_lines
            )
 
            self.localvars['code'] = unicode(highlight(unicode(self.content), lexer, formatter))
        else:
            G.debug('No highlighting done')
            self.localvars['code'] = u'\n'.join(['<pre>',unicode(self.content),'</pre>'])
 
        self.script = unicode(getkey(self.globalvars, '$Templates.Code.script', u''))
        self.script = varsub(self.script, 
                           [self.localvars,
                           self.arguments,
                           self.globalvars],
                           getkey(self.globalvars, '$Templates', False),
                           recursive=getkey(self.arguments, 'substitute', 'yes') != 'no')
