from asciimatics.widgets import Frame, TextBox, Layout, Divider, Text, \
    Button
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError
from asciimatics.event import KeyboardEvent, MouseEvent
from copy import copy

import sys


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
        self._line = 30
        self._column = 0
        self._start_line = 0
        self._start_column = 0
        self._required_height = height
        self._as_string = as_string
        self._on_change = on_change
        self._log_file = open("test.log", "r")

    def update(self, frame_no):
        self._draw_label()
        self._frame._clear()

        # Clear out the existing box content
        (colour, attr, bg) = self._pick_colours("edit_text")
        line = self._log_file.readline()
        if line:
            self._value.insert(self._line, line)
            self._line += 1

        #self._frame.canvas.print_at(line, 2, self._line, colour, attr, 4)
        self._frame._screen._print_at(line, 2, self._line)
        #if self._line == 20:
        #    self._frame._screen._scroll(-2)

        if self._has_focus:
            self._draw_cursor(
                " " if self._column >= len(self._value[self._line]) else
                self._value[self._line][self._column],
                frame_no,
                self._x + self._offset + self._column  - self._start_column,
                self._y + self._line - self._start_line)

    def process_event(self, event):
        if isinstance(event, KeyboardEvent):
            old_value = copy(self._value)
            if event.key_code == Screen.KEY_UP:
                # Move up one line in text
                #self._line = self._start_line
                self._line -= 1

            elif event.key_code == Screen.KEY_DOWN:
                # Move down one line in text
                if self._line < len(self._value):
                    self._line += 1

            elif event.key_code == Screen.KEY_HOME:
                # Go to the start
                self._line = 0

            elif event.key_code == Screen.KEY_END:
                # Go to the end
                self._line = len(self._value) - 1
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
        self.bbb = TextPrint(35, as_string=False)
        layout.add_widget(self.bbb)
        layout.add_widget(Divider())
        layout2.add_widget(Button("Cancel", self._cancel), 1)
        self.fix()

    @property
    def frame_update_count(self):
        result = 100
        for layout in self._layouts:
            if layout.frame_update_count > 0:
                result = min(result, layout.frame_update_count)
        return result

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