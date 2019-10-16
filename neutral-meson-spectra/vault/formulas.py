import ROOT
import json
import six


class FVault(object):
    def __init__(self):
        super(FVault, self).__init__()
        with open('config/vault/formulas.json') as f:
            self._ledger = json.load(f)

    def func(self, production, version="standard"):
        return self._ledger[production][version]["formula"]

    def tf1(self, production, version="standard"):
        data = self._ledger[production][version]
        func = ROOT.TF1(production, data["formula"], *data["range"])
        func.SetParNames(*data["parameters"])
        for name, value in six.iteritems(data["default"]):
            strname = ROOT.TString(name)
            func.SetParameter(strname, value)
        return func
