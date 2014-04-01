from dragonfly import (Grammar, AppContext, MappingRule, Integer, Key, Text)

class GlobalChromeMappings(MappingRule):
    mapping = {
        'close tab': Key('c-w'),
	'open new tab': Key('c-t'),
        'duplicate tab': Key('y/25,t'),                  # vimium
        'reopen tab': Key('cs-t'),
        '[go to] next tab': Key('c-pgdown'),
        '[go to] previous tab': Key('c-pgup'),
        'go to tab <tab>': Key('c-%(tab)d'),
        '[go to] first tab': Key('c-1'),
        '[go to] last tab': Key('c-9'),
        'go back': Key('a-left'),
        'go forward': Key('a-right'),
        'go to address': Key('a-d'),
        'reload page': Key('f5'),
        'show labels': Key('f'),                         # vimium
        'show labels in new tab': Key('s-f'),            # vimium
        '[go to] label <number>': Text('%(number)d'),    # vimium
        'duplicate tab': Key('y,t'),                     # vimium
        }
    extras=[
        Integer('tab', 1, 8),
        Integer('number', 1, 9999)
    ]

context = AppContext(executable='chrome')
grammar=Grammar('Google Chrome',context=context)
grammar.add_rule(GlobalChromeMappings())
grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
