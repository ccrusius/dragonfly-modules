from dragonfly import (Grammar, AppContext, MappingRule, Key)

class GlobalChromeMappings(MappingRule):
    mapping = {
        'close tab': Key('c-w'),
        'new tab': Key('c-t'),
        'reopen tab': Key('cs-t'),
        'next tab': Key('c-tab'),
        'last tab': Key('cs-tab'),
        'down': Key('down'),
        'up': Key('up'),
        }

context = AppContext(executable='chrome')
grammar=Grammar('Google Chrome',context=context)
grammar.add_rule(GlobalChromeMappings())

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
