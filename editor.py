import wx
import wx.aui
import wx.lib.agw.aui

import constants
from code_text import CodeText
from visualiser import Visualiser


class EditorPage(wx.Panel):

    def __init__(self, *args, filename, filepath, filetype, text, **kwargs):
        super().__init__(*args, **kwargs)

        self.create_widgets()

        self.set_file_info(filename, filepath, filetype)
        if text:
            self.code_text.SetText(text)

        self.Bind(wx.EVT_WINDOW_DESTROY, self.window_destroy_event, self)

    def create_widgets(self):

        self.code_text = CodeText(self)
        self.visualiser = Visualiser(self)
        self.code_runner = wx.Panel(self)

        # self.aui_manager = wx.aui.AuiManager(self, wx.aui.AUI_MGR_DEFAULT | wx.aui.AUI_MGR_LIVE_RESIZE)
        self.aui_manager = wx.aui.AuiManager(self, wx.aui.AUI_MGR_ALLOW_FLOATING | wx.aui.AUI_MGR_TRANSPARENT_HINT
                                             | wx.aui.AUI_MGR_LIVE_RESIZE)
        # self.aui_manager = wx.lib.agw.aui.AuiManager(self, wx.aui.AUI_MGR_ALLOW_FLOATING | wx.aui.AUI_MGR_TRANSPARENT_HINT
        #                                              | wx.aui.AUI_MGR_LIVE_RESIZE)
        self.aui_manager.AddPane(self.code_text, wx.CENTRE, 'Code Text')
        self.aui_manager.AddPane(self.visualiser, wx.TOP, 'Visualiser')
        self.aui_manager.AddPane(self.code_runner, wx.BOTTOM, 'Code Runner')
        self.aui_manager.Update()

        # sizer = wx.BoxSizer(wx.VERTICAL)
        # sizer.Add(self.visualiser, 1, wx.EXPAND)
        # sizer.Add(self.code_text, 1, wx.EXPAND)
        # sizer.Add(self.code_runner, 1, wx.EXPAND)
        # self.SetSizer(sizer)

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
        self.visualiser.set_filetype(filetype)

    def get_file_info(self):
        return self.filename, self.filepath, self.filetype

    def get_current_text(self):
        return self.code_text.GetText()

    def open_visualiser(self):
        self.aui_manager.InsertPane(self.visualiser, self.aui_manager.GetPane(self.visualiser).Show())
        self.aui_manager.Update()

    def window_destroy_event(self, event):
        self.aui_manager.UnInit()
        event.Skip()


# class EditorNotebook(wx.aui.AuiNotebook):
class EditorNotebook(wx.lib.agw.aui.AuiNotebook):

    def __init__(self, *args, agwStyle=wx.lib.agw.aui.aui_constants.AUI_NB_TOP
                 | wx.lib.agw.aui.aui_constants.AUI_NB_TAB_SPLIT
                 | wx.lib.agw.aui.aui_constants.AUI_NB_TAB_MOVE
                 #  | wx.lib.agw.aui.aui_constants.AUI_NB_TAB_FIXED_WIDTH
                 | wx.lib.agw.aui.aui_constants.AUI_NB_CLOSE_ON_ALL_TABS
                 | wx.lib.agw.aui.aui_constants.AUI_NB_SCROLL_BUTTONS
                 | wx.lib.agw.aui.aui_constants.AUI_NB_WINDOWLIST_BUTTON
                 | wx.lib.agw.aui.aui_constants.AUI_NB_MIDDLE_CLICK_CLOSE
                 | wx.lib.agw.aui.aui_constants.AUI_NB_DRAW_DND_TAB, **kwargs):
        super().__init__(*args, **kwargs, agwStyle=agwStyle)

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
