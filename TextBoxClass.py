from asciimatics.widgets import Frame, TextBox, Layout, \
    Button
from asciimatics.screen import Screen
from asciimatics.exceptions import NextScene
from asciimatics.event import KeyboardEvent, MouseEvent
from copy import copy


class TextPrint(TextBox):
    def __init__(self, height, label=None, name=None, as_string=False,
                 on_change=None):
        """
        :param height: The required number of input lines for this TextBox.
        :param label: An optional label for the widget.
        :param name: The name for the TextBox.
        :param as_string: Use string with newline separator instead of a list
            for the value of this widget.
        :param on_change: Optional function to call when text changes.
        """
        super(TextBox, self).__init__(name)
        self._label = label
        self._line = 0
        self._column = 0
        self._start_line = 0
        self._start_column = 0
        self._required_height = height
        self._as_string = as_string
        self._on_change = on_change
        #self._log_file = open("test.log", "r")

    def update(self, frame_no):
        self._draw_label()

        # Calculate new visible limits if needed.
        width = self._w - self._offset
        height = self._h
        dx = dy = 0
        self._start_line = max(0, max(self._line - height + 1,
                                      min(self._start_line, self._line)))
        self._start_column = max(0, max(self._column - width + 1,
                                        min(self._start_column, self._column)))
        # Clear out the existing box content
        (colour, attr, bg) = self._pick_colours("edit_text")
        for i in range(height):
            self._frame.canvas.print_at(
                " " * width,
                self._x + self._offset + dx,
                self._y + i + dy,
                colour, attr, 4)
        line = self._log_file.readline()
        if line:
            for i in range(height):
                self._frame.canvas.print_at(line,
                4,
                self._y + i + dy,
                colour, attr, 4)
            self._value.insert(self._line, line)
            self._line += 1
        """
        for i, text in enumerate(self._value):
            if self._start_line <= i < self._start_line + height:
                self._frame.canvas.print_at(
                    text[self._start_column:self._start_column + width],
                    self._x + self._offset + dx,
                    self._y + i + dy - self._start_line,
                    colour, attr, 4)
        """
        # Since we switch off the standard cursor, we need to emulate our own
        # if we have the input focus.
    def process_event(self, event):
        if isinstance(event, KeyboardEvent):
            old_value = copy(self._value)
            if event.key_code == Screen.KEY_UP:
                # Move up one line in text
                self._line = self._start_line
                self._line -= 1

            elif event.key_code == Screen.KEY_DOWN:
                # Move down one line in text
                self._line = min(len(self._value) - 1, self._line + 1)
                if self._column >= len(self._value[self._line]):
                    self._column = len(self._value[self._line])
                self._start_line += 1

            elif event.key_code == Screen.KEY_HOME:
                # Go to the start
                self._line = 0

            elif event.key_code == Screen.KEY_END:
                # Go to the end
                self._line = len(self._value) - 1
            #elif event.key_code >= 32:
                # Insert any visible text at the current cursor position.
            #    self._value[self._line] = chr(event.key_code).join([
            #        self._value[self._line][:self._column],
            #        self._value[self._line][self._column:]])
            #    self._column += 1
            else:
                # Ignore any other key press.
                return event

            # If we got here we might have changed the value...
            if old_value != self._value and self._on_change:
                self._on_change()

        elif isinstance(event, MouseEvent):
            # Mouse event - rebase coordinates to Frame context.
            new_event = self._frame.rebase_event(event)
            if event.buttons != 0:
                if self.is_mouse_over(new_event, include_label=False):
                    self._line = max(0,
                                     new_event.y - self._y + self._start_line)
                    self._line = min(len(self._value) - 1, self._line)
                    self._column = min(
                        len(self._value[self._line]),
                        new_event.x - self._x - self._offset +
                        self._start_column)
                    self._column = max(0, self._column)
                    return
            # Ignore other mouse events.
            return event
        else:
            # Ignore other events
            return event


