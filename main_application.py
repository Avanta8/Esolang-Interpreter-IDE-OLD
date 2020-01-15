import wx

from editor import EditorArea


class App(wx.App):

    def OnInit(self):
        main_window = MainWindow(None, title='Esolang IDE')
        main_window.Show()
        # self.SetTopWindow(main_window)
        return True


class MainWindow(wx.Frame):
    def __init__(self, *args, size=(1080, 720), **kwargs):
        super().__init__(*args, size=size, **kwargs)

        self.create_widgets()

    def create_widgets(self):
        self._create_menubar()
        self.CreateStatusBar()

        self.editor_area = EditorArea(self)

    def _create_menubar(self):
        menubar = wx.MenuBar()

        menus = {
            'File': (
                (wx.ID_NEW, 'New\tCtrl+N', 'New file', self.file_new),
                (wx.ID_OPEN, 'Open\tCtrl+O', 'Open file', self.file_open),
                (wx.ID_SAVE, 'Save\tCtrl+S', 'Save file', self.file_save),
                (wx.ID_SAVEAS, 'Save as\tCtrl+Shift+S', 'Save as', self.file_saveas)
            )
        }

        for title, items in menus.items():
            menu = wx.Menu()
            for id_, label, help_string, handler in items:
                item = menu.Append(id_, label, help_string)
                self.Bind(wx.EVT_MENU, handler, item)
            menubar.Append(menu, title)

        self.SetMenuBar(menubar)

    def file_new(self, event):
        print('file_new')

    def file_open(self, event):
        print('file_open')

    def file_save(self, event):
        print('file_save')

    def file_saveas(self, event):
        print('file_saveas')


def main():
    app = App()
    app.MainLoop()


if __name__ == "__main__":
    main()
