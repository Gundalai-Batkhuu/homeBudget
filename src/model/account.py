from datetime import datetime
from .entry import Entry
from .journal import Journal
from .money import Money
from .entry import EntryType


class Account:
    entries: set
    account_number: int
    name: str
    journal: Journal()

    def __init__(self, account_number: int, name: str):
        self.account_number = account_number
        self.entries = set()
        self.name = name

    def get_entries(self):
        return self.entries

    def add_entry(self, entry: Entry):
        self.entries.add(entry)

    def balance(self, end_date: datetime):
        result = Money(0)
        for entry in self.entries:
            if entry.get_date() <= end_date.date():
                result.add_amount(entry.get_money().amount)
        return result

    def current_balance(self):
        return round(self.balance(datetime.now()).amount, 2)

    def month_balance(self, month: str, year: str):
        selected_year = int(year)
        selected_month = datetime.strptime(month, "%B").month
        result = Money(0)
        for entry in self.entries:
            if entry.get_date().month == selected_month and entry.get_date().year == selected_year:
                result.add_amount(entry.get_money().amount)
        return result

    def deposits(self, end_date: datetime):
        result = Money(0)
        for entry in self.entries:
            if entry.get_date() <= end_date and entry.get_event_type().type == "Deposit":
                result.add_amount(entry.get_money().amount)
        return result

    def deposits_current(self):
        return self.deposits(datetime.now())

    def withdrawals(self, end_date: datetime):
        result = Money(0)
        for entry in self.entries:
            if entry.get_date() <= end_date and entry.get_event_type().type == "Withdrawal":
                result.add_amount(entry.get_money().amount)
        return result

    def withdrawals_current(self):
        return self.withdrawals(datetime.now())

    def withdraw(self, amount: Money, target, date: datetime
                 ):
        entry_type = EntryType("Withdrawal")
        AccountingTransaction(amount, self, target, date, entry_type, self.journal, "")

    def get_name(self):
        return self.name


class AccountingTransaction:
    entries = set()
    date: datetime
    from_acc: Account
    to_acc: Account
    money: Money
    description: str
    account_owner: str
    transaction_type: str

    def __init__(self, money: Money,
                 from_acc: Account,
                 to_acc: Account,
                 date: datetime,
                 entry_type: EntryType,
                 journal: Journal,
                 description: str,
                 account_owner: str,
                 transaction_type: str
                 ):
        self.date = date
        self.from_acc = from_acc
        self.to_acc = to_acc
        self.money = money
        self.description = description
        self.account_owner = account_owner
        self.transaction_type = transaction_type

        neg_amount = money.amount * -1
        from_entry = Entry(date, entry_type, Money(neg_amount))
        from_acc.add_entry(from_entry)
        self.entries.add(from_entry)

        to_entry = Entry(date, entry_type, money)
        to_acc.add_entry(to_entry)
        self.entries.add(to_entry)

        journal.add_transaction(self)

    def get_value(self):
        # Form: ['Date', 'From Account', 'To Account', 'Amount', 'Description', 'Account owner', 'Type']
        result = [self.date, self.from_acc.get_name(), self.to_acc.get_name(), self.money.amount, self.description,
                  self.account_owner, self.transaction_type]

        return result

    def get_from_account(self):
        return self.from_acc.get_name()

    def get_to_account(self):
        return self.to_acc.get_name()

    def get_date(self):
        return self.date


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
