import wx
import wx.aui
import wx.lib.agw.aui.framemanager as _fm

import constants
from code_text import CodeText
from visualiser import Visualiser


print(_fm.AuiManager.RestorePane)

class RestoringManager(wx.aui.AuiManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._pane_infos = {}

        self.Bind(wx.aui.EVT_AUI_PANE_CLOSE, self.pane_close_event)

    def pane_close_event(self, event):
        pane = event.GetPane()
        # self._pane_infos[pane.window] = self.SavePaneInfo(pane)
        self._pane_infos[pane.window] = (self.SavePaneInfo(pane), pane)

    def restore_window(self, window):
        # self.LoadPaneInfo(self._pane_infos[window], self.GetPane(window))
        self.LoadPaneInfo(*self._pane_infos[window])
        self.Update()


class EditorPage(wx.Panel):

    def __init__(self, *args, filename, filepath, filetype, text, **kwargs):
        super().__init__(*args, **kwargs)

        self.create_widgets()

        self.set_file_info(filename, filepath, filetype)
        if text:
            self.code_text.SetText(text)

    def create_widgets(self):

        self.code_text = CodeText(self)
        self.visualiser = Visualiser(self)
        self.code_runner = wx.Panel(self)

        # self.aui_manager = wx.aui.AuiManager(self, wx.aui.AUI_MGR_DEFAULT | wx.aui.AUI_MGR_LIVE_RESIZE)
        # self.aui_manager = wx.aui.AuiManager(self, wx.aui.AUI_MGR_ALLOW_FLOATING | wx.aui.AUI_MGR_TRANSPARENT_HINT | wx.aui.AUI_MGR_LIVE_RESIZE | wx.aui.AUI_MGR_ALLOW_ACTIVE_PANE)
        # self.aui_manager = RestoringManager(self, wx.aui.AUI_MGR_ALLOW_FLOATING | wx.aui.AUI_MGR_TRANSPARENT_HINT | wx.aui.AUI_MGR_LIVE_RESIZE | wx.aui.AUI_MGR_ALLOW_ACTIVE_PANE)
        self.aui_manager = _fm.AuiManager(self, wx.aui.AUI_MGR_ALLOW_FLOATING | wx.aui.AUI_MGR_TRANSPARENT_HINT | wx.aui.AUI_MGR_LIVE_RESIZE | wx.aui.AUI_MGR_ALLOW_ACTIVE_PANE)
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

    def open_visualiser(self):
        # self.aui_manager.RestorePane(self.aui_manager.GetPane(self.visualiser))
        print('open visualiser')
        # self.aui_manager.InsertPane(self.visualiser, self.aui_manager.GetPane(self.visualiser).Show())
        self.aui_manager.RestorePane(self.aui_manager.GetPane(self.visualiser))
        self.aui_manager.Update()
        # self.aui_manager.restore_window(self.visualiser)


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

    def open_visualiser(self):
        page = self.GetCurrentPage()
        if page is None:
            return
        page.open_visualiser()
