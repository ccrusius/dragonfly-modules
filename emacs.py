#
# Emacs speech recognition definitions
#
# With help from
#  * https://github.com/schickm/dragonfly-modules/blob/master/xwin.py
#
# We need emacs server to be running in order for this to work properly.
#
import os
import subprocess

from dragonfly import (Grammar, AppContext, MappingRule, CompoundRule,
                       ActionBase,
                       Dictation, Choice, Integer, IntegerRef,
                       Key, Text)
#
# Find Emacs installation path
#
emacs_root='C:'+os.sep+'emacs-24.3'
emacsclient_bin=emacs_root+os.sep+'bin'+os.sep+'emacsclientw.exe'
if not os.path.exists(emacsclient_bin):
    raise Exception(emacsclient_bin+' not found!')

class ShellCommand(ActionBase):
    """Execute a shell command"""
    def __init__(self, command, wait=None):
        self._command = self.format_command(command)
        self._wait = wait
        super(ShellCommand, self).__init__()

    def format_command(self, command):
        return command

    def _execute(self, data=None):
        command = self._command % data
        standard_out_value = subprocess.PIPE if self._wait else None
        process = subprocess.Popen(command,
                                   stdout=standard_out_value,
                                   shell=True)
        if standard_out_value:
            output = process.communicate()[0].rstrip()
            return output

class EmacsCommand(ShellCommand):
    """Execute emacsclient with given command"""
    def __init__(self, command, message=None, wait=None):
        self._message = message
        super(EmacsCommand, self).__init__(command, wait)
        
    def format_command(self, command):
        formatted_command = '(' + command + ')'
        if self._message:
            formatted_command = '(progn %s (message "%s"))' % (formatted_command, self._message)

        # Need to escape double quotes for the command line
        formatted_command = formatted_command.replace('"', '\\"')
        return emacsclient_bin + ( ' -e "%s"' % formatted_command )

class BufferCommand(EmacsCommand):
    """Execute a command on the current buffer"""
    def format_command(self, command):
        string = 'with-current-buffer (window-buffer (selected-window)) (%s)' % command
        return super(BufferCommand, self).format_command(string)

class EmacsIdentifiers(CompoundRule):
    spec = '<naming> <text>'
    extras = [
        Choice('naming', {
            # [
            #   lower(false)/upper(true) all first,
            #   cap first word, cap other words,
            #   separator
            # ]
            'constant': [ True, False, False, '_' ],
            'lisp': [ False, False, False, '-' ],
            'lower camel': [ False, False, True, '' ],
            'score': [ False, False, False, '_' ],
            'upper camel': [ False, True, True, '' ],
            'lower spaced': [ False, False, False, ' ' ]
        }),
        Dictation('text')
    ]

    def _process_recognition(self, node, extras):
        spec = extras['naming']
        text = extras['text'].format()
        text = text.upper() if spec[0] else text.lower()
        words = text.split(' ')
        if len(words) == 0: return
        if spec[1]: words[0]=words[0].capitalize()
        if spec[2]: words=[words[0]] + [w.capitalize() for w in words[1:]]
        Text(spec[3].join(words)).execute()            
               
class EmacsSymbols(MappingRule):
    mapping = {
        'at': Key('at'),
        'close arc': Key('rparen'),
        'close curly': Key('rbrace'),
        'close square': Key('rbracket'),
        'colon': Key('colon'),
        'comma': Key('comma'),
        'dot': Key('dot'),
        'hash': Key('hash'),
        'open arc': Key('lparen'),
        'open curly': Key('lbrace'),
        'open square': Key('lbracket'),
        'percent': Key('percent'),
        'plus': Key('plus'),
        'slash': Key('slash'),
    }

class EmacsGroupingSymbols(MappingRule):
    mapping = {
        'angle': Key('langle, rangle, left'),
        'arc': Key('lparen, rparen, left'),
        'curly': Key('lbrace, rbrace, left'),
        'double': Key('dquote, dquote, left'),
        'single': Key('squote, squote, left'),
        'square': Key('lbracket, rbracket, left'),
    }
    
