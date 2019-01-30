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


def select_tru(hist, number):
    trumasks = [[
        tru(i, j)
        for j in range(hist.shape[1])]
        for i in range(hist.shape[0])]
    print(trumasks)

    trumask = np.asarray(trumasks) == number
    return hist * trumask
