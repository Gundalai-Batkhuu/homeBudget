from datetime import datetime
from .entry import Entry
from .journal import Journal
from .money import Money
from .entry import EntryType


class Account:
    entries: list
    account_number: int
    name: str
    journal: Journal()
    type: str

    def __init__(self, account_number: int, name: str, type: str):
        self.account_number = account_number
        self.entries = list()
        self.name = name
        self.type = type

    def get_entries(self):
        return self.entries

    def add_entry(self, entry: Entry):
        self.entries.append(entry)

    def balance(self, end_date: datetime):
        result = Money(0)
        for entry in self.entries:
            if entry.get_date() <= end_date.date():
                result.add_amount(entry.get_value().amount)
        return result

    def current_balance(self):
        return round(self.balance(datetime.now()).amount, 2)

    def month_balance(self, month: str, year: str):
        selected_year = int(year)
        selected_month = datetime.strptime(month, "%B").month
        result = Money(0)
        for entry in self.entries:
            if entry.get_date().month == selected_month and entry.get_date().year == selected_year:
                result.add_amount(entry.get_value().amount)
        return result

    def deposits(self, end_date: datetime):
        result = Money(0)
        for entry in self.entries:
            if entry.get_date() <= end_date and entry.get_event_type().type == "Deposit":
                result.add_amount(entry.get_value().amount)
        return result

    def deposits_current(self):
        return self.deposits(datetime.now())

    def withdrawals(self, end_date: datetime):
        result = Money(0)
        for entry in self.entries:
            if entry.get_date() <= end_date and entry.get_event_type().type == "Withdrawal":
                result.add_amount(entry.get_value().amount)
        return result

    def withdrawals_current(self):
        return self.withdrawals(datetime.now())

    def withdraw(self, amount: Money, target, date: datetime
                 ):
        entry_type = EntryType("Withdrawal")
        AccountingTransaction(amount, self, target, date, entry_type, self.journal, "")

    def get_name(self):
        return self.name

    def get_account_entries_for_month(self, month: datetime.month, year: datetime.year) -> list:
        """
        Get all entries for a specific month
        """
        result = []
        for entry in self.entries:
            if entry.get_date().month == month and entry.get_date().year == year:
                result.append(entry)
        return result

    def calculate_account_entries_sum(self, entries):
        """
        Calculate the sum of all entries in the account
        """
        result = Money(0)
        for entry in entries:
            result.add_amount(entry.get_value().amount)
        return result.amount

    def get_entries_sum_for_current_month(self):
        """
        Get the total monetary amount of all transactions for the current month
        :return:
        """
        month = datetime.now().month
        year = datetime.now().year
        return self.calculate_account_entries_sum(
            self.get_account_entries_for_month(month=month, year=year))

    def get_account_entries_sum_for_month(self, month: int, year: int):
        """
        Get the total monetary amount of all transactions for a specific month
        :param month:
        :param year:
        :return: The total monetary amount of all transactions for a specific month
        """
        return self.calculate_account_entries_sum(
            self.get_account_entries_for_month(month=month, year=year))



class AccountingTransaction:
    id: int
    entries = set()
    date: datetime
    from_acc: Account
    to_acc: Account
    money: Money
    description: str
    account_owner: str
    transaction_type: str
    bank_balance: Money

    def __init__(self,
                 transaction_id: int,
                 money: Money,
                 from_acc: Account,
                 to_acc: Account,
                 date: datetime,
                 entry_type: EntryType,
                 description: str,
                 account_owner: str,
                 transaction_type: str,
                 bank_balance: Money
                 ):
        self.id = transaction_id
        self.date = date
        self.from_acc = from_acc
        self.to_acc = to_acc
        self.money = money
        self.description = description
        self.account_owner = account_owner
        self.transaction_type = transaction_type
        self.bank_balance = bank_balance

        neg_amount = money.amount * -1
        from_entry = Entry(date, entry_type, Money(neg_amount))
        from_acc.add_entry(from_entry)
        self.entries.add(from_entry)

        to_entry = Entry(date, entry_type, money)
        to_acc.add_entry(to_entry)
        self.entries.add(to_entry)


    def get_value(self):
        # Form: ['Transaction_id', 'Date', 'From Account', 'To Account', 'Amount', 'Description', 'Account owner', 'Type']
        result = [self.id, self.date, self.from_acc.get_name(), self.to_acc.get_name(), self.money.amount,
                  self.description,
                  self.account_owner, self.transaction_type, self.bank_balance]

        return result

    def get_from_account(self):
        return self.from_acc.get_name()

    def get_to_account(self):
        return self.to_acc.get_name()

    def get_date(self):
        return self.date

    def get_amount(self):
        return self.money.amount

    def get_bank_balance(self):
        return self.bank_balance

    def get_transaction_type(self):
        return self.transaction_type


class AssetAccount(Account):
    pass
    # Additional attributes and methods specific to asset accounts


class LiabilityAccount(Account):
    pass
    # Additional attributes and methods specific to liability accounts


class RevenueAccount(Account):
    pass
    # Additional attributes and methods specific to revenue accounts


class ExpenseAccount(Account):
    pass
    # Additional attributes and methods specific to expense accounts
