import ROOT
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import make_pipeline
import pandas as pd
import plotting
ROOT.TH1.AddDirectory(False)
filepath = "../../../neutral-meson-spectra/" \
    "input-data/data/LHC16/trigger_qa/iteration2/LHC16g-pass1.root"


def from_list(histname, lst, get=False):
    def reader(index):
        if get:
            return lst.Get("{}{}".format(histname, str(index)))
        return lst.FindObject("{}{}".format(histname, str(index)))
    return reader


class HistReader(BaseEstimator, TransformerMixin):
    def __init__(self, in_col, out_col,
                 filepath, pattern, listpath=None):
        self.in_col = in_col
        self.out_col = out_col
        self.filepath = filepath
        self.pattern = pattern
        self.listpath = listpath

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        infile = ROOT.TFile(self.filepath)
        lst = infile.Get(self.listpath) if self.listpath else infile
        if self.in_col == "index":
            X[self.out_col] = X.index.map(from_list(self.pattern, lst, True))
            return X
        X[self.out_col] = X[self.in_col].apply(from_list(self.pattern, lst))
        return X


class EmptyBinRemover(BaseEstimator, TransformerMixin):
    def __init__(self, in_col, out_col):
        super(EmptyBinRemover, self).__init__()
        self.in_col = in_col
        self.out_col = out_col

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X[self.out_col] = X[self.in_col].apply(self.remove_empty_runs)
        return X

    @staticmethod
    def remove_empty_runs(hist):
        runs, counts = [], []
        for i in range(1, hist.GetNbinsX() + 1):
            if not hist.GetBinContent(i) > 0:
                continue
            runs.append(hist.GetBinCenter(i))
            counts.append(hist.GetBinContent(i))
        reduced = ROOT.TH1F(
            hist.GetName() + "_reduced",
            hist.GetTitle(),
            len(runs), 0, len(runs))

        for i, (r, c) in enumerate(zip(runs, counts)):
            reduced.SetBinContent(i + 1, c)
            reduced.GetXaxis().SetBinLabel(i + 1, str(int(r)))
        return reduced


class AcceptanceScaler(BaseEstimator, TransformerMixin):

    def __init__(self, in_cols, out_col):
        self.in_cols = in_cols
        self.out_col = out_col

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X[self.out_col] = X[self.in_cols].apply(
            lambda x: self.scale(*x), axis=1)
        return X

    @staticmethod
    def scale(hist, badmap):
        if not badmap:
            print "No badmap found for ", hist.GetName()
            return hist
        bad_channels = badmap.GetEntries()
        all_channels = badmap.GetNbinsX() * badmap.GetNbinsY()

        scaled = hist.Clone("{}_acceptance".format(hist.GetName()))
        scaled.SetTitle("{} scaled for acceptance".format(hist.GetTitle()))
        scaled.Scale(1. / (all_channels - bad_channels))
        return scaled


class AverageScaler(BaseEstimator, TransformerMixin):
    def __init__(self, in_col, out_col, info=None):
        self.in_col = in_col
        self.out_col = out_col
        self.info = info

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        average = self.average(X[self.in_col])
        payload = pd.DataFrame(
            [{
                self.out_col: average,
                "name": "average"
            }],
            index=["average"])
        return X.append(payload, sort=True)

    @staticmethod
    def average(hists):
        total = hists[0].Clone("average")
        total.Reset()
        for hist in hists:
            total.Add(hist)
        total.Scale(1. / len(hists))
        return total


def main(nmodules=4):
    badmap_fname = "BadMap_LHC16-updated.root"
    hist, lst = "hRunMatchedTriggers", "PHOSTriggerQAResultsL0"
    analysis = make_pipeline(
        HistReader("name", "raw", filepath, hist, lst),
        HistReader("index", "badmap", badmap_fname, "PHOS_BadMap_mod"),
        EmptyBinRemover("raw", "cleaned"),
        AcceptanceScaler(["cleaned", "badmap"], "scaled"),
        AverageScaler("scaled", "scaled")
    )

    outputs = pd.DataFrame(index=map(str, range(1, nmodules + 1)))
    outputs["name"] = outputs.index.map("SM{}".format)
    outputs = analysis.transform(outputs)
    plotting.plot(outputs["scaled"], outputs["name"])


if __name__ == '__main__':
    main()