class EmacsGlobalMappings(MappingRule):
    mapping = {
        'cancel': Key('escape:3'), # WSR screws up 'cancel'
        'undo that': Key('c-x, u'), # WSR screws up 'undo'
        'tab [<n>]': Key('tab:%(n)d'),
        'say <text>': Text('%(text)s'),
        'close window': Key('c-x,c-c'),
        #
        # File
        #
        'open file': Key('c-x, c-f'), # WSR screws up 'open'
        'save file': Key('c-x, c-s'), # WSR screws up 'save'
        #
        # Movement
        #
        'skip sex [<n>]': Key('ca-f:%(n)d'),
        'back sex [<n>]': Key('ca-b:%(n)d'),
        'skip list [<n>]': Key('ca-n:%(n)d'),
        'back list [<n>]': Key('ca-p:%(n)d'),
        'skip word [<n>]': Key('a-f:%(n)d'),
        'back word [<n>]': Key('a-b:%(n)d'),
        '(skip|right) [<n>] (block|blocks)': Key('a-e:%(n)d'),
        '(back|up) [<n>] (block|blocks)': Key('a-a:%(n)d'),
        '(skip|down) [<n>] (line|lines)': Key('c-n:%(n)d'),
        '(back|up) [<n>] (line|lines)': Key('c-p:%(n)d'),
        '[go to] line [number] [<n>]': BufferCommand('goto-line %(n)d'),
        'search <text>': Key('c-s, enter') + Text('%(text)s') + Key('enter'),
        'back search <text>': Key('c-r, enter') + Text('%(text)s') + Key('enter'),
        #
        # Selecting
        #
        '(set) mark': Key('c-space'),
        'cut': Key('c-w'),
        'copy': Key('a-w'),
        'paste': Key('c-y'),
        #
        # Erasing
        # "erase"  = remove backward
        # "delete" = remove forward
        #
        'kill sex [<n>]': Key('ca-k:%(n)d'),
        'erase [<n>] (word|words)': Key('a-backspace:%(n)d'),
        'delete [<n>] (word|words)': Key('a-delete:%(n)d'),
        'kill sex [<n>]': Key('ca-k:%(n)d'),
        '(kill|delete|erase) [<n>] (line|lines)': Key('cs-backspace:%(n)d'),
        '(erase|backspace) [<n>]': Key('backspace:%(n)d'),
        #
        # Buffers
        #
        'switch buffer': Key('c-x, b'),
        'kill buffer': Key('c-x, k'),
        #
        # Windows
        #
        'go to next window': Key('c-x, o'),
        'close other windows': Key('c-x, 1'),
        'split horizontal': Key('c-x, 2'),
        'split vertical': Key('c-x, 3'),
        #
        # Symbols
        #
        '(dash|minus)': Key('hyphen'),
        'backslash': Key('backslash'),
        '(bar|pipe)': Key('bar'),
        '(equal|equals)': Key('equal'),
        'less than': Key('langle'),
        '(greater|more|bigger) than': Key('rangle'),
        #
        # Folding
        #
        'start folding': BufferCommand('hs-minor-mode')+Key('enter, c-c, at, ca-h'),
        '(show|expand) all [(blocks|folds)]': Key('c-c, at, ca-s'),
        '(hide|collapse) all [(blocks|folds)]': Key('c-c, at, ca-h'),
        '(show|expand) (block|fold)': Key('home, c-c, at, c-s'),
        '(hide|collapse) (block|fold)': Key('home, c-c, at, c-h'),
        }
    extras = [
            IntegerRef('n',0,9999),
            Dictation('text')
            ]

    defaults = {
            'n': 1
            }

class EmacsPythonMappings(MappingRule):
    """Emacs mappings for python coding"""
    mapping = {
        '(new|create) python class': Key('a-colon')+Text('(python-skeleton-class)')+Key('enter'),
        '(new|create) python function': Text('def ():')+Key('left:3')
        }

context = AppContext(executable="emacs")
grammar = Grammar("GNU Emacs", context=context)
grammar.add_rule(EmacsIdentifiers())
grammar.add_rule(EmacsSymbols())
grammar.add_rule(EmacsGroupingSymbols())
grammar.add_rule(EmacsGlobalMappings())
grammar.add_rule(EmacsPythonMappings())
grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
