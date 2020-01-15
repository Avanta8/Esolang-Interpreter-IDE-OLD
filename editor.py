import wx
# import wx.lib.agw.flatnotebook as flatnotebook
import wx.aui

# wx.aui almost cenrtainly contains a dockable widget
# Could have one dockwidget for the whole editor area


class TextEditor(wx.Panel):
    pass


class EditorNotebook(wx.aui.AuiNotebook):
    # https://wiki.wxpython.org/AuiNotebook
    # https://wxpython.org/Phoenix/docs/html/wx.aui.AuiNotebook.html
    # https://wxpython.org/Phoenix/docs/html/wx.lib.agw.aui.auibook.AuiNotebook.html

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Just quick stuff to check everything works

        self.AddPage(TextEditor(self), 'Window1', True)
        self.AddPage(TextEditor(self), 'Window2', True)


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
