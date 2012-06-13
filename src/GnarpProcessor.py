#!/usr/bin/python

import sys
import io
import datetime

import G

from GnarpUtils import getkey
from GnarpGeneric import Generic

## @class Processor
# 
# This class takes a filename, processes it using Gnarp objects and split out 
# output. It supports besided all the speicalised objects (in the files
# GnarpX) syntac suger and some special cases such as title and paragraph.
#
# FIXME: Finish commenting this
class Processor:

    ## @fn __init__
    #
    # The initialiser for the Processor class
    #
    # @param _root The root folder where the file is
    # @param _filename The filename part of the path
    # @param optional _output The output format [html]
    def __init__(self, _root, _filename, _output='html', _is_main_file=True, _outputfile='noname'):
        self.root = _root
        self.filename = _filename
        self.is_main_file = _is_main_file
        self.output = _output
        self.globalvars = {'root': _root, 'output': _output, 'filename': _filename, 'outputfile': _outputfile} # A hash for storing document data while processing
        self.finished_once = False # The processing needs to be done several times
        self.objects = [] # The sequence of objects that makes the document
        self.process_queue = [] # A list of objects that need to be processed again
        self.document = u'unproduced'
        
        # SyntaxSugar 
        self.globalvars['$SyntaxSugar'] = []

        # Templates
        self.globalvars['$Templates'] = {} 
    
    ## @fn set_output
    #
    # FIXME: Investigate if this is necessary
    #
    # @param _output
    def set_output(self, _output):
        self.output = _output
    
    ## @fn init_file
    # 
    # Open the file and store the pointer to the object
    #
    # @return True on success, False on failure
    def init_file(self):
        self.first_lines = getkey(G.first_lines, self.output, [])
        filepath = ''.join([self.root,self.filename])
        G.info(''.join(['Trying to open file "',filepath,'".']))
        try:
            self.file = io.open(filepath, 'r')
        except IOError:
            G.critical(''.join(['The file "',filepath,'" could not be opened.']))
            return False
        else:
            G.info(''.join(['The file "',filepath,'" was opened.']))
            return True
    
    ## @fn get_line 
    # 
    # Get the next line
    #
    # @return The line as a string
    def get_line(self):
        if len(self.first_lines):
            G.debug("Return first line")
            self.doing_first_lines = True
            return self.first_lines.pop(0) # shift
        if self.doing_first_lines:
            self.first_object = True
            self.doing_first_lines = False
        try:
            line = self.file.readline()
        except IOError:
            G.warning('IO Error: Could not read line.')
            return ''
        else:
            return line
    
    ## @fn close_file
    # 
    # Close the file opened for process
    #
    # @return True on success, False on failure
    def close_file(self):
        try:
            self.file.close()
        except IOError:
            G.warning('File close failed.')
            return False
        else:
            return True
    
    ## @fn load_objects
    # 
    # Reads file line by line and strips out objects.
    def load_objects(self):
        self.doing_first_lines = True
        self.first_object = True # First object will be treated differently
        last_line = False # A flag for last line (eof) detection
        lines = [] # A object line buffer, cleared after each object stored
        while (True):
            next_line = self.get_line()
            # Detect last line before stripping away te \n
            if len(next_line) == 0:
                last_line = True
                G.debug('Detected last line.')
            next_line = next_line.strip('\n\r')
            G.debug(''.join(['Reading line: ',next_line]))

            # Check if it is an empty line, if so, finish object
            if not next_line:
                if len(lines):
                    G.debug('Creating object.')
    
                    # Create a Generic Object that can later be upgraded
                    obj = Generic(self.globalvars, lines, self.first_object, self.is_main_file)
    
                    # Prepare for next round and save the current object
                    lines = []
                    self.first_object = False
    
                    if not obj.removed:
                        self.objects.append(obj)
                else:
                    G.debug('Skipping empty object.')
            else:
                lines.append(next_line)
                #lines.append(next_line.strip())
            if last_line:
                return

    ## @fn preprocess_objects
    #
    # Loops through the object list until there are no objects left to (re)propress
    # Takes care of Input and Use objects before general processing
    # and puts all other objects in the process queue for later handling
    def preprocess_objects(self):
        G.info('Starting preprocessing.')
        rerun = True
        turn_count = 0
        while (rerun and turn_count < 100):
            turn_count += 1
            G.info(''.join(['Prerocessing round ',str(turn_count),'.']))
            rerun = False
            i = 0
            o = len(self.objects)
            G.debug("There are "+str(o)+" objects.")
            while i < o:
                obj = self.objects[i]
                G.debug("Preprocessing object of type "+obj.object_name)
                if obj.object_name in ['Use','Input','Template']:
                    obj.process()
                    s = len(obj.sub_objects)
                    G.debug("There are "+str(s)+" subobjects.")
                    if s > 0: # if there are subobjects in object
                        G.debug("There are sub-objects.")
                        result = []
                        for j in range(0, i):
                            result.append(self.objects[j])
                        for j in range(0, s):
                            result.append(obj.sub_objects[j])
                            G.debug("Adding object "+obj.sub_objects[j].object_name)
                        for j in range(i+1, o):
                            result.append(self.objects[j])
                        self.objects = result
                        i -= 1
                        o += s - 1
                    else:
                        G.debug("There are no sub-objects.")
                elif 'Wrapper' in obj.object_name:
                    G.info('The wrapper is omitted in the process queue')
                else:
                    self.process_queue.append(obj)
                i += 1
        G.debug('Did '+str(turn_count)+' turns')
        G.info('Finished preprocessing.')
    
    ## @fn process_objects_for_syntax_sugar
    #
    # Loops through the object list until there are no objects left to (re)propress
    # Takes care of Input and Use objects before general processing
    # and puts all other objects in the process queue for later handling
    def process_objects_for_syntax_sugar(self):
        G.info('Starting syntax sugar processing.')
        for obj in self.objects:
            # SyntaxSugar translation (for paragraphs, which is the fallback object type)
            if obj.object_name == "Paragraph" and len(obj.lines):    
                if '$SyntaxSugar' in self.globalvars:
                    for sugar in self.globalvars['$SyntaxSugar']:
                        if not sugar.broken:
                            G.debug(''.join(['Running SyntaxSugar: ',sugar.regexp_string]))
                            if sugar.translate(obj.lines[0]):
                                obj.content = '' # clear object content from old syntax sugar
                                G.info(''.join(['Processing pattern: ',sugar.regexp_string]))
                                obj.lines.pop(0)
                                obj.lines[:0] = sugar.result
                                obj.transform() # reload object from new source
                
        G.info('Finished syntax sugar processing.')
    
    ## @fn process_object_queue
    #
    # Loops through the object list until there are no objects left to (re)propress
    def process_object_queue(self):
        G.info('Starting queue processing.')
        subprocessors = getkey(self.globalvars, '$Subprocessors', [])
        while(len(self.process_queue)):
            obj = self.process_queue.pop(0)
            if not obj.removed:
                G.info(''.join(['Processing object of type ', obj.object_name]))
                for sp in subprocessors:
                    new_objects = sp.run(obj)
                    if len(new_objects):
                        for no in new_objects:
                            self.objects.append(no)
                            self.process_queue.append(no)
                        obj.needs_rerun = True
                obj.process()
                if obj.needs_rerun:
                    self.process_queue.append(obj)
        G.info('Finished queue processing.')

    ## @fn perform_wrapping
    #
    # Loops through the object list until there are no objects left to (re)propress
    def perform_wrapping(self):
        G.info('Starting wrapping.')
        self.globalvars['body'] = ''
        self.globalvars['style'] = ''
        self.globalvars['script'] = ''
        for obj in self.objects:
            if not obj.removed:
                if not obj.body == '': self.globalvars['body'] = u'\n'.join([self.globalvars['body'], obj.body])
                if not obj.style == '': self.globalvars['style'] = u'\n'.join([self.globalvars['style'], obj.style])
                if not obj.script == '': self.globalvars['script'] = u'\n'.join([self.globalvars['script'], obj.script])
        templates = getkey(self.globalvars, '$Templates', {})
        for tname in templates:
            G.debug('Adding template to style/script for '+tname)
            template = getkey(templates, tname, {})
            self.globalvars['style'] = '\n'.join([self.globalvars['style'], getkey(template, 'style')])
            self.globalvars['script'] = '\n'.join([self.globalvars['script'], getkey(template, 'script')])

        wrapper = getkey(self.globalvars, '$Wrapper', False)
        if wrapper:
            wrapper.process()
            self.document = wrapper.body
        else:
            G.critical("No wrapper registered")
            self.document = u'no wrapper'
        G.info('Finished wrapping.')

    ## @fn postprocess_objects
    #
    # Call the post_process function on each object.
    #
    # @return nothing
    def postprocess_objects(self):
        G.info("Doing post-processing")
        for obj in self.objects:
            #G.debug("Doing post-processing on " + obj.object_name)
            obj.post_process()

    ## @fn generate
    # 
    # A aggregate wrapper that calls all functions needed to generate the output.
    # This is the interface to the user application.
    # 
    # @param _template The template name (without path)
    #
    # @return True on success, False on failure
    def generate(self):
        # Store todays date
        self.globalvars['today'] = str(datetime.date.today())

        if not self.init_file():
            return False
        self.load_objects()
        self.close_file()
        G.debug('\n'.join(['POST LOAD_OBJECT DUMP', self.get_objects_as_string()]))
        self.preprocess_objects()
        G.debug('\n'.join(['POST PRE_PROCESS DUMP', self.get_objects_as_string()]))
        self.process_objects_for_syntax_sugar()
        G.debug('\n'.join(['POST PROCESS_OBJECT_FOR_SYNTAX_SUGAR DUMP', self.get_objects_as_string()]))
        self.process_object_queue()
        self.perform_wrapping()
    
    ## @fn get_text
    #
    # Concatenates all objects' texts and returns them
    #
    # @return Text represenation of all objects
    def get_text(self):
        return self.document

    ## @fn get_objects_as_strings
    #
    # Concatenates all objects' types and primaries and returns them
    #
    # @return Text represenation of all objects
    def get_objects_as_string(self):
        output = ''
        for obj in self.objects:
            output = '\n'.join([output, '============================================',obj.dump()])
        return output
