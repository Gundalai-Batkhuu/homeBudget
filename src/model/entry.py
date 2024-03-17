from datetime import datetime

from .money import Money


class EntryType:
    type: str

    def __init__(self, entry_type: str):
        self.type = entry_type


class Entry:
    date: datetime
    entry_type: EntryType
    money: Money

    def __init__(self, date: datetime, entry_type: EntryType, money: Money):
        self.date = date
        self.entry_type = entry_type
        self.money = money

    def get_value(self) -> Money:
        return self.money

    def get_date(self):
        return self.date

    def get_event_type(self):
        return self.entry_type

