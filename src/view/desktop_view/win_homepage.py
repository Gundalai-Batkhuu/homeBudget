from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg
import matplotlib.pyplot as plt
import matplotlib

from src.model.model import Model


def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg


class HomeWindow:
    model: Model = None

    def __init__(self, model: Model):
        self.model = model
        data = model.get_all_transaction_values_increment_for_current_month()
        x = data['Date']
        y = data['Expenses']
        # Add data label to the last point
        last_value = str(round(data['Expenses'].iloc[-1], 2))
        last_date = data['Date'].iloc[-1].strftime('%d %B')

        self.layout = [[sg.Text("$" + last_value + " as at " + last_date, font=('Helvetica', 16), text_color='black')],
                       [sg.Canvas(key="-CANVAS-")],
                       [sg.Button("Journal")],
                       [sg.Button("Accounts")],
                       [sg.Button("Quit")]]

        self.window = sg.Window("Home", self.layout, finalize=True)

        # Create a plot
        fig = plt.figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(x, y, marker='o', linestyle='-', label='Net Profit')

        # Customize the plot
        ax.set_title('Expenses for this month')
        ax.grid(True)

        # Use matplotlib with tkinter
        matplotlib.use("TkAgg")

        # Add the plot to the window
        draw_figure(self.window["-CANVAS-"].TKCanvas, fig)

    def make_window(self):
        return self.window
