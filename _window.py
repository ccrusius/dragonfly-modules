from dragonfly import *

"""
    Snap window to a region of the current monitor.
"""
class SnapWindowRule(CompoundRule):
    spec = '(snap|place|move) window [to] [the] [<screen_region>] [corner] [ [on] monitor <monitor>]'
    extras = [
        Choice('screen_region', {
            'northwest': 'northwest', 'top left': 'northwest',
            'north': 'north', 'top': 'north',
            'northeast': 'northeast', 'top right': 'northeast',
            'east': 'east', 'right': 'east',
            'southeast': 'southeast', 'bottom right': 'southeast',
            'south': 'south', 'bottom': 'south',
            'southwest': 'southwest', 'bottom left': 'southwest',
            'west': 'west', 'left': 'west',
            'maximized': 'maximized',
            'as-is': 'as-is', 'as it is': 'as-is', 'unchanged': 'as-is'
        }),
        Integer('monitor',1,4)
    ]

    def __init__(self):
        self.region_specs ={
            'northwest': [ 0, 0, 0.5, 0.5 ], 'north': [ 0, 0, 1, 0.5 ],
            'northeast': [ 0.5, 0, 0.5, 0.5 ], 'east': [ 0.5, 0, 0.5, 1 ],
            'southeast': [ 0.5, 0.5, 0.5, 0.5 ], 'south': [ 0, 0.5, 1, 0.5 ],
            'southwest': [ 0, 0.5, 0.5, 0.5 ], 'west': [ 0, 0, 0.5, 1 ],
            'maximized': [ 0, 0, 1, 1 ], 'as-is': [ -1, -1, -1, -1 ]
            }
        self.monitor_specs = {}
        for i, m in enumerate(monitors):
            self.monitor_specs[i]=m
        super(SnapWindowRule,self).__init__()

    def _process_recognition(self, node, extras):
        window=Window.get_foreground()
        
        if 'monitor' in extras:
            monitor=self.monitor_specs[extras['monitor']-1].rectangle
        else:
            monitor=window.get_containing_monitor().rectangle

        if 'screen_region' in extras:
            region_id=extras['screen_region']
        else:
            region_id='as-is'
            
        region_spec=self.region_specs[region_id]

        if region_spec[0] < 0:
            current_monitor=window.get_containing_monitor().rectangle
            current_position=window.get_position()
            pos = Rectangle(
                monitor.x1+current_position.x1-current_monitor.x1,
                monitor.y1+current_position.y1-current_monitor.y1,
                current_position.dx,
                current_position.dy
                )
        else:
            pos = Rectangle(
                monitor.x1+monitor.dx*region_spec[0],
                monitor.y1+monitor.dy*region_spec[1],
                monitor.dx*region_spec[2],
                monitor.dy*region_spec[3])

        window.set_position(pos)

"""
    Set up the grammar
"""
grammar =  Grammar('window control')
grammar.add_rule(SnapWindowRule())
grammar.load()
def unload():
    global grammar
    if grammar : grammar.unload()
    grammar = None
