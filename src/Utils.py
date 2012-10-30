#!/usr/bin/python

# Utils for common tasks in the report processor

import os
import re

import G

# Helper class for translating syntactic sugar formatted lines to
# equivalent base formatted code.
class SyntaxSugarDefinition:

    # @fn __init__
    # Initialiser
    #
    # @param _regexp a regular expression pattern to match the line
    # @param _params a list of alphanumeric names to be used in _output as placeholders, in order of the regexp matches
    # @param _output an output text with _params as %param1% etc
    def __init__(self, _regexp, _params, _output):
        self.regexp_string = _regexp
        try:
            self.regexp = re.compile(_regexp, re.UNICODE)
        except re.error:
            G.critical(''.join(['Regexp ',_regexp,' failed to compile, ignoring it.']))
            self.broken = True
        else:
            G.debug(''.join(['Registred SyntaxSugar:\nRegexp: ',_regexp,
                                   ', Params: ',str(_params),
                                   ', Output: ',_output]))
            self.broken = False
            self.output = _output
            self.params = _params
            self.result = 'none'

    # @fn translate
    # Translates from a SyntaxSugar line into base formatted code
    # The result can be found as .result in this object as line array
    #
    # @param _input (possibly) SyntaxSuger formatted line
    # 
    # @return True if match occured, False otherwise
    def translate(self, _input):
        if self.broken:
            G.debug('This SyntaxSugar is broken.')
            return False
        G.debug(''.join(['Testing expression: ', _input]))
        m = re.match(self.regexp, _input)
        if m:
            G.debug(''.join([u'Match! Parameters: ',unicode(self.params)]))
            result = self.output
            for i in range(1, len(self.params)+1):
                G.debug(''.join(['Replacing parameter: ', ''.join(['%',self.params[i-1],'%']), ' -> ', m.group(i)]))
                result = result.replace(
                        ''.join(['%',self.params[i-1],'%']), 
                        m.group(i)
                    )
            G.debug(''.join(['Result: ', result]))
            self.result = result.split('\n')
            return True 
        else:
            return False 

# Recursive variable substitution (path separator is .)
def getkey(_dict, _key, _default=''):
    if not _dict:
        G.debug('Dict is not defined or empty for getkey')
        return _default
    parts = _key.split('.')
    if len(parts) == 1:
        if _key in _dict:
            return _dict[_key]
    else:
        if parts[0] in _dict:
            # FIXME maybe optimise this by not converting to and from arrays 
            return getkey(_dict[parts[0]], '.'.join(parts[1:]), _default)
    G.debug(''.join(['Key "',_key,'" not found in hash.']))
    return _default

