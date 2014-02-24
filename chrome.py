from dragonfly import (Grammar, AppContext, MappingRule, Integer, Key)

class GlobalChromeMappings(MappingRule):
    mapping = {
        'close tab': Key('c-w'),
	'open new tab': Key('c-t'),
        'reopen tab': Key('cs-t'),
        'go to next tab': Key('c-tab'),
        'go to previous tab': Key('cs-tab'),
        'go to tab <tab>': Key('c-%(tab)d'),
        'go to last tab': Key('c-9'),
        'go back': Key('a-left'),
        'go forward': Key('a-right'),
        'reload page': Key('c-r'),
        }
    extras=[
        Integer('tab', 1, 8)
    ]

context = AppContext(executable='chrome')
grammar=Grammar('Google Chrome',context=context)
grammar.add_rule(GlobalChromeMappings())

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
