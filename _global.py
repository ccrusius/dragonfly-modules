from dragonfly import (Grammar, MappingRule, IntegerRef, Key)

class GlobalMovementRule(MappingRule):
    mapping={
        'up [<n>]': Key('up:%(n)d'),
        'down [<n>]': Key('down:%(n)d'),
        'left [<n>]': Key('left:%(n)d'),
        'right [<n>]': Key('right:%(n)d'),
        'home': Key('home'),
        'end': Key('end'),
        'enter [<n>]': Key('enter:%(n)d'),
    }
    extras=[
        IntegerRef('n',1,9999)
    ]
    defaults = {
        'n': 1
    }

grammar=Grammar('Global Mappings')
grammar.add_rule(GlobalMovementRule())
grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None

