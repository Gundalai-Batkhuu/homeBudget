from decimal import Decimal


class Money:
    amount: Decimal

    def __init__(self, amount: Decimal):
        self.amount = amount

    def add_amount(self, amount: Decimal):
        self.amount += amount

    def get_amount(self) -> Decimal:
        return self.amount
