from asciimatics.widgets import Frame, TextBox, Layout, Divider, Text, \
    Button
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError
from asciimatics.event import KeyboardEvent, MouseEvent
from copy import copy

import sys, time

f = open("test.log", "r")

class TextPrintString(Text):
    def update(self, frame_no):
        self._draw_label()
        # Calculate new visible limits if needed.
        width = self._w - self._offset
        self._start_column = max(0, max(self._column - width + 1,
                                        min(self._start_column, self._column)))
        # Render visible portion of the text.
        (colour, attr, bg) = self._pick_colours("edit_text")
        text = self._value[self._start_column:self._start_column + width]
        text += " " * (width - len(text))
        for line in f.readlines():
            self._frame.canvas.print_at(
            line,
            self._x,
            self._y,
            colour, attr, bg)
            self._y += 1


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
        line = f.readline()

        if line:
            self._value.insert(self._line, line)
            self._line += 1

        for i, text in enumerate(self._value):
            if self._start_line <= i < self._start_line + height:
                self._frame.canvas.print_at(
                    text[self._start_column:self._start_column + width],
                    self._x + self._offset + dx,
                    self._y + i + dy - self._start_line,
                    colour, attr, 4)

        # Since we switch off the standard cursor, we need to emulate our own
        # if we have the input focus.
        """
        if self._has_focus:
            self._draw_cursor(
                " " if self._column >= len(self._value[self._line]) else
                self._value[self._line][self._column],
                frame_no,
                self._x + self._offset + self._column  - self._start_column,
                self._y + self._line - self._start_line)
        """
    def process_event(self, event):
        if isinstance(event, KeyboardEvent):
            old_value = copy(self._value)
            if event.key_code in [10, 13]:
                # Split and insert line  on CR or LF.
                self._value.insert(self._line + 1,
                                   self._value[self._line][self._column:])
                self._value[self._line] = self._value[self._line][:self._column]
                self._line += 1
                self._column = 0
            elif event.key_code == Screen.KEY_BACK:
                if self._column > 0:
                    # Delete character in front of cursor.
                    self._value[self._line] = "".join([
                        self._value[self._line][:self._column - 1],
                        self._value[self._line][self._column:]])
                    self._column -= 1
                else:
                    if self._line > 0:
                        # Join this line with previous
                        self._line -= 1
                        self._column = len(self._value[self._line])
                        self._value[self._line] += \
                            self._value.pop(self._line + 1)
            elif event.key_code == Screen.KEY_UP:
                # Move up one line in text
                self._line = max(0, self._line - 1)
                if self._column >= len(self._value[self._line]):
                    self._column = len(self._value[self._line])
            elif event.key_code == Screen.KEY_DOWN:
                # Move down one line in text
                self._line = min(len(self._value) - 1, self._line + 1)
                if self._column >= len(self._value[self._line]):
                    self._column = len(self._value[self._line])
            elif event.key_code == Screen.KEY_LEFT:
                # Move left one char, wrapping to previous line if needed.
                self._column -= 1
                if self._column < 0:
                    if self._line > 0:
                        self._line -= 1
                        self._column = len(self._value[self._line])
                    else:
                        self._column = 0
            elif event.key_code == Screen.KEY_RIGHT:
                # Move right one char, wrapping to next line if needed.
                self._column += 1
                if self._column > len(self._value[self._line]):
                    if self._line < len(self._value) - 1:
                        self._line += 1
                        self._column = 0
                    else:
                        self._column = len(self._value[self._line])
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

class HwView(Frame):
    def __init__(self, screen):
        super(HwView, self).__init__(screen,
                                     screen.height,
                                     screen.width ,
                                     hover_focus=False,
                                     has_border=True,
                                     title="Hardware information")
        layout = Layout([1], fill_frame=True)
        layout2 = Layout([1, 1, 1], fill_frame=False)
        self.add_layout(layout)
        self.add_layout(layout2)
        self.bbb = TextPrint(20, as_string=False)
        layout.add_widget(self.bbb)
        layout2.add_widget(Button("Cancel", self._cancel), 1)
        self.fix()

    @staticmethod
    def _cancel():
        sys.exit(0)

def demo(screen, scene):
    scenes = [Scene([HwView(screen)], -1, name = "HwView")]
    effects = []

    screen.play(scenes, stop_on_resize=True, start_scene=scene)


last_scene = None
while True:
    try:
        Screen.wrapper(demo, catch_interrupt=False, arguments=[last_scene])
        sys.exit(0)
    except ResizeScreenError as e:
        last_scene = e.scene