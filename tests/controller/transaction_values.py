import unittest
from src.main.Controller import Controller
from src.main.Model.Model import Model
from src.main.Controller.WindowController import WindowController


class TestAccountNames(unittest.TestCase):
    def setUp(self):
        self.view = WindowController()
        self.model = Model()
        controller = Controller(self.view, self.model)
        self.view.set_controller(controller)
        self.view.run()

    def test_account_transaction_values(self):
        self.assertEqual(self.view.win_account.transaction_values, self.model.journal.get_account_transaction_values(self.view.win_account.account_name))


if __name__ == '__main__':
    unittest.main()