import json


class FVault(object):
    def __init__(self):
        super(FVault, self).__init__()
        with open('config/vault/formulas.json') as f:
            self._ledger = json.load(f)

    def func(self, production, version="standard"):
        return self._ledger[production][version]
