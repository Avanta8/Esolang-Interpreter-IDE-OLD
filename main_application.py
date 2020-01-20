import os

import wx

import constants
from editor import EditorNotebook


import wx.lib.inspection


class App(wx.App):

    def OnInit(self):
        main_window = MainWindow(None, title='Esolang IDE')
        main_window.Show()
        # self.SetTopWindow(main_window)
        wx.lib.inspection.InspectionTool().Show()
        return True


class MainWindow(wx.Frame):
    def __init__(self, *args, size=(1080, 720), **kwargs):
        super().__init__(*args, size=size, **kwargs)

        self.create_widgets()

    def create_widgets(self):
        self._create_menubar()
        self.CreateStatusBar()

        self._create_file_dialogs()

        self.editor_notebook = EditorNotebook(self)
        sizer = wx.BoxSizer()
        sizer.Add(self.editor_notebook, 1, wx.EXPAND)
        self.SetSizer(sizer)

    def _create_menubar(self):
        menubar = wx.MenuBar()

        menus = {
            'File': (
                (wx.ID_NEW, 'New\tCtrl+N', 'Create a new file', self.file_new),
                (wx.ID_OPEN, 'Open\tCtrl+O', 'Open an existing file', self.file_open),
                (wx.ID_SAVE, 'Save\tCtrl+S', 'Save the current file', self.file_save),
                (wx.ID_SAVEAS, 'Save as\tCtrl+Shift+S', 'Save as a new file', self.file_saveas),
            ),
            'Run': (
                (wx.ID_ANY, 'Run code\tCtrl+B', 'Execute code', self.run_code),
                (wx.ID_ANY, 'Open visualiser\tCtrl+Shift+B', 'Open Visualiser', self.open_visualiser),
            ),
        }

        for title, items in menus.items():
            menu = wx.Menu()
            for id_, label, help_string, handler in items:
                item = menu.Append(id_, label, help_string)
                self.Bind(wx.EVT_MENU, handler, item)
            menubar.Append(menu, title)

        self.SetMenuBar(menubar)

    def _create_file_dialogs(self):
        wildcard = 'Brainfuck (*.b)|*.b|' \
                   'Text file (*.txt)|*.txt|' \
                   'All files (*.*)|*.*'

        self.open_dialog = wx.FileDialog(
            self, message='Choose a file',
            wildcard=wildcard,
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
        )

        self.save_dialog = wx.FileDialog(
            self, message='Save file as...',
            wildcard=wildcard,
            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
        )

    def file_new(self, event):
        self.create_new_page()

    def file_open(self, event):
        if self.open_dialog.ShowModal() == wx.ID_CANCEL:
            return
        filepath = self.open_dialog.GetPath()
        text = self._read_file(filepath)

        self.create_new_page(*self._parse_filepath(filepath), text=text)

    def file_save(self, *event):
        current_file_info = self.editor_notebook.get_current_file_info()
        text = self.editor_notebook.get_current_text()
        if current_file_info is None:
            return

        _, filepath, _ = current_file_info
        if filepath is None:
            self.file_saveas()
        else:
            self._write_file(filepath, text)

    def file_saveas(self, *event):
        if self.save_dialog.ShowModal() == wx.ID_CANCEL:
            return

        filepath = self.save_dialog.GetPath()
        self.set_current_file_info(filepath)

        self.file_save()

    def create_new_page(self, filename=None, filepath=None, filetype=constants.FileTypes.none, text=''):
        self.editor_notebook.new_page(filename=filename, filepath=filepath, filetype=filetype, text=text)

    def set_current_file_info(self, filepath):
        args = self._parse_filepath(filepath)
        self.editor_notebook.set_current_file_info(*args)

    def _read_file(self, filepath):
        """Read `filepath` and return the contents."""
        with open(filepath, 'r') as file:
            read = file.read()
        return read

    def _write_file(self, filepath, text):
        """Write `text` to `filepath`."""
        with open(filepath, 'w') as file:
            file.write(text)

    def _parse_filepath(self, filepath):
        """Return filename and filetype"""
        extension = os.path.splitext(filepath)[1]
        filetype = constants.FileTypes.brainfuck if extension == '.b' else constants.FileTypes.none
        filename = os.path.basename(filepath)
        return filename, filepath, filetype

    def run_code(self, event):
        pass

    def open_visualiser(self, event):
        self.editor_notebook.open_visualiser()


def main():
    app = App()
    app.MainLoop()


if __name__ == "__main__":
    main()
