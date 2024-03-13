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

    def test_account_names_in_view(self):
        self.assertEqual(self.view.account_names, self.model.ledger.get_account_names())

    def test_account_names_in_home_window(self):
        self.assertEqual(self.view.win_home.account_names, self.model.ledger.get_account_names())

    def test_account_names_in_accounts_window(self):
        self.assertEqual(self.view.win_home.win_accounts.account_names, self.model.ledger.get_account_names())


if __name__ == '__main__':
    unittest.main()