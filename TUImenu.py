from asciimatics.widgets import Frame, Layout, Divider, Text, \
    Button, TextBox, Widget, CheckBox, Label, RadioButtons
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, NextScene, StopApplication


import os, time, sys

form_data = {}
form_data2 = {}

class LogView(Frame):
    def __init__(self, screen):
        global form_data2
        super(LogView, self).__init__(screen,
                                       screen.height * 1,
                                       screen.width * 1,
                                       hover_focus=True,
                                       title="TPO Log",
                                      data=form_data2)

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
                                       title="Test TPO",
                                      data=form_data)
        self._tests_list = tests_list
        layout = Layout([1], fill_frame=True)
        self.add_layout(layout)

        self._start_button = Button("Start", self._start)

        layout.add_widget(Label("Available tests"))
        layout.add_widget(Divider())
        for x in tests_list:
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
            if (key not in form_data) or (form_data[key] != value):
                changed = True
                break
        self._start_button.disabled = not changed

    def _start(self):
        global form_data2
        for key, value in self.data.items():
            form_data2[key] = value
            print(key, value)
        self.save()
        raise NextScene("LogView")

    @staticmethod
    def _quit():
        raise StopApplication("User pressed quit")

def demo(screen, scene):

    scenes = [
        Scene([ListView(screen, py_list)], -1, name="Main"),
        Scene([LogView(screen)], -1, name="LogView")
    ]

    screen.play(scenes, stop_on_resize=True, start_scene=scene)


files = os.listdir()
py_list = [x for x in files if x.endswith('.py')]

for x in py_list:
    form_data[x] = True
print(form_data)

last_scene = None
while True:
    try:
        Screen.wrapper(demo, catch_interrupt=False, arguments=[last_scene])
        sys.exit(0)
    except ResizeScreenError as e:
        last_scene = e.scene
