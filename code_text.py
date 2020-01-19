import wx
import wx.stc

import constants
import lexers


class CodeText(wx.stc.StyledTextCtrl):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.syntax_styler = SyntaxStyler(self)

        self.init_settings()

    def init_settings(self):
        font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, 'Source Code Pro')
        self.StyleSetFont(wx.stc.STC_STYLE_DEFAULT, font)
        self.StyleSetBackground(wx.stc.STC_STYLE_INDENTGUIDE, wx.Colour(211, 211, 211))
        self.StyleSetForeground(wx.stc.STC_STYLE_INDENTGUIDE, wx.Colour(211, 211, 211))

        self.SetLexer(wx.stc.STC_LEX_CONTAINER)
        self.Bind(wx.stc.EVT_STC_STYLENEEDED, self.syntax_styler.style_needed)

        self.SetMarginType(1, wx.stc.STC_MARGIN_NUMBER)
        self.SetMarginWidth(1, 50)

        self.SetCaretLineVisible(True)
        self.SetCaretLineBackground(wx.Colour(245, 245, 245))
        # self.SetCaretLineBackAlpha(50)
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
            print('Mouse drag')
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

    def set_filetype(self, filetype):
        self.syntax_styler.set_filetyle(filetype)


class SyntaxStyler:

    def __init__(self, textctrl):

        self.filetype_to_stylefunc = {
            constants.FileTypes.none: self.no_style,
            constants.FileTypes.brainfuck: self.brainfuck_style,
        }

        self.textctrl = textctrl
        self.filetype = constants.FileTypes.none
        self.no_style()

    def style_needed(self, event):
        self._lexer.style_text(event)

    def set_filetyle(self, filetype):
        if filetype is self.filetype:
            return

        self.filetype = filetype

        self.filetype_to_stylefunc[self.filetype]()

        # self.textctrl.Colourise(0, 100)
        # self.textctrl.SetLexer(wx.stc.STC_LEX_CONTAINER)

    def no_style(self):
        self._lexer = lexers.BaseLexer()

    def brainfuck_style(self):
        self._lexer = lexers.BrainfuckLexer()

        foreground = (
            (lexers.BrainfuckLexer.STYLE_PAREN, wx.Colour(255, 0, 0)),  # red
            (lexers.BrainfuckLexer.STYLE_IO, wx.Colour(0, 0, 255)),  # blue
            (lexers.BrainfuckLexer.STYLE_CELL, wx.Colour(0, 150, 0)),  # green
            (lexers.BrainfuckLexer.STYLE_POINTER, wx.Colour(170, 0, 150)),  # purple
            (lexers.BrainfuckLexer.STYLE_COMMENT, wx.Colour(120, 120, 120)),  # grey
        )

        for style, colour in foreground:
            self.textctrl.StyleSetForeground(style, colour)