# @fn varsub
# Variable substitution, recursive
# Handles:
# %variable% single variable substitution
# %$list using template%
#
# @param _obj Generic obj to do varsub in
# @param _dicts List of hashes, prioritised order
# @param _templates Hash of loaded templates
def varsub(_text, _dicts, _templates, recursive=True):
    # Regexps
    re_var =    '(%(\w+?)%)'
    re_list =   '(%(\$\w+?) using (\w+?)%)'
    re_counter =   '(\!\!(\w+?)\!\!)'
    re_translate =   '(__(\w+?)__)'
    re_inline = '(%([A-Za-z0-9]+?):(\w+?)%)'
    re_link = '(\[\[([^\]]+?)\]\])'

    # Foundness tracker
    found = False

    # Single variables %variable%
    m_var = re.findall(re_var, _text)
    for m in  m_var:
        G.debug(u'Varsub variable: '+m[0])
        value = ''
        for d in _dicts:
            v = getkey(d, m[1], False)
            if v:
                value = v
                found = found or v
                break
        G.debug(u'Varsub variable value: '+unicode(value))
        _text = _text.replace(m[0], unicode(value))
    
    if not recursive:
        return _text

    # Translations __token__
    m_var = re.findall(re_translate, _text)
    for m in  m_var:
        G.debug(u'Varsub variable: '+m[0])
        value = ''
        for d in _dicts:
            t = getkey(d, '$i18n', False)
            if t:
                l = getkey(t, getkey(d, 'language', 'en'), False)
                if l:
                    v = getkey(l, m[1], False)
                    if v:
                        value = v
                        found = found or v
                        break
        G.debug(u'Varsub variable value: '+unicode(value))
        _text = _text.replace(m[0], unicode(value))

    # List using template for items %$List using template%
    m_var = re.findall(re_list, _text)
    for m in  m_var:
        G.debug(u'Varsub list placeholder: '+m[0])
        G.debug(u'Varsub list variable:    '+m[1])
        G.debug(u'Varsub list template:    '+m[2])
        itemlist = []
        for d in _dicts:
            v = getkey(d, m[1], False)
            if v:
                itemlist = v
                found = found or v
                break
        template = getkey(_templates, m[2], False)
        if template: # remove this when nested getkey is implemented
            template = getkey(template, 'body', False)
        if not template:
            G.critical(''.join(['Template not found: ',m[2]]))
            next
        result = u''
        for item in itemlist:
            G.debug('Varsub list processing item: '+
                          getkey(item, 'caption', '[item caption not found!!!]'))
            result = u'\n'.join([result, varsub(template, [item]+_dicts, _templates)])
        _text = _text.replace(m[0], result)
    
    # Counter for items !!counter!!
    m_var = re.findall(re_counter, _text)
    counters = []
    for m in  m_var:
        G.debug(u'Varsub counter placeholder: '+m[0])
        G.debug(u'Varsub counter variable:    '+m[1])
        for d in _dicts:
            v = getkey(d, '$Counters', False)
            if v:
                counters = v
                break
        if v:
            counter = getkey(counters, m[1], False)
        if counter:
            _text = _text.replace(m[0], counter_get(counter))

    # Links [[link]]
    m_var = re.findall(re_link, _text)
    for m in  m_var:
        G.debug(u'Link expression: '+m[0])
        value = ''
        v = False
        parts = m[1].split(' ', 1)
        if len(parts) == 1:
            target = parts[0]
            caption = parts[0]
        else:   
            target = parts[0]
            caption = parts[1]
        G.debug(u'Link target/caption: %s/%s' % (target, caption))
        source = False
        if target[0] == '#':
            source = '$Labels'
        elif target[0] == '!':
            source = '$References'
        else:
            v = '<a href="%s">%s</a>' % (target, caption)
            G.debug(u'Link is external %s' % v)
            value = v
            found = found or v
        if source:
            target = target[1:]
            for d in _dicts:
                if source in d:
                    label = getkey(d[source], target, False)
                    if label:
                        v = '<a href="#%s">%s</a>' % (getkey(label, 'id', ''), getkey(label, 'caption', caption))
                        G.debug(u'Link is internal %s' % v)
                if v:
                    value = v
                    found = found or v
                    break
        if v:
            G.debug(u'Varsub link variable value: '+unicode(value))
            _text = _text.replace(m[0], unicode(value))

    # Tail recursive substitution
    if found:
        return varsub(_text, _dicts, _templates)
    else:
        return _text

# @fn safe_link
#
# @param title The title to translate
#
# @return A html link adress name
def safe_link(title):
    safe_title = re.sub('[\W]','', title.replace(' ','_')).lower()
    G.debug(''.join(['Safing ',title,' to ',safe_title,'.']))
    return '_'.join([safe_title, str(G.getSafeLinkId())])

def counter_create(counter_hash, name, child, style='arabic', value=0):
    counter_hash[name] = {
            'value': value,
            'style': style,
            'child': child
            }

def counter_tick(counter_hash, name, step=1):
    counter = getkey(counter_hash, name, False)
    child_name = getkey(counter, 'child', False)
    if child_name:
        child = getkey(counter_hash, child_name, False)
    else:
        child = False
    if not counter:
        G.debug("Counter "+name+" does not exist")
        return 'counter error'
    G.debug("Adding "+str(step)+" to counter "+name)
    counter['value'] += step
    if child:
        G.debug("Resetting counter "+child_name)
        child['value'] = 0
    return 0

def counter_get(counter):
    if counter:
        return str(counter['value'])
    else:
        return 'no counter'
