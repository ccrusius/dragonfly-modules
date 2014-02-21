from dragonfly import *

class MoveWindowMonitor(ActionBase):
    """Move window to a given monitor."""
    def __init__(self, spec=None):
        super(MoveWindowMonitor,self).__init__()
        self._spec = spec

    def _execute(self, data=None):
        window=Window.get_foreground()
        monitor=monitors[int(self._spec%data)-1].rectangle
        current_monitor=window.get_containing_monitor().rectangle
        current_position=window.get_position()
        pos = Rectangle(
            monitor.x1+current_position.x1-current_monitor.x1,
            monitor.y1+current_position.y1-current_monitor.y1,
            current_position.dx,
            current_position.dy
        )
        window.set_position(pos)
    
class SnapWindow(ActionBase):
    """Snap window to some region of the current monitor"""
    def __init__(self, spec=None):
        super(SnapWindow,self).__init__()
        self._spec = spec
        self.region_specs ={
            'top left': [ 0, 0, 0.5, 0.5 ],
            'top half': [ 0, 0, 1, 0.5 ],
            'top right': [ 0.5, 0, 0.5, 0.5 ],
            'right half': [ 0.5, 0, 0.5, 1 ],
            'bottom right': [ 0.5, 0.5, 0.5, 0.5 ],
            'bottom half': [ 0, 0.5, 1, 0.5 ],
            'bottom left': [ 0, 0.5, 0.5, 0.5 ],
            'left half': [ 0, 0, 0.5, 1 ],
            'maximize': [ 0, 0, 1, 1 ]
            }

    def _execute(self, data=None):
        window=Window.get_foreground()
        monitor=window.get_containing_monitor().rectangle
        region_spec=self.region_specs[self._spec % data]
        pos = Rectangle(
            monitor.x1+monitor.dx*region_spec[0],
            monitor.y1+monitor.dy*region_spec[1],
            monitor.dx*region_spec[2],
            monitor.dy*region_spec[3])
        window.set_position(pos)


class WindowMappings(MappingRule):
    mapping = {
        'maximize window': SnapWindow('maximize'),
        'snap window to <screen_region>': SnapWindow('%(screen_region)s'),
        'move window to monitor <monitor>': MoveWindowMonitor('%(monitor)d'),
    }
    extras = [
        Choice('screen_region', {
            'top left':     'top left',
            'top half':     'top half',
            'top right':    'top right',
            'right half':   'right half',
            'bottom right': 'bottom right',
            'bottom half':  'bottom half',
            'bottom left':  'bottom left',
            'left half':    'left half',
        }),
        Integer('monitor',1,4)
    ]

"""
    Set up the grammar
"""
grammar =  Grammar('window control')
grammar.add_rule(WindowMappings())
grammar.load()
def unload():
    global grammar
    if grammar : grammar.unload()
    grammar = None
