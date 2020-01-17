import wx
import wx.aui

import constants
from code_text import CodeText


class EditorPage(wx.Panel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.create_widgets()

        # self.set_file_info(None, None, constants.FileTypes.none)
        self.set_file_info(None, None, constants.FileTypes.brainfuck)

    def create_widgets(self):

        self.code_text = CodeText(self)
        self.visualiser = wx.Panel(self)
        self.code_runner = wx.Panel(self)

        self.aui_manager = wx.aui.AuiManager(self, wx.aui.AUI_MGR_DEFAULT | wx.aui.AUI_MGR_LIVE_RESIZE)
        self.aui_manager.AddPane(self.code_text, wx.CENTRE, 'Code Text')
        self.aui_manager.AddPane(self.visualiser, wx.TOP, 'Visualiser')
        self.aui_manager.AddPane(self.code_runner, wx.BOTTOM, 'Code Runner')
        self.aui_manager.Update()

    def set_file_info(self, filename, filepath, filetype):
        r"""
        Arguments:
            - `filename` -- name of file including extension. Eg. 'editor.py'
            - `filepath` -- full file path. Eg. 'C:\Users\Harry\Documents\Programming\Python\esolang_interpreter\Esolang-Interpreter-IDE\editor.py'
            - `filetype` -- constants.FileTypes
        """
        self.filename = filename
        self.filepath = filepath
        self.filetype = filetype

        self.code_text.set_filetype(filetype)


class EditorNotebook(wx.aui.AuiNotebook):

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
        # sizer.Add(self.editor_notebook, 1, wx.ALL | wx.EXPAND, 5)
        sizer.Add(self.editor_notebook, 1, wx.EXPAND)
        self.SetSizer(sizer)
