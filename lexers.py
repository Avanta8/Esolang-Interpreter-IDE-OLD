class BaseLexer:

    def style_text(self, event):
        pass


class BrainfuckLexer(BaseLexer):
    
    STYLE_PAREN = 1
    STYLE_IO = 2
    STYLE_POINTER = 3
    STYLE_CELL = 4
    STYLE_COMMENT = 5

    def style_text(self, event):
        textctrl = event.GetEventObject()

        last_styled_pos = textctrl.GetEndStyled()

        line = textctrl.LineFromPosition(last_styled_pos)
        start_pos = textctrl.PositionFromLine(line)
        end_pos = event.GetPosition()

        textctrl.StartStyling(start_pos, 0x1f)

        # Refactor this. Probably use a dictionary to store {charcode: style}.
        while start_pos < end_pos:
            char = chr(textctrl.GetCharAt(start_pos))
            if char in '[]':
                style = self.STYLE_PAREN
            elif char in ',.':
                style = self.STYLE_IO
            elif char in '<>':
                style = self.STYLE_POINTER
            elif char in '-+':
                style = self.STYLE_CELL
            else:
                style = self.STYLE_COMMENT

            textctrl.SetStyling(1, style)
            start_pos += 1
