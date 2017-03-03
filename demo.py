from asciimatics.widgets import Frame, Layout, Divider, \
    Button, CheckBox, Label, ListBox, Widget
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, NextScene, StopApplication
from hw_info import hw_info

#own class base on TextBox class from asciimatics for output
from TextBoxClass import OutView

import subprocess

import os, sys, logging, time
logging.basicConfig(format=u'[%(asctime)s]  %(message)s', level=logging.DEBUG, filename=u'mylog.log')


class ArrayScript(object):
    def __init__(self):
        self.files = os.listdir("debug_scripts\\")
        self.py_list = [x for x in self.files if x.endswith('.py')]
        self.form_data = {}
        for x in self.py_list:
            self.form_data[x] = False

    def get_form_data(self):
        return self.form_data

    def update(self, details):
        self.form_data = details.copy()


class MainView(Frame):
    def __init__(self, screen):
        super(MainView, self).__init__(screen,
                                       screen.height * 1,
                                       screen.width * 1,
                                       hover_focus=True,
                                       title="Testing software")

        layout2 = Layout([1, 1, 1], fill_frame=False)

        self.add_layout(layout2)
        layout2.add_widget(Label("Select an option"), 1)

        self.init_values = [("Hardware information", 0), ("Functional tests", 1), ("Logging", 2)]

        self._list_view = ListBox(4, self.init_values, on_change=self._on_pick)
        layout2.add_widget(self._list_view, 1)
        layout2.add_widget(Divider())

        layout = Layout([1, 1], fill_frame=False)
        self.add_layout(layout)
        self._ok_button = Button("OK", self._ok_button)

        layout.add_widget(self._ok_button)
        layout.add_widget(Button("Quit", self._quit), 1)

        self.fix()
        self._on_pick()

    def _on_pick(self):
        self._ok_button.disabled = self._list_view.value is None

    def _ok_button(self):
        if self._list_view.options[self._list_view.value][0] == "Hardware information":
            raise NextScene("HwView")
        elif self._list_view.options[self._list_view.value][0] == "Functional tests":
            raise NextScene("ListView")
        elif  self._list_view.options[self._list_view.value][0] == "Logging":
            raise NextScene("Output")


    @staticmethod
    def _quit():
        sys.exit(0)


class LogView(Frame):
    def __init__(self, screen):
        super(LogView, self).__init__(screen,
                                       screen.height * 1,
                                       screen.width *  2 // 3,
                                       hover_focus=True,
                                       title="TPO Log")

        self._screen = screen
        #self._screen.print_at("Hello world", 3, 3)
        self.f = open("test.log", "rb")
        layout = Layout([1], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(Label("It`s LOG"))
        layout.add_widget(Button("Cancel", self._cancel))
        self._screen.height = 300 #base buf size windows cmd
        self._dy = 0
        self._start_line = 0

    def _cancel(self):
        self.save()
        raise NextScene("Main")

    def _update(self, frame_no):
        # Reset the canvas to prepare for next round of updates.
        self._clear()
        self.canvas._start_line = 0

        for layout in self._layouts:
            layout.update(frame_no)

        # Then update any effects as needed.
        for effect in self._effects:
            effect.update(frame_no)
        print("test")
        line = self.f.readline()
        o = self._screen._stdout
        p = self._screen._stdin
        sys.stdout = p
        #o.WriteConsole(line)
        self._screen.print_at(line.decode("CP1251"), 10, 10)
        self._dy += 1


class HwView(Frame):
    def __init__(self, screen, hw_list):
        super(HwView, self).__init__(screen,
                                     screen.height * 1,
                                     screen.width * 1,
                                     hover_focus=True,
                                     title="Hardware information")

        self._hw_list = hw_list
        self.data = self._hw_list._get_data()
        layout = Layout([1, 1, 1], fill_frame=False)

        layout2 = Layout([1, 1, 1], fill_frame=False)

        self.add_layout(layout)
        self.add_layout(layout2)

        self._start_button = Button("Start", self._start)
        self._start_button.disabled = False
        for x in self.data:
            layout.add_widget(CheckBox(name=x, text=x, on_change=self._add), 1)

        layout2.add_widget(self._start_button)
        layout2.add_widget(Button("Cancel", self._cancel), 2)
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
        print("ok")
        self._hw_list._update(self.data)
        raise StopApplication("pause")
        #raise NextScene("Output")

    @staticmethod
    def _cancel():
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
        layout.add_widget(Button("Cancel", self._cancel))
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
        self._tests_list.update(self.data)
        self._start_button.disabled = not changed

    def _start(self):
        #for key in self._tests_list.get_form_data():
        #    if self._tests_list.get_form_data()[key] is True:
        #        logging.debug(u'Call script: ' + key)
        #       self._screen._print_at("test string", 2, 15)
        #        f1 = call_script(key, self._screen._stdout)

        #self.save()
        self._tests_list.update(self.data)
        raise StopApplication("User pressed quit")
        #raise NextScene("LogView")

    @staticmethod
    def _cancel():
        raise NextScene("Main")


def call_script(name):
    with subprocess.Popen("python debug_scripts\\" + name + " > main.log",
                          stdin=subprocess.DEVNULL, stdout=subprocess.PIPE) as process:
        print("\nSTART: " + name)

        #output.WriteConsole(process.stdout.read().decode("CP1251"))
        log_subprocess_output(process.stdout)
        return process.stdout


def log_subprocess_output(pipe):
    for line in iter(pipe.read, b''): # b'\n'-separated lines
        logging.info(line.decode('CP866'))
        print(line.decode('CP866'))


def demo(screen, scene, scripts, hw_list):
    scenes = [
        Scene([MainView(screen)], -1, name="Main"),
        Scene([OutView(screen, hw_list)], -1, name="Output"),
        Scene([HwView(screen, hw_list)], -1, name = "HwView"),
        Scene([ListView(screen, scripts)], -1, name="ListView"),
        Scene([LogView(screen)], -1, name="LogView"),
    ]

    screen.play(scenes, stop_on_resize=True, start_scene=scene)


def main():
    scripts = ArrayScript()
    hw = hw_info()

    last_scene = None

    while True:
        try:
            logging.debug(u'START SCENE')
            Screen.wrapper(demo, catch_interrupt=False, arguments=[last_scene, scripts, hw])
            #Screen.close()

            os.system("cls")
            #update functional test list after call ListView and go test
            for key in scripts.get_form_data():
                if scripts.get_form_data()[key]:
                    try:
                        logging.debug(u'Call script: ' + key)
                        call_script(key)
                        scripts.get_form_data()[key] = False
                        print("End Test\n")
                    except:
                        print("Test", key, "Failed")

            #update hw_list after call HwView and go test
            count = 0
            for i in hw._get_data():
                if hw._get_data()[i]:
                    try:
                        print(i.upper())
                        eval('hw.' + i + '()')
                        print("\n")
                        hw._get_data()[i] = False
                        print()
                    except:
                        print(i.upper() + "FAILED")
                else:
                    count += 1
            print("Press Enter key")
            print("next", input())

        except ResizeScreenError as e:
            last_scene = e.scene

if __name__ == '__main__':
        main()



