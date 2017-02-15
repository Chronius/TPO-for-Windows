from asciimatics.widgets import Frame, Layout, Divider, Text, \
    Button, TextBox, Widget, CheckBox, Label, RadioButtons
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, NextScene, StopApplication


import os, time, sys

form_data2 = {}
class ArrayScript(object):
    def __init__(self):
        self.files = os.listdir()
        self.py_list = [x for x in self.files if x.endswith('.py')]
        self.form_data = {}
        for x in self.py_list:
            self.form_data[x] = True

    def get_form_data(self):
        print(self.form_data)
        return self.form_data
    def update(self):


class LogView(Frame):
    def __init__(self, screen):
        global form_data2
        super(LogView, self).__init__(screen,
                                       screen.height * 1,
                                       screen.width * 1,
                                       hover_focus=True,
                                       title="TPO Log")

        layout = Layout([1], fill_frame=True)
        self.add_layout(layout)

        for key, value in self.data.items():
            if value is True:
                layout.add_widget(Label(key))
        #        print(key, value)
            #    os.system("python" + key)
        layout.add_widget(Button("Cancel", self._cancel))

        self.fix()
        screen.refresh()

    def _cancel(self):
        self.save()
        raise NextScene("Main")

class ListView(Frame):
    def __init__(self, screen, tests_list):
        super(ListView, self).__init__(screen,
                                       screen.height * 1,
                                       screen.width * 1,
                                       hover_focus=True,
                                       title="Test TPO")
        self._tests_list = tests_list
        layout = Layout([1], fill_frame=True)
        self.add_layout(layout)

        self._start_button = Button("Start", self._start)

        layout.add_widget(Label("Available tests"))
        layout.add_widget(Divider())
        self.data = self._tests_list.get_form_data()
        for x in self.data:
            layout.add_widget(CheckBox(name=x, text=x, on_change=self._add))
        layout.add_widget(Divider())

        layout.add_widget(self._start_button)
        layout.add_widget(Button("Quit", self._quit))
        self._start_button.disabled = False
        self.fix()

    def _add(self):

        changed = False
        self.save()
        for key, value in self.data.items():
            value = False
            if (key not in self.data) or (self.data[key] != value):
                changed = True
                break
        self._start_button.disabled = not changed

    def _start(self):
        self.save()
        raise NextScene("LogView")

    @staticmethod
    def _quit():
        raise StopApplication("User pressed quit")

def demo(screen, scene):

    scenes = [
        Scene([ListView(screen, scripts)], -1, name="Main"),
        Scene([LogView(screen)], -1, name="LogView")
    ]

    screen.play(scenes, stop_on_resize=True, start_scene=scene)


scripts = ArrayScript()
last_scene = None
while True:
    try:
        Screen.wrapper(demo, catch_interrupt=False, arguments=[last_scene])
        sys.exit(0)
    except ResizeScreenError as e:
        last_scene = e.scene
