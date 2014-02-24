from dragonfly import (Grammar, AppContext, MappingRule, Key)

class GMailMappings(MappingRule):
    """
    Mappings for GMail. Shortcuts should be enabled in GMail settings for this to work.
    """
    mapping = {
        'compose message': Key('c'),
        'message list': Key('u'),
        'archive message': Key('e'),
        'reply to author': Key('r'),
        'reply to all': Key('a'),
        'select message': Key('x'),
        'erase message': Key('hash'),
        'open message': Key('o'),
    }

context1 = AppContext(title=' Gmail')
context2 = AppContext(title='@gmail.com')
grammar = Grammar('GMail',context=(context1 & context2))
grammar.add_rule(GMailMappings())
grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
