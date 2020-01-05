import ROOT
import pytest

from spectrum.vault import FVault
from spectrum.comparator import Comparator


@pytest.fixture
def parameters():
    return {
        "old": [
            -0.014719244288611932,
            2 * 0.8017501954719543,
            1.050000000000015,
        ],
        "updated gamma": [
            -0.008502585550404397,
            1.063118454172695,
            1.0222154255076596
        ],
        "updated pi0": [
            -0.022361543707205396,
            1.9834455549215824,
            1.0160704760491277,
        ],
        "new pi0": [
            -0.023207895974126137,
            2.1705074159914495,
            1.0178019980200619
        ]
    }


@pytest.mark.interactive
@pytest.mark.onlylocal
def test_nonlin_function(parameters):
    fv = FVault()
    functions = [
        ROOT.TF1('f' + str(i), fv.func("nonlinearity"), 0, 20)
        for i in parameters
    ]

    histograms = []
    for f, p in zip(functions, parameters):
        f.SetParameters(*parameters[p])
        histograms.append(f.GetHistogram())
        histograms[-1].SetTitle(p)
        histograms[-1].label = p
        histograms[-1]
    Comparator().compare(*histograms)
