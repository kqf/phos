import ROOT
import six
import hashlib
import json


class AnalysisInput(object):
    def __init__(
        self,
        filename,
        listname,
        histname="MassPt",
        pt_range=(0., 20.),
        suffixes=("", "Mix"),
        histnames=None,
        n_events=None,
        prefix="h",
    ):
        super(AnalysisInput, self).__init__()
        self.filename = filename
        self.listname = listname
        self.histname = histname
        self.suffixes = suffixes or ("", )
        self.prefix = prefix
        self.pt_range = tuple(pt_range)
        self.histnames = histnames or [
            "{}{}{}".format(self.prefix, p, self.histname)
            for p in self.suffixes]
        self.n_events = n_events


class DataVault(object):
    def __init__(self, ledger='ledger.json'):
        super(DataVault, self).__init__()
        with open('config/vault/' + ledger) as f:
            self._ledger = json.load(f)

    def _validate_dataset(self, production, version):
        dataset = self.dataset(production, version)

        hsum_nominal = dataset["hsum"]
        filename = dataset["file"]

        hashsum = hashlib.sha256()
        with open(filename, "rb") as f:
            data = f.read()
        hashsum.update(data)
        hsum_real = hashsum.hexdigest()

        msg = "File {0} doesn't match the desired hash {1} but got {2}"
        if hsum_real != hsum_nominal:
            raise IOError(msg.format(filename, hsum_nominal, hsum_real))

    def dataset(self, production, version="latest"):
        return self._ledger[production][version]

    def file(self, production, version="latest"):
        self._validate_dataset(production, version)
        return self.dataset(production, version)["file"]

    def input(self, production, version="latest",
              listname=None, pt_range=None,
              *args, **kwargs):

        filename = self.file(production, version)
        if not listname:
            listname = self.dataset(production, version)['default_selection']

        if not pt_range:
            pt_range = self.dataset(production, version)['pt_range']

        return AnalysisInput(
            filename, str(listname), pt_range=pt_range, *args, **kwargs)


class FVault(object):
    def __init__(self):
        super(FVault, self).__init__()
        with open('config/vault/formulas.json') as f:
            self._ledger = json.load(f)

    def func(self, production, version="standard"):
        return self._ledger[production][version]["formula"]

    def tf1(self, production, version="standard", fixed=False):
        data = self._ledger[production][version]
        func = ROOT.TF1(production, data["formula"], *data["range"])
        func.SetParNames(*data["parameters"])
        for name, value in six.iteritems(data["default"]):
            index = func.GetParNumber(name)
            func.SetParameter(index, value)
            if fixed:
                func.FixParameter(index, value)
        return func
