import PySimpleGUI as sg

from src.model.model import Model


class JournalWindow:
    header_list = ['Date', 'From Account', 'To Account', 'Amount', 'Description', 'Account Owner']
    transaction_values: list[list[[str, int, float]]]
    model: Model = None

    def __init__(self, model):
        self.model = model
        self.transaction_values = self.model.get_transaction_values()

        sg.set_options(element_padding=(0, 0))

        self.layout = [[sg.Text("Transactions")],
                       [sg.Table(values=self.format_date(self.transaction_values),
                                 headings=self.header_list,
                                 max_col_width=25,
                                 auto_size_columns=True,
                                 justification='right',
                                 alternating_row_color='darkblue',
                                 num_rows=min(len(self.transaction_values), 20))],
                       [sg.Button("Home")]]

    def make_window(self):
        return sg.Window("General Journal", self.layout, finalize=True, grab_anywhere=False)

    def set_transaction_values(self, transaction_values: list[list[[str, int, float]]]):
        self.transaction_values = transaction_values

    def format_date(self, transaction_values):
        for transaction in transaction_values:
            transaction[1] = transaction[1].strftime("%d-%m-%Y")
        return transaction_values