import wx
import wx.aui

import constants
from code_text import CodeText


class EditorPage(wx.Panel):

    def __init__(self, *args, filename, filepath, filetype, text, **kwargs):
        super().__init__(*args, **kwargs)

        self.create_widgets()

        self.set_file_info(filename, filepath, filetype)
        if text:
            self.code_text.SetText(text)

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

    def get_file_info(self):
        return self.filename, self.filepath, self.filetype

    def get_current_text(self):
        return self.code_text.GetText()


class EditorNotebook(wx.aui.AuiNotebook):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, style=wx.aui.AUI_NB_DEFAULT_STYLE)

    def new_page(self, filename, filepath, filetype, text):
        self.AddPage(EditorPage(self, filename=filename, filepath=filepath, filetype=filetype, text=text), filename or 'Untitled', True)

    def set_current_file_info(self, filename, filepath, filetype):
        page = self.GetCurrentPage()
        if page is not None:
            page.set_file_info(filename, filepath, filetype)
            self.SetPageText(self.GetPageIndex(page), filename)

    def get_current_file_info(self):
        page = self.GetCurrentPage()
        if page is None:
            return None
        return page.get_file_info()

    def get_current_text(self):
        page = self.GetCurrentPage()
        if page is None:
            return None
        return page.get_current_text()
