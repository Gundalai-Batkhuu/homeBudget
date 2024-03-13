from src.model import database as db
from src.model.account import AccountingTransaction
from src.model.journal import Journal
from src.model.ledger import Ledger
from src.model.money import Money

class Model:
    journal = Journal()
    account_names: list
    transaction_values: list[list[[str, int, float]]] = [[]]
    conn = None
    ledger = None

    def __init__(self, conn):
        self.conn = conn
        df = db.fetch_data_from_db(conn)

        self.set_account_names()

        self.ledger = Ledger(self.account_names)
        for index, row in df.iterrows():
            value = "Debit" if row["amount"] < 0 else "Credit"
            self.journal.add_transaction(AccountingTransaction(Money(row["amount"]),
                                                               self.ledger.get_account(row["credit_account"]),
                                                               self.ledger.get_account(row["debit_account"]),
                                                               row["date"],
                                                               row["credit_account"],
                                                               self.journal,
                                                               row["description"],
                                                               row["member_id"],
                                                               row["type"]
                                                               ))
    def get_account_names(self):
        return self.account_names

    def get_transaction_values(self):
        return self.journal.get_transactions_values()

    def get_all_transaction_values_increment_for_current_month(self):
        return self.journal.get_all_transaction_values_increment_for_current_month()

    def get_account_transaction_values_increment_for_current_month(self, account_name: str):
        return self.journal.get_account_transaction_values_increment_for_current_month(account_name)

    def get_account_total_expense_for_current_month(self, account_name: str):
        return self.journal.get_account_total_expense_for_current_month(account_name)

    def get_all_accounts_total_expense_for_current_month(self, account_names) -> list[list]:
        return self.journal.get_all_account_total_expense_for_current_month(account_names)

    def get_account_transaction_values(self, account_name: str):
        return self.journal.get_account_transaction_values(account_name)

    def get_account_balance(self, account_name: str):
        return self.ledger.get_account(account_name).current_balance()

    def get_account_transaction_values_for_month(self, account_name: str, month: str, year: str):
        return self.journal.get_account_transaction_values_for_month(account_name, month, year)

    def get_account_balance_for_month(self, account_name, month, year):
        return self.ledger.get_account(account_name).month_balance(month, year)

    # Implement the 'PUB-SUB' change propagation mechanism if model has multiple views using the same data

    def set_account_names(self):
        self.account_names = db.get_account_names(self.conn)

    def get_account_proportions_for_current_month(self):
        return self.journal.get_account_proportions_for_current_month(self.account_names)

    def get_current_bank_balance(self):
        return self.ledger.get_account("Cash").current_balance()





