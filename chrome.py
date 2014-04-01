from dragonfly import (Grammar, AppContext, MappingRule, Integer, Key, Text)

class GlobalChromeMappings(MappingRule):
    mapping = {
        'close tab': Key('x'),                           # vimium
	'open new tab': Key('t'),                        # vimium
        'duplicate tab': Key('y/25,t'),                  # vimium
        'reopen tab': Key('X'),                          # vimium
        '(go to) next tab': Key('K'),                    # vimium
        '(go to) previous tab': Key('J'),                # vimium
        'go to tab <tab>': Key('c-%(tab)d'),
        '(go to) first tab': Key('g,0'),                 # vimium
        '(go to) last tab': Key('g,dollar'),             # vimium
        'go back': Key('H'),                             # vimium
        'go forward': Key('L'),                          # vimium
        'go to address': Key('a-d'),
        'reload page': Key('r'),                         # vimium
        'show labels': Key('f'),                         # vimium
        'show labels in new tab': Key('s-f'),            # vimium
        '(go to) label <number>': Text('%(number)d'),    # vimium
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
