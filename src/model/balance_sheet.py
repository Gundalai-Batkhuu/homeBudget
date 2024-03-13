class BalanceSheet:
    assets = set()
    liabilities = set()

    def __init__(self, assets, liabilities):
        self.assets = assets
        self.liabilities = liabilities

    def get_assets(self):
        return self.assets

    def get_liabilities(self):
        return self.liabilities

    def set_assets(self, assets):
        self.assets = assets

    def set_liabilities(self, liabilities):
        self.liabilities = liabilities

    def add_asset(self, asset):
        self.assets.append(asset)

    def add_liability(self, liability):
        self.liabilities.append(liability)

    def remove_asset(self, asset):
        self.assets.remove(asset)

    def remove_liability(self, liability):
        self.liabilities.remove(liability)

    def get_balance_sheet(self):
        return self