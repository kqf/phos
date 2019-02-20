import ROOT
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

TRIGGER_MODULE_SHAPE = (16, 28)


def from_list(histname, lst):
    def reader(index):
        try:
            return lst.Get("{}{}".format(histname, str(index)))
        except AttributeError:
            return lst.FindObject("{}{}".format(histname, str(index)))
    return reader


def hist2array2d(hist):
    data = [[
        hist.GetBinContent(i + 1, j + 1)
        for j in range(hist.GetNbinsY())]
        for i in range(hist.GetNbinsX())]

    return np.asarray(data)


def hist2array(hist):
    # Ugly but efficient hack against ROOT typing
    if "2" in str(type(hist)):
        return hist2array2d(hist)
    start, stop = 1, hist.GetNbinsX() + 1
    return np.array([hist.GetBinContent(i) for i in range(start, stop)])


def array2hist(array, hist):
    for i in range(hist.GetNbinsX()):
        for j in range(hist.GetNbinsY()):
            hist.SetBinContent(i + 1, j + 1, array[i][j])
    return hist


def tru(cell_x, cell_z):
    # Return TRU region number for given cell.
    # cell_x: [0-63], cell_z: [0-55]

    # RCU0: TRU 1,2
    if 0 <= cell_x < 16:
        if 0 <= cell_z < 28:
            return 2
        return 1

    # RCU1: TRU 3,4
    if 16 <= cell_x < 32:
        if 0 <= cell_z < 28:
            return 4
        return 3

    # RCU2: TRU 5,6
    if 32 <= cell_x < 48:
        if 0 <= cell_z < 28:
            return 6
        return 5

    # RCU3: TRU 7,8
    if 48 <= cell_x < 64:
        if 0 <= cell_z < 28:
            return 8
        return 7

    return -111


def tru_from_patch(patch_x, patch_z):
    # Return TRU region number for given cell.
    # patch_x: [0-63], patch_z: [0-55]

    # RCU0: TRU 1,2
    if 0 <= patch_x < 4:
        if 0 <= patch_z < 14:
            return 2
        return 1

    # RCU1: TRU 3,4
    if 4 <= patch_x < 8:
        if 0 <= patch_z < 14:
            return 4
        return 3

    # RCU2: TRU 5,6
    if 8 <= patch_x < 12:
        if 0 <= patch_z < 14:
            return 6
        return 5

    # RCU3: TRU 7,8
    if 12 <= patch_x < 16:
        if 0 <= patch_z < 14:
            return 8
        return 7

    return -111


def select_tru(hist, number):
    trumasks = [[
        tru_from_patch(i, j)
        for j in range(hist.shape[1])]
        for i in range(hist.shape[0])]
    trumask = np.asarray(trumasks) == number
    return hist * trumask


def style(hist):
    hist.SetLineWidth(2)
    hist.SetMarkerStyle(20)
    hist.SetMarkerSize(0.5)
    hist.SetNdivisions(530)
    hist.SetAxisRange(0., 39.)
    hist.SetXTitle("E, GeV")
    return hist


def trendhist(bins, contents):
    hist = ROOT.TH1F("trending", "", len(bins), 0, len(bins))
    for i, (b, c) in enumerate(sorted(zip(bins, contents))):
        hist.SetBinContent(i + 1, c)
        hist.GetXaxis().SetBinLabel(i + 1, str(b))
    hist.SetLineWidth(2)
    hist.GetXaxis().LabelsOption("v")
    hist.GetXaxis().SetLabelSize(0.05)
    return hist


def row_decoder(listkey, sm_start=1, sm_stop=4, tru_start=1, tru_stop=8):
    lst, output = listkey.ReadObj(), []

    for sm in range(sm_start, sm_stop + 1):
        for tru in range(tru_start, tru_stop + 1):
            output.append({
                "run": int(listkey.GetName()),
                "module": "SM{}".format(sm),
                "tru": "TRU{}".format(tru),
                "hPhotAll": lst.FindObject(
                    "hPhotAllSM{}TRU{}".format(sm, tru)),
                "hPhotTrig": lst.FindObject(
                    "hPhotTrigSM{}TRU{}".format(sm, tru)),
                "events": lst.FindObject("hNev").GetBinContent(1)
            })

    return output


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


def read_dataset(filepath, rules):
    infile = ROOT.TFile(filepath)
    # infile.ls()
    outputs = []
    for key in infile.GetListOfKeys():
        outputs += row_decoder(key)
    return pd.DataFrame(outputs)
