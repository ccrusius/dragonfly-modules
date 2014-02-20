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

class GMailMappings(MappingRule):
    """
    Mappings for GMmail. Shortcuts should be enabled in GMail settings.
    """
    mapping = {
        'compose message': Key('c'),
        'message list': Key('u'),
        'archive message': Key('e'),
        'reply [to] message': Key('r'),
        'reply [to] all': Key('a'),
        'select message': Key('x'),
        'erase message': Key('hash'),
        'open message': Key('o'),
    }

grammars = {}

def create_chrome_grammar(name,context,rules):
    global grammars
    grammars[name] = Grammar( name, context )
    for rule in rules:
        grammars[name].add_rule(rule)
    grammars[name].load()
    
chrome_context = AppContext(executable='chrome')
create_chrome_grammar('Google Chrome',chrome_context,[GlobalChromeMappings()])

gmail_context = chrome_context & AppContext(title='@gmail.com')
create_chrome_grammar('Google Chrome GMail', gmail_context, [GMailMappings()])

def unload():
    global grammars
    for name, grammar in grammars.iteritems():
        if grammar: grammar.unload()
        grammars[name] = None
    grammars = {}
