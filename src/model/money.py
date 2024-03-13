class Money:
    amount = 0.0

    def __init__(self, amount: float):
        self.amount = amount

    def add_amount(self, amount: float):
        self.amount += amount

    def get_amount(self) -> float:
        return self.amount
