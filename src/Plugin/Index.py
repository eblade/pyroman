#!/usr/bin/python

import os
import sys

import G

from Utils import getkey, counter_create, counter_tick, varsub
from Generic import Generic
import Processor

class Index(Generic):
    def __init__(self):
        super(Index, self).__init__()
        self.init()
        self.globalvars
    
    # An Index Object loads all other files in the given folder and extracts their
    # TOC and comments and adds that to the local TOC.
    #
    # All files must be in the same folder, and preferably execute this command in
    # that same folder as well. The sub documents should have a TOC object.
    def pre_process(self):
        root_path = self.globalvars.get('root') or '.'
        self_filename = self.filepath.replace(root_path, '')
        exclude_string = ','.join([self.arguments.get('exclude', ''), self_filename])
        exclude_files = exclude_string.split(',')
        files = self.arguments.get(u'startwith', '').split(',')

        listed_files = os.listdir(root_path)
        listed_files.sort()
        for path in listed_files:
            if not path in files:
                files.append(path)
        
        remarks = []
        for path in files:
            if os.path.isfile(os.path.join( root_path, path)) and path not in exclude_string and not path.startswith('.'):
                G.info('Reading file %s' % path)

                # Load file (locally on its own)
                p = Processor.Processor(getkey(self.globalvars,'root'), path, 'no', True, '%s.html' % path) # make them think they are main
                #p = Processor('', filename, 'html', True, outfile)
                if p.init_file():
                    p.load_objects()
                    p.close_file()
                else:
                    G.error('Skipping file "%s"' % path)
                    continue
                
                # Filter out objects we need
                needed_objects = []
                comment_objects = []
                doctitle = 'no title object found'
                for obj in p.objects:
                    if obj.object_name in ('Paragraph', 'Title', 'Input', 'Use', 'Template','Heading', 'TOC'):
                        needed_objects.append(obj)
                        if obj.object_name == 'Title':
                            doctitle = obj.arguments.get(u'title', 'wtf')
                    if obj.object_name == 'Comment' or obj.content.startswith("\nTODO") or obj.content.startswith("TODO"):
                        if not obj.arguments.get('state', False):
                            if obj.object_name == 'Comment':
                                obj.arguments['state'] = 'warning'
                            else:
                                obj.arguments['state'] = 'critical'
                        comment_objects.append(obj)

                p.objects = needed_objects
                p.preprocess_objects()
                p.process_objects_for_syntax_sugar()
                p.process_object_queue()

                # Take index comment objects
                for obj in comment_objects:
                    remarks.append({
                        'filename': obj.filepath,
                        'linenumber': obj.lineno,
                        'object_type': obj.object_name,
                        'note': obj.content,
                        'state': obj.arguments.get('state'),
                    })

                # Add main TOC item
                counter_tick(self.globalvars['$Counters'],
                             ''.join(['toc',str(1)]))
                tocitem = { 'safe_title': path,
                            'link': '%s.html' % path,
                            'title': p.globalvars.get('title', doctitle),
                            'level': 1,
                            'numbering': varsub(
                                ''.join(['%indexnumbering',
                                         str(1),
                                         '%']),
                                [self.globalvars],
                                [])
                          }
                self.globalvars['$TOC'].append(dict(tocitem))
                self.globalvars['$ALTTOC'].append(dict(tocitem))

                # Extract Headings from TOC
                toc = p.globalvars.get('$TOC', False)
                if not toc:
                    G.error('The file "%s" did not have any TOC' % path)
                    continue

                for entry in toc:
                    level = entry.get('level', False)
                    if not level:
                        G.error('level missing for some entry in file "%s"' % path)
                        continue
                    level = int(level) + 1
                    safe_title = entry.get('safe_title', False)
                    if not safe_title:
                        G.error('safe_title missing for some entry in file "%s"' % path)
                        continue
                    title = entry.get('title', 'untitled')
                    counter_tick(self.globalvars['$Counters'],
                             ''.join(['toc',str(level)]))
                    numbering = varsub(
                        ''.join(['%indexnumbering', str(level), '%']), 
                        [self.globalvars], [])
                    tocitem = { 'safe_title': '%s-%s' % (path, safe_title),
                                'link':  '%s.html#%s' % (path, safe_title),
                                'title': title,
                                'level': level,
                                'numbering': numbering,
                              }
                    if (level <= 
                        int(getkey(self.globalvars, 'toc_depth', 3))):
                        self.globalvars['$TOC'].append(dict(tocitem))

                    if (level <= 
                        int(getkey(self.globalvars, 'alt_toc_depth', 7))):
                        self.globalvars['$ALTTOC'].append(dict(tocitem))
        
        self.globalvars['$IndexedRemarks'] = remarks
        # This object is now "obselete"
        self.removed = True

    def get_text():
        return ''
