import wx
import wx.stc


class CodeText(wx.stc.StyledTextCtrl):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.init_settings()

    def init_settings(self):
        font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, 'Source Code Pro')
        self.StyleSetFont(wx.stc.STC_STYLE_DEFAULT, font)
        self.StyleSetBackground(wx.stc.STC_STYLE_INDENTGUIDE, wx.Colour(211, 211, 211))
        self.StyleSetForeground(wx.stc.STC_STYLE_INDENTGUIDE, wx.Colour(211, 211, 211))

        self.SetLexer(wx.stc.STC_LEX_PYTHON)
        self.SetMarginType(1, wx.stc.STC_MARGIN_NUMBER)

        self.SetCaretLineVisible(True)
        self.SetAdditionalSelectionTyping(True)

        self._set_default_indentation_settings()
        self._edit_keybinds()

    def _set_default_indentation_settings(self):
        self.SetIndent(4)
        self.SetTabWidth(4)
        self.SetBackSpaceUnIndents(True)
        self.SetTabIndents(True)
        self.SetUseTabs(False)
        self.SetIndentationGuides(True)

    def _edit_keybinds(self):

        # I could `self.CmdKeyClearAll()` and then only bind the keybinds that are necessary

        self.CmdKeyClear(ord('U'), wx.stc.STC_SCMOD_CTRL)
        self.CmdKeyClear(ord('U'), wx.stc.STC_SCMOD_CTRL | wx.stc.STC_SCMOD_SHIFT)
        # self.CmdKeyAssign(65, wx.stc.STC_SCMOD_NORM, lambda: print)

        self.Bind(wx.EVT_KEY_DOWN, self.key_pressed_event)
        self.Bind(wx.EVT_LEFT_DOWN, self.mouse_left_down_event)
        self.Bind(wx.EVT_MOTION, self.mouse_move_event)

    def key_pressed_event(self, event):
        key_code = event.GetKeyCode()
        modifiers = event.GetModifiers()

        if key_code == wx.WXK_RETURN and modifiers == wx.MOD_NONE:
            self.newline_with_indentation()
        else:
            event.Skip()

    def mouse_left_down_event(self, event):
        modifiers = event.GetModifiers()

        self.SetFocus()

        pos = self.PositionFromPoint(event.GetPosition())
        if modifiers == wx.MOD_CONTROL:
            self.AddSelection(pos, pos)
        else:
            self.ClearSelections()
            self.SetSelection(pos, pos)

    def mouse_move_event(self, event):
        modifiers = event.GetModifiers()

        if event.LeftIsDown():
            print('ctrl + mouse drag')
            selection = self.GetMainSelection()
            pos = self.PositionFromPoint(event.GetPosition())
            anchor = self.GetSelectionNAnchor(selection)
            if pos < anchor:
                self.SetSelectionNStart(selection, pos)
            else:
                self.SetSelectionNEnd(selection, pos)
            self.SetSelectionNAnchor(selection, anchor)
            self.SetSelectionNCaret(selection, pos)
        else:
            event.Skip()

    def newline_with_indentation(self):
        indentation = self.GetLineIndentation(self.GetCurrentLine())
        self.NewLine()
        self.AddText(' ' * indentation)
