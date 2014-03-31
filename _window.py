from dragonfly import (Grammar,
                       CompoundRule,
                       Choice, Dictation, Integer)

from dragonfly.windows.window import Window
from dragonfly.windows.monitor import monitors
from dragonfly.windows.rectangle import Rectangle
from difflib import get_close_matches
from time import sleep

class PrintWindowDetails(CompoundRule):
    spec='print window details'
    def _process_recognition(self,node,extras):
        window=Window.get_foreground()
        print 'Window details'
        print 'title=',window.title
        print 'executable=',window.executable
        print 'window=',window

class FocusWindow(CompoundRule):
    spec='focus <name>'
    extras=[Dictation('name')]

    @staticmethod
    def clean_unwanted_matches(matches,name):
        return [m for m in matches if m not in [
            'focus '+name,
            'program manager',
            'winsplithookhiddenframe']]
        
    def _process_recognition(self,node,extras):
        name=extras['name'].format().lower()
        windows=[w for w in Window.get_all_windows() if w.is_visible ]
        names=[w.executable.lower() for w in windows]
        names+=[w.title.lower() for w in windows]
        matches=get_close_matches(name,names,10,0.1)
        matches=self.clean_unwanted_matches(matches,name)
        if not matches: return
        for window in windows:
            if matches[0] in [window.executable.lower(),window.title.lower()]:
                # In Windows, this is not guaranteed to work. See:
                # http://stackoverflow.com/questions/688337/how-do-i-force-my-app-to-come-to-the-front-and-take-focus
                # http://msdn.microsoft.com/en-us/library/windows/desktop/ms633539(v=vs.85).asp                
                window.set_foreground()
                return
        
class BasicWindowOps(CompoundRule):
    spec='<operation> window'
    extras=[
        Choice('operation',{
            'maximize': Window.maximize,
            'minimize': Window.minimize,
            'restore': Window.restore
            })
        ]
    def _process_recognition(self, node, extras):
        window=Window.get_foreground()
        extras['operation'](window)

class MoveToMonitorRule(CompoundRule):
    spec='move window to monitor <monitor>'
    extras=[Integer('monitor',1,9)]

    @staticmethod
    def move_to_monitor(window,monitor_number):
        monitor=monitors[monitor_number].rectangle
        current_monitor=window.get_containing_monitor().rectangle
        current_position=window.get_position()
        pos = Rectangle(
            monitor.x1+current_position.x1-current_monitor.x1,
            monitor.y1+current_position.y1-current_monitor.y1,
            current_position.dx,
            current_position.dy
        )
        window.set_position(pos)

    def _process_recognition(self, node, extras):
        monitor_number=int(extras['monitor'])-1
        self.move_to_monitor(Window.get_foreground(),monitor_number)
    
class SnapWindowRule(CompoundRule):
    spec='snap window to <region>'
    extras=[
        Choice('region',{
            'top left': [ 0, 0, 0.5, 0.5 ],
            'top half': [ 0, 0, 1, 0.5 ],
            'top right': [ 0.5, 0, 0.5, 0.5 ],
            'right half': [ 0.5, 0, 0.5, 1 ],
            'bottom right': [ 0.5, 0.5, 0.5, 0.5 ],
            'bottom half': [ 0, 0.5, 1, 0.5 ],
            'bottom left': [ 0, 0.5, 0.5, 0.5 ],
            'left half': [ 0, 0, 0.5, 1 ],
            'whole monitor': [ 0, 0, 1, 1 ],
        })]

    @staticmethod
    def snap_window(window,region_spec):
        monitor=window.get_containing_monitor().rectangle
        pos = Rectangle(
            monitor.x1+monitor.dx*region_spec[0],
            monitor.y1+monitor.dy*region_spec[1],
            monitor.dx*region_spec[2],
            monitor.dy*region_spec[3])
        window.restore()
        window.set_position(pos)

    def _process_recognition(self, node, extras):
        self.snap_window(Window.get_foreground(),extras['region'])

grammar =  Grammar('window control')
grammar.add_rule(PrintWindowDetails())
grammar.add_rule(BasicWindowOps())
grammar.add_rule(SnapWindowRule())
grammar.add_rule(MoveToMonitorRule())
grammar.add_rule(FocusWindow())
grammar.load()
def unload():
    global grammar
    if grammar : grammar.unload()
    grammar = None
