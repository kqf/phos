import numpy as np


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
