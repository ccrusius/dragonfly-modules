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
        
class TextFormatter(ActionBase):
    """Text formatter base class: an action that adds a pre-formatting step to 'Text'"""
    def __init__(self, spec=None):
        super(TextFormatter,self).__init__()
        self._spec = spec

    def _format_text(self, text):
        pass
        
    def _execute(self, data=None):
        text = self._spec
        if data is None:
            data = {}
        if self._spec.find('%') > -1:
            text = self._spec % data
        text = self._format_text(text)
        Text(text).execute()
    
class TypeName(TextFormatter):
    """Formats spoken words as a Java-style type name."""
    def __init__(self, spec=None):
        super(TypeName,self).__init__(spec)

    def _format_text(self, text):
        words = [ word.lower() for word in text.split(' ') ]
        return ''.join(word.capitalize() for word in words)

class VarName(TextFormatter):
    """Formats spoken words as a Java-style method/variable name."""
    def __init__(self, spec=None):
        super(VarName,self).__init__(spec)

    def _format_text(self, text):
        words = [ word.lower() for word in text.split(' ') ]
        return words[0] + ''.join(word.capitalize() for word in words[1:] )

class ScoreName(TextFormatter):
    """Formats spoken words as a C-style undercored variable name."""
    def __init__(self, spec=None):
        super(ScoreName,self).__init__(spec)

    def _format_text(self, text):
        words = [ word.lower() for word in text.split(' ') ]
        return '_'.join(words)

class LispName(TextFormatter):
    """Formats spoken words as a Lisp-style dashed name."""
    def __init__(self, spec=None):
        super(LispName,self).__init__(spec)

    def _format_text(self, text):
        words = [ word.lower() for word in text.split(' ') ]
        return '-'.join(words)
        
class Phonetic(TextFormatter):
    """
    A formatter that picks up the first letter of the words said. Letters
    can be capitalized with 'capitalize' before them.
    """
    def __init__(self, spec=None):
        super(Phonetic,self).__init__(spec)

    def _format_text(self, text):
        words = [ word.lower() for word in text.split(' ') ]
        text = ""
        capitalize = False
        for word in words:
            if word == 'capital' or word == 'cap':
                capitalize = True
            else:
                if capitalize:
                    word = word.upper()
                text = text + word[0]
                capitalize = False
        return text

class EmacsGlobalMappings(MappingRule):
    mapping = {
        '(drop it|cancel)': Key('escape:3'), # WSR screws up 'cancel'
        '(undo|regret) [that]': Key('c-x, u'), # WSR screws up 'undo'
        'tab': Key('tab'),
        'say <text>': Text('%(text)s'),
        #
        # File
        #
        '(open|load) file': Key('c-x, c-f'), # WSR screws up 'open'
        '(save|write) file': Key('c-x, c-s'), # WSR screws up 'save'
        #
        # Movement
        #
        '(skip|right|forward) [<n>] (word|words)': Key('a-f:%(n)d'),
        '(back|left) [<n>] (word|words)': Key('a-b:%(n)d'),
        '(skip|right|forward) [<n>] (block|blocks)': Key('a-e:%(n)d'),
        '(back|up) [<n>] (block|blocks)': Key('a-a:%(n)d'),
        '(skip|down|forward) [<n>] (line|lines)': Key('c-n:%(n)d'),
        '(back|up) [<n>] (line|lines)': Key('c-p:%(n)d'),
        'left [<n>]': Key('left:%(n)d'),
        'right [<n>]': Key('right:%(n)d'),
        '[go to] line [number] [<n>]': BufferCommand('goto-line %(n)d'),
        'search <text>': Key('c-s, enter') + Text('%(text)s') + Key('enter'),
        'back search <text>': Key('c-r, enter') + Text('%(text)s') + Key('enter'),
        'home': Key('c-a'),
        'end': Key('c-e'),
        '(back | left) <n>': Key('left:%(n)d'),
        #
        # Selecting
        #
        '(set) mark': Key('c-space'),
        #
        # Erasing
        # "erase"  = remove backward
        # "delete" = remove forward
        #
        'erase [<n>] (word|words)': Key('a-backspace:%(n)d'),
        'delete [<n>] (word|words)': Key('a-delete:%(n)d'),
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
        '(switch|next) window': Key('c-x, o'),
        'close other windows': Key('c-x, 1'),
        'split horizontal': Key('c-x, 2'),
        'split vertical': Key('c-x, 3'),
        #
        # Indentifiers
        #
        '(type [name] | class name) <text>': TypeName('%(text)s'),
        'score <text>': ScoreName('%(text)s'),
        'var <text>': VarName('%(text)s'),
        'spell <text>': Phonetic('%(text)s'),
        'lisp <text>': LispName('%(text)s'),
        #
        # Parenthesis
        #
        '(arc|ark)': Key('lparen, rparen, left'),
        'square': Key('lbracket, rbracket, left'),
        'curly': Key('lbrace, rbrace, left'),
        'angle': Key('langle, rangle, left'),
        'single': Key('squote, squote, left'),
        'double': Key('dquote, dquote, left'),
        #
        # Symbols
        #
        'at': Key('at'),
        'hash': Key('hash'),
        'colon': Key('colon'),
        'comma': Key('comma'),
        'dot': Key('dot'),
        'slash': Key('slash'),
        '(dash|minus)': Key('hyphen'),
        'backslash': Key('backslash'),
        '(bar|pipe)': Key('bar'),
        '(equal|equals)': Key('equal'),
        'less than': Key('langle'),
        '(greater|more|bigger) than': Key('rangle'),
        'percent': Key('percent'),
        'plus': Key('plus'),
        'enter': Key('enter'),
        #
        # Folding
        #
        '(begin|start) folding': BufferCommand('hs-minor-mode')+Key('enter, c-c, at, ca-h'),
        '(show|expand) all [(blocks|folds)]': Key('c-c, at, ca-s'),
        '(hide|collapse) all [(blocks|folds)]': Key('c-c, at, ca-h'),
        '(show|expand) (block|fold)': Key('c-c, at, c-s'),
        '(hide|collapse) (block|fold)': Key('c-c, at, c-h'),
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
        '(new|create) python def': Key('a-colon')+Text('(python-skeleton-def)')+Key('enter')
        }

context = AppContext(executable="emacs")
grammar = Grammar("GNU Emacs", context=context)
grammar.add_rule(EmacsGlobalMappings())
grammar.add_rule(EmacsPythonMappings())
grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
