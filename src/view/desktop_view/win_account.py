import PySimpleGUI as sg
import datetime

from src.model.model import Model
from src.view.desktop_view.view import View


class AccountWindow(View):
    account_name = ""
    transaction_values: list[list[[str, int, float]]] = [[]]
    header_list = ['Date', 'From Account', 'To Account', 'Amount', 'Description', 'Account Owner']
    account_balance: float = 0.0
    months = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]
    current_year = datetime.datetime.now().year
    years = [str(year) for year in range(current_year - 10, current_year + 11)]
    model: Model = None

    def __init__(self, account_name, model: Model):
        super().__init__(model)
        self.model = model
        self.account_name = account_name
        self.transaction_values = self.model.get_account_transaction_values(account_name)

    def set_layout(self):
        col1 = sg.Column([[sg.Text("Transactions")], [sg.Table(values=self.format_date(self.transaction_values),
                                                               headings=self.header_list,
                                                               max_col_width=25,
                                                               auto_size_columns=True,
                                                               justification='right',
                                                               alternating_row_color='darkblue',
                                                               num_rows=min(len(self.transaction_values), 20))],
                          ], pad=(0, 0))

        col2 = sg.Column([
            [sg.Frame('Information:', [[sg.Column([[sg.Text('Account balance:')],
                                                   [sg.Text(self.account_balance)],
                                                   ], size=(235, 350), pad=(0, 0))]])],


                                 [sg.Text("Month:"),
                                  sg.Combo(self.months, default_value="January", key="-MONTH-", readonly=True)],
                                 [sg.Text("Year:"),
                                  sg.Combo(self.years, default_value=str(self.current_year), key="-YEAR-",
                                           readonly=True)],
                                 [sg.Button("Filter", key='-FILTER-')],

        ], pad=(0, 0)),

        return [[sg.Text("Account: " + self.account_name)],
                [col1, col2],
                [sg.Button("Back")]]

    def make_window(self):
        return sg.Window("Account", self.set_layout(), finalize=True)

    def set_account_transaction_values(self, transaction_values: list[list[[str, int, float]]]):
        self.transaction_values = transaction_values

    def set_account_balance(self, account_balance: float):
        self.account_balance = account_balance

    def init_account_balance(self):
        self.account_balance = self.model.get_account_balance(self.account_name)

    def set_monthly_account_balance(self, month: str, year: str):
        self.account_balance = self.model.get_account_balance_for_month(self.account_name, month, year).amount

    def format_date(self, transaction_values):
        for transaction in transaction_values:
            transaction[0] = transaction[0].strftime("%d-%m-%Y")
        return transaction_values
