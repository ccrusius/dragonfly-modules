from dragonfly import (Grammar,
                       CompoundRule,
                       Choice, Dictation, Integer)

from dragonfly.windows.window import Window
from dragonfly.windows.monitor import monitors
from dragonfly.windows.rectangle import Rectangle
from difflib import get_close_matches
from time import sleep

class FocusWindow(CompoundRule):
    spec='focus <name>'
    extras=[Dictation('name')]

    @staticmethod
    def clean_unwanted_matches(matches,name):
        result=[]
        for match in matches:
            if match == 'focus '+name: continue
            if match == 'program manager': continue
            if match == 'winsplithookhiddenframe': continue
            result.append(match)
        return result
        
    def _process_recognition(self,node,extras):
        name=extras['name'].format().lower()
        windows=Window.get_all_windows()
        names=[]
        for window in windows:
            if not window.is_visible: continue
            names.append(window.executable.lower())
            names.append(window.title.lower())
        executables=[w.executable.lower() for w in windows]
        titles=[w.title.lower() for w in windows]
        matches=get_close_matches(name,names,10,0.1)
        matches=self.clean_unwanted_matches(matches,name)
        if len(matches) == 0: return
        for window in windows:
            if not window.is_visible: continue
            if window.executable.lower()==matches[0] or window.title.lower()==matches[0]:
                for attempt in range(4):
                    try:
                        window.set_foreground()
                    except Exception:
                        sleep(0.2)
                    else:
                        break
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
grammar.add_rule(BasicWindowOps())
grammar.add_rule(SnapWindowRule())
grammar.add_rule(MoveToMonitorRule())
grammar.add_rule(FocusWindow())
grammar.load()
def unload():
    global grammar
    if grammar : grammar.unload()
    grammar = None
