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
        self.assertEqual(self.view.accounts_info, self.model.ledger.get_accounts_info())

    def test_account_names_in_home_window(self):
        self.assertEqual(self.view.win_home.accounts_info, self.model.ledger.get_accounts_info())

    def test_account_names_in_accounts_window(self):
        self.assertEqual(self.view.win_home.win_accounts.accounts_info, self.model.ledger.get_accounts_info())


if __name__ == '__main__':
    unittest.main()