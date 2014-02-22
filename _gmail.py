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

context = AppContext(title='@gmail.com - Gmail')
grammar = Grammar('GMail',context=context)
grammar.add_rule(GMailMappings())
grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