class SumView(Frame):
    def __init__(self, screen, res_list):
        super(SumView, self).__init__(screen,
                                     screen.height,
                                     screen.width ,
                                     hover_focus=False,
                                     has_border=True,
                                     title="Hardware information")

        self._res_list = res_list
        layout = Layout([1], fill_frame=True)
        layout2 = Layout([1, 1, 1], fill_frame=False)
        self.add_layout(layout)
        self.add_layout(layout2)
        self.bbb = TextPrint(35, as_string=False)
        #layout.add_widget(self.bbb)
        #layout.add_widget(Divider())
        layout2.add_widget(Button("OK", self._ok), 1)
        self.fix()

    def _ok(self):
        raise NextScene("Main")

    def _update(self, frame_no):
        # Reset the canvas to prepare for next round of updates.
        self._clear()

        # Update all the widgets first.
        for layout in self._layouts:
            layout.update(frame_no)

        # Then update any effects as needed.
        for effect in self._effects:
            effect.update(frame_no)

        # Draw any border if needed.
        if self._has_border:
            # Decide on box chars to use.
            tl = u"┌" if self._canvas.unicode_aware else "+"
            tr = u"┐" if self._canvas.unicode_aware else "+"
            bl = u"└" if self._canvas.unicode_aware else "+"
            br = u"┘" if self._canvas.unicode_aware else "+"
            horiz = u"─" if self._canvas.unicode_aware else "-"
            vert = u"│" if self._canvas.unicode_aware else "|"

            # Draw the basic border first.
            (colour, attr, bg) = self.palette["borders"]
            for dy in range(self._canvas.height):
                y = self._canvas.start_line + dy
                if dy == 0:
                    self._canvas.print_at(
                        tl + (horiz * (self._canvas.width - 2)) + tr,
                        0, y, colour, attr, bg)
                elif dy == self._canvas.height - 1:
                    self._canvas.print_at(
                        bl + (horiz * (self._canvas.width - 2)) + br,
                        0, y, colour, attr, bg)
                else:
                    self._canvas.print_at(vert, 0, y, colour, attr, bg)
                    self._canvas.print_at(vert, self._canvas.width - 1, y,
                                          colour, attr, bg)

            # Now the title
            (colour, attr, bg) = self.palette["title"]
            self._canvas.print_at(
                self._title,
                (self._canvas.width - len(self._title)) // 2,
                self._canvas.start_line,
                colour, attr, bg)

            # And now the scroll bar
            if self._canvas.height > 5:
                # Sort out chars
                cursor = u"█" if self._canvas.unicode_aware else "O"
                back = u"░" if self._canvas.unicode_aware else "|"

                # Now draw...
                sb_height = self._canvas.height - 4
                sb_pos = (self._canvas.start_line /
                          (self._max_height - self._canvas.height))
                sb_pos = min(1, max(0, sb_pos))
                sb_pos = max(int(sb_height * sb_pos) - 1, 0)
                (colour, attr, bg) = self.palette["scroll"]
                for dy in range(sb_height):
                    y = self._canvas.start_line + dy + 2
                    self._canvas.print_at(cursor if dy == sb_pos else back,
                                          self._canvas.width - 1, y,
                                          colour, attr, bg)

            #clear
            #for i in range(2, self._canvas.height - 6):
            #    self._canvas.print_at(
            #        " " * (self._canvas.width - 2), 1, i, 7, bg, bg)

            #self._canvas.print_at("test", self._canvas.width // 2 - 2, 20, 7, attr, bg)
            i = 0
            for x in self._res_list.get_data():
                i += 2
                self._canvas.print_at(x + " " + self._res_list.get_data()[x], self._canvas.width // 2 - 5, i + 5, 7, attr, bg)
            self._res_list.get_data().clear()

        # Now push it all to screen.
        self._canvas.refresh()

        # And finally - draw the shadow
        if self._has_shadow:
            (colour, _, bg) = self.palette["shadow"]
            self._screen.highlight(
                self._canvas.origin[0] + 1,
                self._canvas.origin[1] + self._canvas.height,
                self._canvas.width - 1,
                1,
                fg=colour, bg=bg, blend=50)
            self._screen.highlight(
                self._canvas.origin[0] + self._canvas.width,
                self._canvas.origin[1] + 1,
                1,
                self._canvas.height,
                fg=colour, bg=bg, blend=50)