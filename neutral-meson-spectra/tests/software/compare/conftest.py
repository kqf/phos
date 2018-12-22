import pytest
import ROOT
import json

import sys
from vault.formulas import FVault


@pytest.fixture()
def data():
    with open('config/test_particles.json') as f:
        particles = json.load(f)
    data = [_spectrum(i, particles[i]) for i in particles]

    for hist in data:
        hist.logy = 1
    return data


@pytest.fixture()
def stop():
    pytest = 'pytest' in sys.argv[0]
    discover = 'discover' in sys.argv
    compare = 'test.software.compare' in sys.argv
    skip = discover and not compare or pytest
    return not skip


def _spectrum(name, par):
    function = ROOT.TF1(name, FVault().func("tsallis"), 0.3, 15, 3)
    function.SetParameters(*par)
    title = '%s p_{T} spectrum; p_{T}, GeV/c; #frac{dN}{dp_{T}}' % name
    histogram = function.GetHistogram().Clone()
    histogram.SetName(name + "_spectrum")
    histogram.SetTitle(title)
    histogram.Scale(100000000)
    histogram.label = name
    for i in range(histogram.GetNbinsX()):
        histogram.SetBinError(
            i + 1,
            histogram.GetBinContent(i) ** 0.5
        )
    return histogram
