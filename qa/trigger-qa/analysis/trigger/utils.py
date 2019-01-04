import numpy as np


def hist2array(hist):
    start, stop = 1, hist.GetNbinsX() + 1
    return np.array([hist.GetBinContent(i) for i in range(start, stop)])
