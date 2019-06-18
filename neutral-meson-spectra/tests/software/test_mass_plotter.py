import sys
import pytest
import ROOT


import spectrum.sutils as su
from spectrum.ptplotter import MassesPlot


@pytest.fixture
def imass():
    data = ROOT.TH1F("test", "Test hist", 100, 0, 1.5)
    data.FillRandom("gaus")
    func = ROOT.TF1("fitf", "gaus")
    data.Fit(func, "Q0")
    data.mass = data
    data.background = None
    data.sigf = func
    data.bgrf = None
    data.signal = data
    data.integration_region = (0.1, 0.12)
    data.initial_fitting_region = (0.08, 0.14)
    return data


@pytest.fixture
def stop():
    stop = 'discover' not in sys.argv
    stop = stop and 'pytest' not in sys.argv[0]
    return stop


def test_plots_ivnariatmass(imass, stop):
    canvas = su.gcanvas()
    MassesPlot().transform(imass, canvas)
    su.wait(stop=stop)
