from src.model import account
from src.model.account import Account


class Ledger:
    accounts = set()
    account_names : list

    def __init__(self, account_names: list):
        self.account_names = account_names

        for account in self.account_names:
            self.accounts.add(Account(self.account_names.index(account), account))

    def get_account(self, account_name):
        for account in self.accounts:
            if account.get_name() == account_name:
                return account
        return None

    def get_all_accounts(self):
        return self.accounts

    def add_account(self, account):
        self.accounts.add(account)

    def remove_account(self, account):
        self.accounts.remove(account)

    def print_account_names(self):
        for account in self.accounts:
            print(account.get_name())

    def get_account_names(self):
        names = []
        for account in self.accounts:
            names.append(account.get_name())
        return names

