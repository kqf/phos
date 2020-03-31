import json

import pytest
import ROOT
from spectrum.vault import FVault


@pytest.fixture()
def data():
    with open('config/tests/particles.json') as f:
        particles = json.load(f)
    data = [_spectrum(i, particles[i]) for i in particles]

    for hist in data:
        hist.logy = 1
    return data


def _spectrum(name, par):
    function = ROOT.TF1(name, FVault().func("tsallis"), 0.3, 15, 3)
    function.SetParameters(*par)
    histogram = function.GetHistogram().Clone()
    histogram.SetName(name + "_spectrum")
    histogram.SetTitle('{} #it{{p}}_{{T}} spectrum'.format(name))
    histogram.GetXaxis().SetTitle("#it{p}_{T} (GeV/#it{c})")
    histogram.GetYaxis().SetTitle("#frac{d#it{N}}{d#it{p}_{T}}")
    histogram.Scale(100000000)
    histogram.label = name
    for i in range(histogram.GetNbinsX()):
        histogram.SetBinError(
            i + 1,
            histogram.GetBinContent(i) ** 0.5
        )
    return histogram
