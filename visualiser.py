import wx
import wx.stc
import wx.lib.splitter


import constants


class CommandsPanel(wx.Panel):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        self.create_widgets()
        self.create_binds()

    def create_widgets(self):
        # self.SetBackgroundColour('red')

        # sizer = wx.StaticBoxSizer(wx.VERTICAL, self, label='Commands')
        sizer = wx.BoxSizer(wx.VERTICAL)

        buttons = self.create_buttons()
        speed = self.create_speed()
        jump = self.create_jump()

        sizer.Add(buttons, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(speed, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(jump, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(sizer)

    def create_buttons(self):
        self.run_button = wx.Button(self, label='Run')
        self.continue_button = wx.Button(self, label='Continue')
        self.step_button = wx.Button(self, label='Step')
        self.pause_button = wx.Button(self, label='Pause')
        self.back_button = wx.Button(self, label='Back')
        self.stop_button = wx.Button(self, label='Stop')
        self.buttons = [self.run_button, self.step_button,
                        self.pause_button, self.back_button,
                        self.stop_button, self.continue_button]

        for button in self.buttons:
            button.Hide()

        self.buttons_sizer = wx.GridSizer(2, 2, 5)
        self.buttons_sizer.AddMany(((self.run_button, 0, wx.EXPAND),
                                    (self.continue_button, 0, wx.EXPAND),
                                    (self.step_button, 0, wx.EXPAND),
                                    (self.pause_button, 0, wx.EXPAND)))

        self.run_button.Show()
        self.continue_button.Show()
        self.step_button.Show()
        self.pause_button.Show()

        # self.buttons_sizer = wx.GridBagSizer(5, 5)
        # self.buttons_sizer.AddMany((
        #     (self.run_button, (0, 0), (1, 1), wx.EXPAND),
        #     (self.continue_button, (0, 1), (1, 1), wx.EXPAND),
        #     (self.step_button, (1, 0), (1, 1), wx.EXPAND),
        #     (self.pause_button, (1, 1), (1, 1), wx.EXPAND)
        # ))

        sizer = wx.StaticBoxSizer(wx.VERTICAL, self, 'Commands:')
        sizer.Add(self.buttons_sizer, 0, wx.EXPAND)
        return sizer

    def create_speed(self):
        self.speed_slider = wx.Slider(self)
        self.speed_checkbox = wx.CheckBox(self, label='Faster:', style=wx.ALIGN_RIGHT)

        # speed_sizer = wx.BoxSizer(wx.VERTICAL)
        speed_sizer = wx.StaticBoxSizer(wx.VERTICAL, self, 'Runspeed:')
        speed_sizer.AddMany((
            (self.speed_slider, 0, wx.EXPAND),
            (self.speed_checkbox, 0)
        ))

        return speed_sizer

    def create_jump(self):
        jump_label = wx.StaticText(self, label='Steps:')
        self.jump_entry = wx.TextCtrl(self)
        self.forwards_button = wx.Button(self, label='Forwards')
        self.backwards_button = wx.Button(self, label='Backwards')

        entry_sizer = wx.BoxSizer(wx.HORIZONTAL)
        entry_sizer.AddMany((
            (jump_label, 0, wx.ALIGN_CENTRE | wx.LEFT | wx.RIGHT, 5),
            (self.jump_entry, 1, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, 5)
        ))

        buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
        buttons_sizer.AddMany((
            (self.backwards_button, 1),
            (self.forwards_button, 1)
        ))

        jump_sizer = wx.StaticBoxSizer(wx.VERTICAL, self, 'Jump:')
        jump_sizer.AddMany((
            (entry_sizer, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5),
            (buttons_sizer, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)
        ))

        return jump_sizer

    def create_binds(self):
        pass


class IOPanel(wx.Panel):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        self.create_widgets()

    def create_widgets(self):
        self.SetBackgroundColour('blue')

        # self.input_text = wx.stc.StyledTextCtrl(self)
        self.input_text = wx.TextCtrl(self, style=wx.TE_PROCESS_TAB | wx.TE_MULTILINE | wx.HSCROLL)
        self.output_text = wx.TextCtrl(self, style=wx.TE_PROCESS_TAB | wx.TE_MULTILINE | wx.HSCROLL | wx.TE_READONLY)
        self.error_text = wx.TextCtrl(self, style=wx.TE_READONLY, value='hi im error text' * 100)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddMany((
            (self.input_text, 1, wx.EXPAND),
            (self.output_text, 1, wx.EXPAND),
            (self.error_text, 0, wx.EXPAND)
        ))
        self.SetSizer(sizer)


class VisualiserPanel(wx.Panel):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        self.create_widgets()

    def create_widgets(self):
        raise NotImplementedError


class NoVisualiserPanel(VisualiserPanel):
    def create_widgets(self):
        self.SetBackgroundColour('Black')


class BrainfuckVisualiserPanel(VisualiserPanel):
    def create_widgets(self):
        self.SetBackgroundColour('Green')


class Visualiser(wx.lib.splitter.MultiSplitterWindow):

    filetype_to_visualiser = {
        constants.FileTypes.none: NoVisualiserPanel,
        constants.FileTypes.brainfuck: BrainfuckVisualiserPanel,
    }

    def __init__(self, parent, id=-1, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.SP_LIVE_UPDATE, name='multiSplitter'):
        super().__init__(parent, id=id, pos=pos, size=size, style=style, name=name)

        self.SetMinimumPaneSize(10)

        self.create_widgets()

    def create_widgets(self):
        self.visualiser_panel = NoVisualiserPanel(self)
        self.commands_panel = CommandsPanel(self)
        self.io_panel = IOPanel(self)

        self.AppendWindow(self.visualiser_panel)
        self.AppendWindow(self.commands_panel)
        self.AppendWindow(self.io_panel)

    def set_filetype(self, filetype):
        visualiser_type = self.filetype_to_visualiser[filetype]
        if isinstance(self.visualiser_panel, visualiser_type):
            return

        old_visualiser = self.visualiser_panel

        self.visualiser_panel = visualiser_type(self)

        self.ReplaceWindow(old_visualiser, self.visualiser_panel)

        old_visualiser.Destroy()
