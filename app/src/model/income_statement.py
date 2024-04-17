class IncomeStatement:
    revenues = []
    expenses = []

    def __init__(self, revenues, expenses):
        self.revenues = revenues
        self.expenses = expenses

    def get_revenues(self):
        return self.revenues

    def get_expenses(self):
        return self.expenses

    def set_revenues(self, revenues):
        self.revenues = revenues

    def set_expenses(self, expenses):
        self.expenses = expenses

    def add_revenue(self, revenue):
        self.revenues.append(revenue)

    def add_expense(self, expense):
        self.expenses.append(expense)

    def remove_revenue(self, revenue):
        self.revenues.remove(revenue)

    def remove_expense(self, expense):
        self.expenses.remove(expense)

    def get_income_statement(self):
        return self