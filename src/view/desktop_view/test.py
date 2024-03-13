import PySimpleGUI as sg


class Page1:
    def __init__(self):
        layout = [
            [sg.Text("Page 1")],
            [sg.Button("Next")],
            [sg.Input(key='-CAL-DAY-')],
            [sg.CalendarButton('Calendar',
                               close_when_date_chosen=True,
                               target='-CAL-DAY-',
                               location=(0, 0),
                               no_titlebar=False)],
        ]
        self.window = sg.Window("Window with Pages").Layout(layout)


class Page2:
    def __init__(self):
        layout = [
            [sg.Text("Page 2")],
            [sg.Button("Previous"), sg.Button("Next")]
        ]
        self.window = sg.Window("Window with Pages").Layout(layout)


class Page3:
    def __init__(self):
        layout = [
            [sg.Text("Page 3")],
            [sg.Button("Previous")]
        ]
        self.window = sg.Window("Window with Pages").Layout(layout)


class PageManager:
    def __init__(self):
        self.pages = [Page1(), Page2(), Page3()]
        self.current_page = 0
        self.show_current_page()

    def show_current_page(self):
        current_window = self.pages[self.current_page].window
        while True:
            event, _ = current_window.read()
            if event == sg.WIN_CLOSED:
                break
            elif event == "Next":
                self.show_next_page()
            elif event == "Previous":
                self.show_previous_page()
        current_window.close()

    def show_next_page(self):
        self.current_page += 1
        if self.current_page >= len(self.pages):
            self.current_page = len(self.pages) - 1
        self.show_current_page()

    def show_previous_page(self):
        self.current_page -= 1
        if self.current_page < 0:
            self.current_page = 0
        self.show_current_page()


if __name__ == "__main__":
    PageManager()
