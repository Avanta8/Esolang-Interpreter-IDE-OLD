import wx
# import wx.lib.agw.flatnotebook as flatnotebook
import wx.aui

# wx.aui almost cenrtainly contains a dockable widget
# Could have one dockwidget for the whole editor area


class EditorPage(wx.Panel):
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.create_widgets()
    
    def create_widgets(self):

        self.code_text = wx.TextCtrl(self)
        self.visualiser = wx.Panel(self)
        self.code_runner = wx.Panel(self)

        self.aui_manager = wx.aui.AuiManager(self, wx.aui.AUI_MGR_DEFAULT | wx.aui.AUI_MGR_LIVE_RESIZE)
        self.aui_manager.AddPane(self.code_text, wx.CENTRE, 'Code Text')
        self.aui_manager.AddPane(self.visualiser, wx.TOP, 'Visualiser')
        self.aui_manager.AddPane(self.code_runner, wx.BOTTOM, 'Code Runner')
        self.aui_manager.Update()



class EditorNotebook(wx.aui.AuiNotebook):
    # https://wiki.wxpython.org/AuiNotebook
    # https://wxpython.org/Phoenix/docs/html/wx.aui.AuiNotebook.html
    # https://wxpython.org/Phoenix/docs/html/wx.lib.agw.aui.auibook.AuiNotebook.html

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, style=wx.aui.AUI_NB_DEFAULT_STYLE)

        # Just quick stuff to check everything works

        self.AddPage(EditorPage(self), 'Window1', True)
        self.AddPage(EditorPage(self), 'Window2', True)
        self.AddPage(EditorPage(self), 'Window2', True)
        self.AddPage(EditorPage(self), 'Window2', True)


class EditorArea(wx.Panel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.create_widgets()

    def create_widgets(self):
        self.editor_notebook = EditorNotebook(self)
        sizer = wx.BoxSizer()
        sizer.Add(self.editor_notebook, 1, wx.ALL | wx.EXPAND, 5)
        # sizer.Add(self.editor_notebook, 1, wx.EXPAND)
        self.SetSizer(sizer)
