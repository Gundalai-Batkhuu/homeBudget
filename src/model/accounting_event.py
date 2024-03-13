from datetime import datetime

from .customer import Customer
from .event_type import EventType
from .posting_rule import PostingRule


class AccountingEvent:
    rule: PostingRule
    account_number: int
    event_type: EventType
    date: datetime
    customer: Customer
    resulting_entries: set

    def __init__(self, event_type: EventType, date: datetime, customer: Customer):
        self.event_type = event_type
        self.date = date
        self.customer = customer

    def get_customer(self):
        return self.customer

    def process(self):
        pass

    def find_agreement(self, event):
        pass

    def get_account_number(self):
        return self.account_number

    def get_event_type(self):
        return self.event_type

    def get_date(self):
        return self.date

    def find_rule(self):
        return self.rule

    def add_resulting_entry(self, entry):
        self.resulting_entries.add(entry)

