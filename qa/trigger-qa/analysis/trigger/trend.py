import ROOT
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import make_pipeline
import pandas as pd
import plotting
ROOT.TH1.AddDirectory(False)


def from_list(histname, lst):
    def reader(index):
        try:
            return lst.Get("{}{}".format(histname, str(index)))
        except AttributeError:
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
        X[self.out_col] = X[self.in_col].apply(from_list(self.pattern, lst))
        return X


class EmptyBinRemover(BaseEstimator, TransformerMixin):
    def __init__(self, in_col, out_col):
        super(EmptyBinRemover, self).__init__()
        self.in_col = in_col
        self.out_col = out_col
        self._empty_bins = None

    def fit(self, X, y=None):
        all_bins = X[self.in_col].apply(self.empty_runs)
        duplicated = sum(all_bins.values, [])
        self._empty_bins = sorted(set(duplicated))
        return self

    def transform(self, X):
        X[self.out_col] = X[self.in_col].apply(self.remove_empty_runs)
        return X

    def remove_empty_runs(self, hist):
        runs, counts = [], []
        for i in self._empty_bins:
            runs.append(hist.GetBinCenter(i))
            counts.append(hist.GetBinContent(i))

        reduced = ROOT.TH1F(
            hist.GetName() + "_reduced",
            hist.GetTitle(),
            len(runs), 0, len(runs))

        for i, (r, c) in enumerate(zip(runs, counts)):
            reduced.SetBinContent(i + 1, c)
            reduced.GetXaxis().SetBinLabel(i + 1, str(int(r)))
        reduced.LabelsOption("v")
        return reduced

    @staticmethod
    def empty_runs(hist):
        runs = [
            i for i in range(1, hist.GetNbinsX() + 1)
            if hist.GetBinContent(i) > 0]
        return runs


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
            return hist
        bad_channels = badmap.GetEntries()
        all_channels = badmap.GetNbinsX() * badmap.GetNbinsY()

        scaled = hist.Clone("{}_acceptance".format(hist.GetName()))
        scaled.SetTitle("{} scaled for acceptance".format(hist.GetTitle()))
        scaled.Scale(1. / (all_channels - bad_channels))
        return scaled


class AverageCalculator(BaseEstimator, TransformerMixin):
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


class EventsScaler(EmptyBinRemover):
    def __init__(self, in_col, out_col, raw_col, eventmap):
        super(EventsScaler, self).__init__(raw_col, out_col)
        self.input = in_col
        self.out_col = out_col
        self.eventmap = eventmap
        self._eventmap_cleaned = None

    def fit(self, X, y=None):
        super(EventsScaler, self).fit(X, y)
        self._eventmap_cleaned = self.remove_empty_runs(self.eventmap)
        return self

    def transform(self, X):
        X[self.out_col] = X[self.input].apply(self.scale)
        return X

    def scale(self, hist):
        divided = hist.Clone("{}_{}".format(hist.GetName(), self.out_col))
        divided.Divide(hist, self._eventmap_cleaned, 1, 1, "B")
        divided.LabelsOption("v")
        return divided


def process(hist, lst, filepath, badmap_fname,
            pattern="SM{}", nhists=4, sm=None):
    event_runs = ROOT.TFile(filepath).Get(lst).FindObject("hRunEvents")
    analysis = make_pipeline(
        HistReader("name", "raw", filepath, hist, lst),
        HistReader("module_number", "badmap", badmap_fname, "PHOS_BadMap_mod"),
        EmptyBinRemover("raw", "cleaned"),
        AcceptanceScaler(["cleaned", "badmap"], "acceptance"),
        EventsScaler("acceptance", "scaled",
                     raw_col="raw", eventmap=event_runs),
        AverageCalculator("scaled", "scaled")
    )

    outputs = pd.DataFrame(index=map(str, range(1, nhists + 1)))
    outputs["module_number"] = sm or outputs.index
    outputs["name"] = outputs.index.map(pattern.format)
    return analysis.fit_transform(outputs)


def fired_trigger_fraction(mtriggers, triggers):
    output = []
    for trig, mtrig in zip(triggers, mtriggers):
        fired = mtrig.Clone()
        fired.Divide(mtrig, trig, 1, 1, "B")
        title = "Ratio of matched trigger clusters to all triggered clusters"
        fired.SetTitle(title)
        output.append(fired)
    return output


def trend(filepath, lst="PHOSTriggerQAResultsL0",
          badmap_fname="../BadMap_LHC16-updated.root"):
    plotter = plotting.Plotter()
    canvas = ROOT.TCanvas("TrendPlots", "TrendPlots", 1000, 500)
    canvas.Divide(1, 3)

    triggers = process("hRunTriggers", lst, filepath, badmap_fname)
    title = "Number of 4x4 patches per run"
    title += ";; # patches / accepntace/ #events"
    plotter.plot(triggers["scaled"],
                 triggers["name"],
                 canvas.cd(1),
                 title)

    mtriggers = process("hRunMatchedTriggers", lst, filepath, badmap_fname)
    title = "Numbero of matched 4x4 patches per run"
    title += ";;# patches / accepntace/ #events"
    plotter.plot(mtriggers["scaled"],
                 mtriggers["name"],
                 canvas.cd(2),
                 title)

    fired_fraction = fired_trigger_fraction(mtriggers["scaled"],
                                            triggers["scaled"])

    title = "Number of matched tirggers / number of all triggers"
    title += ";;#patches / # matched"
    plotter.plot(fired_fraction,
                 triggers["name"],
                 canvas.cd(3),
                 title)

    plotting.save_canvas(canvas, "trending")
    canvas.Update()
    raw_input()


def trend_tru(filepath, lst="PHOSTriggerQAResultsL0",
              badmap_fname="../BadMap_LHC16-updated.root", n_modules=4):
    for sm in range(1, n_modules + 1):
        plotter = plotting.Plotter()
        canvas = ROOT.TCanvas("TrendPlots", "TrendPlots", 1000, 500)
        canvas.Divide(1, 3)

        triggers = process("hRunTriggersSM{}".format(sm),
                           lst, filepath, badmap_fname,
                           pattern="TRU{}", nhists=8, sm=sm)
        title = "Number of 4x4 patches per run SM{}".format(sm)
        title += ";; # patches / accepntace/ #events"
        plotter.plot(triggers["scaled"],
                     triggers["name"],
                     canvas.cd(1),
                     title)

        mtriggers = process("hRunMatchedTriggersSM{}".format(sm),
                            lst, filepath, badmap_fname,
                            pattern="TRU{}", nhists=8, sm=sm)
        title = "Numbero of matched 4x4 patches per run SM{}".format(sm)
        title += ";;# patches / accepntace/ #events"
        plotter.plot(mtriggers["scaled"],
                     mtriggers["name"],
                     canvas.cd(2),
                     title)

        fired_fraction = fired_trigger_fraction(mtriggers["scaled"],
                                                triggers["scaled"])

        title = "Number of matched tirggers"
        title += " / number of all triggers SM{}".format(sm)
        title += ";;#patches / # matched"
        plotter.plot(fired_fraction,
                     triggers["name"],
                     canvas.cd(3),
                     title)

        plotting.save_canvas(canvas, "trending-tru-sm-{}".format(sm))
        canvas.Update()
        raw_input()
