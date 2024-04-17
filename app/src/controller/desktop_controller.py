import src.view.desktop_view.win_accounts as accs
import src.view.desktop_view.win_account as acc
import app.src.view.desktop_view.win_journal as jrn
import src.view.desktop_view.win_homepage as hp
import PySimpleGUI as sg
from src.model.model import Model
from app.src.model.database import connect, close


class WindowController:
    model: Model = None
    account_name: str = ""
    transaction_values: list[list[[str, int, float]]] = [[]]

    win_home = None
    win_accounts = None
    win_journal = None
    win_plot = None
    win_account = None

    def __init__(self, model: Model):
        self.model = model
        self.win_home = hp.HomeWindow(model).make_window()
        self.win_accounts = accs.AccountsWindow(model)
        self.win_journal = jrn.JournalWindow(model)
        self.win_account = acc.AccountWindow(self.account_name, model)

    def run(self):

        while True:
            window, event, values = sg.read_all_windows()

            if event == "Quit" or event == sg.WIN_CLOSED:
                break

            if event == "Journal":
                self.win_journal = jrn.JournalWindow(self.model).make_window()
                self.win_home.hide()

            if event == "Accounts":
                self.win_accounts = accs.AccountsWindow(self.model).make_window()
                self.win_home.hide()

            if window == self.win_journal and (event == 'Home' or event == 'Back'):
                self.win_journal.close()
                self.win_journal = None
                self.win_home.un_hide()

            if window == self.win_accounts and (event == 'Home' or event == 'Back'):
                self.win_accounts.close()
                self.win_accounts = None
                self.win_home.un_hide()

            if event == '-ACCT-LIST-':
                selected_item = values['-ACCT-LIST-'][0] if len(values['-ACCT-LIST-']) > 0 else None
                window['-OUTPUT-'].update(selected_item)
                self.account_name = selected_item
                continue

            if window == self.win_accounts and event == '-ACCOUNT-DETAILS-':
                self.win_accounts.close()
                self.win_accounts = None
                win_account_obj = acc.AccountWindow(self.account_name, self.model)
                win_account_obj.init_account_balance()
                self.win_account = win_account_obj.make_window()

            if window == self.win_account and event == 'Back':
                self.win_account.close()
                self.win_account = None
                self.win_home.un_hide()
                self.win_accounts = accs.AccountsWindow(self.model).make_window()

            if window == self.win_account and event == '-BY-DAY-':
                date = sg.popup_get_date()
                if date:
                    month, day, year = date
                    window['-CAL-DAY-'].update(f"{year}-{month:0>2d}-{day:0>2d}")

            if window == self.win_account and event == '-FILTER-':
                month = values['-MONTH-']
                year = values['-YEAR-']
                self.win_account.close()
                win_account_obj = acc.AccountWindow(self.account_name, self.model)
                win_account_obj.set_account_transaction_values(
                    self.model.get_account_transaction_values_for_month(self.account_name, month, year))
                win_account_obj.set_monthly_account_balance(month, year)
                self.win_account = win_account_obj.make_window()

        self.win_home.close()


def run_desktop_app():
    conn = connect()

    model = Model(conn)
    controller = WindowController(model)
    controller.run()
    close(conn)
