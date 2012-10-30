#!/usr/bin/python

import G

from Generic import Generic
from Utils import SyntaxSugarDefinition, safe_link, getkey, varsub
from Utils import counter_create, counter_tick

class Heading(Generic):
    def __init__(self):
        super(Heading, self).__init__()
        self.init()
    
    def pre_process(self):
        # Do heading and toc stuff here
        if self.arguments.has_key('level'):
            self.localvars['level'] = self.arguments['level']
        else:
            self.localvars['level'] = '2'
        G.debug(''.join(['Level set to ',self.localvars['level']]))
        
        if self.arguments.has_key('primary'):
            self.localvars['title'] = self.arguments['primary']
        G.debug(''.join(['Title set to ',self.localvars['title']]))
        
        # Store title to TOC
        if u'label' in self.arguments:
            self.localvars['safe_title'] = self.arguments[u'label']
            self.globalvars['$Labels'][self.arguments[u'label']] = {
                'id':  self.localvars['safe_title'],
                'caption': getkey(self.localvars,'title','title missing'),
            }
        else:
            self.localvars['safe_title'] = safe_link(
                getkey(self.localvars,'title','title missing'))
        counter_tick(self.globalvars['$Counters'],
                     ''.join(['toc',str(self.localvars['level'])]))
        tocitem = { 'safe_title': self.localvars['safe_title'],
                    'title': self.localvars['title'],
                    'level': self.localvars['level'],
                    'numbering': varsub(
                        ''.join(['%numbering',
                                 self.localvars['level'],
                                 '%']),
                        [self.globalvars],
                        [])
                  }
        self.localvars['numbering'] = tocitem['numbering']

        if (int(self.localvars['level']) <= 
            int(getkey(self.globalvars, 'toc_depth', 3))):
            self.globalvars['$TOC'].append(tocitem)
        

        return True

    def setup(self):
        if '$Heading' in self.globalvars:
            G.info("Heading already setup.")
            return
        G.info("Setting up Heading.")
        # Add SyntaxSugar
        # FIXME These could be more generalised
        self.globalvars['$SyntaxSugar'].append(SyntaxSugarDefinition('= ([\s\w\.\^\$\*\+\?\{\}\[\]\\\\\|\(\)\/@-]+?) =',
            ['title'], 
            'Heading: %title%\nlevel: 1'))
        self.globalvars['$SyntaxSugar'].append(SyntaxSugarDefinition('== ([\s\w\.\^\$\*\+\?\{\}\[\]\\\\\|\(\)\/@-]+?) ==',
            ['title'], 
            'Heading: %title%\nlevel: 2'))
        self.globalvars['$SyntaxSugar'].append(SyntaxSugarDefinition('=== ([\s\w\.\^\$\*\+\?\{\}\[\]\\\\\|\(\)\/@-]+?) ===',
            ['title'], 
            'Heading: %title%\nlevel: 3'))
        self.globalvars['$SyntaxSugar'].append(SyntaxSugarDefinition('==== ([\s\w\.\^\$\*\+\?\{\}\[\]\\\\\|\(\)\/@-]+?) ====',
            ['title'], 
            'Heading: %title%\nlevel: 4'))
        self.globalvars['$SyntaxSugar'].append(SyntaxSugarDefinition('===== ([\s\w\.\^\$\*\+\?\{\}\[\]\\\\\|\(\)\/@-]+?) =====',
            ['title'], 
            'Heading: %title%\nlevel: 5'))
        self.globalvars['$SyntaxSugar'].append(SyntaxSugarDefinition('====== ([\s\w\.\^\$\*\+\?\{\}\[\]\\\\\|\(\)\/@-]+?) ======',
            ['title'], 
            'Heading: %title%\nlevel: 6'))
        self.globalvars['$SyntaxSugar'].append(SyntaxSugarDefinition('======= ([\s\w\.\^\$\*\+\?\{\}\[\]\\\\\|\(\)\/@-]+?) =======',
            ['title'], 
            'Heading: %title%\nlevel: 7'))
        # Add SyntaxSugar that applies to Jira
        self.globalvars['$SyntaxSugar'].append(SyntaxSugarDefinition('h1. ([\s\w\.\^\$\*\+\?\{\}\[\]\\\\\|\(\)\/@-]+)',
            ['title'], 
            'Heading: %title%\nlevel: 1'))
        self.globalvars['$SyntaxSugar'].append(SyntaxSugarDefinition('h2. ([\s\w\.\^\$\*\+\?\{\}\[\]\\\\\|\(\)\/@-]+)',
            ['title'], 
            'Heading: %title%\nlevel: 2'))
        self.globalvars['$SyntaxSugar'].append(SyntaxSugarDefinition('h3. ([\s\w\.\^\$\*\+\?\{\}\[\]\\\\\|\(\)\/@-]+)',
            ['title'], 
            'Heading: %title%\nlevel: 3'))
        self.globalvars['$SyntaxSugar'].append(SyntaxSugarDefinition('h4. ([\s\w\.\^\$\*\+\?\{\}\[\]\\\\\|\(\)\/@-]+)',
            ['title'], 
            'Heading: %title%\nlevel: 4'))
        self.globalvars['$SyntaxSugar'].append(SyntaxSugarDefinition('h5. ([\s\w\.\^\$\*\+\?\{\}\[\]\\\\\|\(\)\/@-]+)',
            ['title'], 
            'Heading: %title%\nlevel: 5'))
        self.globalvars['$SyntaxSugar'].append(SyntaxSugarDefinition('h6. ([\s\w\.\^\$\*\+\?\{\}\[\]\\\\\|\(\)\/@-]+)',
            ['title'], 
            'Heading: %title%\nlevel: 6'))
        self.globalvars['$SyntaxSugar'].append(SyntaxSugarDefinition('h7. ([\s\w\.\^\$\*\+\?\{\}\[\]\\\\\|\(\)\/@-]+)',
            ['title'], 
            'Heading: %title%\nlevel: 7'))
        # Set defaults
        self.globalvars['$Heading'] = {
                'level': '2',
                }
        # Init TOC list
        self.globalvars['$TOC'] = []
        # Init counters
        if not getkey(self.globalvars, '$Counters', False):
            self.globalvars['$Counters'] = {}
        counter_create(self.globalvars['$Counters'], 'toc1', 'toc2')
        counter_create(self.globalvars['$Counters'], 'toc2', 'toc3')
        counter_create(self.globalvars['$Counters'], 'toc3', 'toc4')
        counter_create(self.globalvars['$Counters'], 'toc4', 'toc5')
        counter_create(self.globalvars['$Counters'], 'toc5', 'toc6')
        counter_create(self.globalvars['$Counters'], 'toc6', 'toc7')
        counter_create(self.globalvars['$Counters'], 'toc7', None)
        self.globalvars['numbering1'] = '!!toc1!!.'
        self.globalvars['numbering2'] = '!!toc1!!.!!toc2!!.'
        self.globalvars['numbering3'] = '!!toc1!!.!!toc2!!.!!toc3!!.'
        self.globalvars['numbering4'] = '!!toc1!!.!!toc2!!.!!toc3!!.!!toc4!!.'
        self.globalvars['numbering5'] = '!!toc1!!.!!toc2!!.!!toc3!!.!!toc4!!.!!toc5!!.'
        self.globalvars['numbering6'] = '.!!toc6!!.'
        self.globalvars['numbering7'] = '.!!toc6!!.!!toc7!!.'
