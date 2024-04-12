import PySimpleGUI as sg
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib

from src.model.model import Model


def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg


class AccountsWindow:
    account_names: list
    account_name = ""
    model: Model = None
    accounts_total_expense_for_current_month: dict
    table_header = ["Account", "Amount", "Date"]
    pie_chart_data: list[list]

    def __init__(self, model: Model):
        self.model = model
        self.account_names = self.model.get_accounts_info()
        self.accounts_total_expense_for_current_month = model.get_all_account_total_transaction_value_for_month_by_type("Expense")
        self.pie_chart_data = model.get_account_transaction_proportions_for_month_by_type("Expense")

        canvas_column = sg.Column([
            [sg.Canvas(key="-CANVAS-")]
            ], pad=(0, 0))

        accounts_column = sg.Column([
            [sg.Listbox(values=self.account_names, key='-ACCT-LIST-', size=(15, 20), enable_events=True)],
            [sg.Button('Open account details', key='-ACCOUNT-DETAILS-')]
            ], pad=(0, 0))

        expenses_column = sg.Column([[sg.Table(values=self.accounts_total_expense_for_current_month,
                                    headings=self.table_header,
                                    max_col_width=25,
                                    auto_size_columns=True,
                                    justification='right',
                                    alternating_row_color='darkblue',
                                    num_rows=min(len(self.accounts_total_expense_for_current_month), 20))]], pad=(0, 0))
        self.layout = [[canvas_column, expenses_column, accounts_column, ], [sg.Button("Home")],
                       [sg.Text('Selected item: '), sg.Text(size=(30, 1), key='-OUTPUT-')]]

        # Prepare data
        data = pd.DataFrame(self.pie_chart_data, columns=['Labels', 'Sizes'])
        labels = data['Labels']
        sizes = data['Sizes']

        # Create a plot
        self.fig = plt.figure(figsize=(5, 4), dpi=100)
        ax = self.fig.add_subplot(111)

        # Create the pie chart using ax.pie()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)

        # Set aspect ratio and title
        ax.axis('equal')

        # Use matplotlib with tkinter
        matplotlib.use("TkAgg")

    def make_window(self):
        window = sg.Window("Accounts", self.layout, finalize=True)
        draw_figure(window["-CANVAS-"].TKCanvas, self.fig)
        return window

    def set_account_names(self, account_names: list):
        self.account_names = account_names
