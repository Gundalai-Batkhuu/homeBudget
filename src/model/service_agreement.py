import datetime

from .event_type import EventType
from .posting_rule import PostingRule


class ServiceAgreement:
    rate: float
    posting_rules: map

    def add_posting_rule(self, event_type: EventType, posting_rule: PostingRule, date: datetime.datetime):
        if self.posting_rules[event_type] is None:
            self.posting_rules[event_type] = []

    def get_posting_rule(self, event_type: EventType, date: datetime.datetime):
        return self.posting_rules[event_type][date]
















