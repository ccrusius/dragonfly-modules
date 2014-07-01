from dragonfly import (Grammar,AppContext,CompoundRule,MappingRule,Key,Text,Dictation)

class ShellCommand(CompoundRule):
    spec='shell <command>'
    extras=[
        Dictation('command')
    ]
    def _process_recognition(self,node,extras):
        words=extras['command']
        print words

class ShellMappings(MappingRule):
    """"""
    mapping={
        'cp': Text('cp '),
        'ls': Text('ls '),
        'pr stat': Text('prstat -Z 1'),
        't mucks': Text('tmux '),
    }
            
context = AppContext(executable="putty")
grammar =  Grammar('shell commands', context=context)
grammar.add_rule(ShellCommand())
grammar.add_rule(ShellMappings())
grammar.load()
def unload():
    global grammar
    if grammar : grammar.unload()
    grammar = None
