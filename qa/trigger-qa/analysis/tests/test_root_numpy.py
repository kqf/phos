from __future__ import print_function

import ROOT
import pytest
from trigger.utils import hist2array
import numpy as np


def badmap():
    hist = ROOT.TH2F("PHOS_BadMap_mod1", "", 64, 0.5, 63.5, 56, 0.5, 55.5)
    for i in range(hist.GetNbinsX()):
        for j in range(hist.GetNbinsY()):
            hist.SetBinContent(i + 1, j + 1, 1000 * i + j)
    return hist


def hist1d():
    hist = ROOT.TH1F("testing_vector", "", 64, 0.5, 63.5)
    for i in range(hist.GetNbinsX()):
        hist.SetBinContent(i + 1, i)
    return hist


@pytest.mark.parametrize("hist", [
    hist1d(),
    badmap(),
])
def test_hist2array(hist):
    try:
        import root_numpy as rnp
    except BaseException as e:
        print(e)
        return  # Skip checks for the machines that don't support root_numpy

    np.testing.assert_almost_equal(rnp.hist2array(hist), hist2array(hist))
