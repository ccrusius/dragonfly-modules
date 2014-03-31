#
# Outlook commands
#
# With help from:
#  * http://msdn.microsoft.com/en-us/library/ff184607.aspx
#  * http://dragonfly-modules.googlecode.com/svn-history/r50/trunk/command-modules/documentation/mod-_outlook.html
#

from dragonfly import(Config, Section, Item,
                      Grammar, ConnectionGrammar, AppContext,
                      MappingRule, CompoundRule,
                      Key, Integer, IntegerRef,
                      DictList, DictListRef)
import tempfile
import os
import os.path

config = Config('Microsoft Outlook control')
config.lang = Section('Language section')
config.lang.go_to_folder = Item('folder <folder>')
config.lang.move_to_folder = Item('move to <folder>')
config.lang.sync_folders = Item('refresh folders')
config.load()

def collection_iter(collection):
    for index in xrange(1, collection.Count + 1):
        yield collection.Item(index)

class OutlookControlGrammar(ConnectionGrammar):
    def __init__(self):
        self.folders = DictList("folders")
        super(OutlookControlGrammar,self).__init__(
            name="Microsoft Outlook control",
            context=AppContext(executable="outlook"),
            app_name="Outlook.Application"
        )

    def connection_up(self):
        self.update_folders()

    def connection_down(self):
        self.reset_folders()

    def update_folders(self):
        root_folder = self.application.Session.DefaultStore.GetRootFolder()
        self.folders.set({})
        stack = [collection_iter(root_folder.Folders)]
        while stack:
            try:
                folder = stack[-1].next()
            except StopIteration:
                stack.pop()
                continue
            self.folders[folder.Name] = folder
            stack.append(collection_iter(folder.Folders))

    def reset_folders(self):
        self.folders.set({})

    def get_active_explorer(self):
        try:
            explorer = self.application.ActiveExplorer()
        except com_error, e:
            self._log.warning('%s: COM error getting active explorer: %s'
                              % (self, e))
            return None
        if not explorer:
            self._log_warning('%s: no active explorer.' % self)
            return None
        return explorer

grammar = OutlookControlGrammar()

class SynchronizeFolderRule(CompoundRule):
    spec = config.lang.sync_folders
    def _process_recognition(self, node, extras):
        self.grammar.update_folders()

grammar.add_rule(SynchronizeFolderRule())
    
class GoToFolderRule(CompoundRule):
    spec = config.lang.go_to_folder
    extras = [DictListRef('folder', grammar.folders)]
    def _process_recognition(self, node, extras):
        folder = extras['folder']
        explorer = self.grammar.get_active_explorer()
        if not explorer: return
        explorer.SelectFolder(folder)

grammar.add_rule(GoToFolderRule())

class MoveToFolderRule(CompoundRule):
    """Move selected messages to folder"""
    spec = config.lang.move_to_folder
    extras = [DictListRef('folder', grammar.folders)]
    def _process_recognition(self, node, extras):
        folder = extras['folder']
        explorer = self.grammar.get_active_explorer()
        if not explorer: return
        for item in collection_iter(explorer.Selection):
            self._log.debug('%s: moving item %r to folder %r.'
                            % (self, item.Subject, folder.Name))
            item.Move(folder)

grammar.add_rule(MoveToFolderRule())

class OpenAttachmentRule(CompoundRule):
    spec='open attachment <n>'
    extras=[Integer('n', 1, 10)]
    def _process_recognition(self,node,extras):
        index=extras['n']
        explorer=self.grammar.get_active_explorer()
        if not explorer: return
        if explorer.Selection.Count < 0:
            self._log.warning('%s: no selected, not opening.' % self)
            return
        elif explorer.Selection.Count > 1:
            self._log.warning('%s: multiple items selected, not opening.' % self)
            return
        item=explorer.Selection.Item(1)
        if not (1 <= index <= item.Attachments.Count):
            self._log.warning('%s: attachment index %d of item %r'
                              ' out of range (1 <= index <= %d).'
                              % (self, index, item.Subject, item.Attachments.Count))
            return
        attachment=item.Attachments.Item(index)
        filename=os.path.basename(attachment.FileName)
        temp_dir=tempfile.mkdtemp()
        path=os.path.join(temp_dir,filename)
        attachment.SaveAsFile(path)
        os.startfile(path)

grammar.add_rule(OpenAttachmentRule())

class OutlookMappings(MappingRule):
    """outlook keyboard shortcuts"""
    mapping = {
        'mark as read': Key('c-q'),
        'mark as unread': Key('c-u'),
        'collapse': Key('left'),
        'expand': Key('right'),
        'shortcut <n>': Key('cs-%(n)d'),
        'next week [<n>]': Key('a-down:%(n)d'),
        'previous week [<n>]': Key('a-up:%(n)d'),
    }
    extras = [
            IntegerRef('n',0,9999)
            ]
    defaults = {
            'n': 1
            }

grammar.add_rule(OutlookMappings())

grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
