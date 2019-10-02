import pytest
import ROOT

import spectrum.sutils as su
from spectrum.options import option
from spectrum.ptplotter import MassesPlot, MultiplePlotter


def generate_from_data(conf, particle="#pi^{0}"):
    conf = option(conf, particle)
    measured = ROOT.TF1("measured", "gaus(0) + pol2(3)", 0, 1.5)
    measured.SetParameters(*conf.preliminary.parameters)
    measured.SetParNames(*conf.preliminary.par_names)
    return measured


@pytest.fixture
def mass():
    measured = generate_from_data("config/data/gaus.json")
    data = ROOT.TH1F("test", ";p_{T}, GeV/c; M_{#gamma#gamma}", 400, 0, 1.5)
    data.FillRandom(measured.GetName(), 10000)
    func = ROOT.TF1("fitf", "gaus")
    data.Fit(func, "Q0")
    data.mass = data
    data.background = None
    data.sigf = func
    data.bgrf = None
    data.signal = data
    data.integration_region = (0.125, 0.146)
    data.fit_range = (0.08, 0.2)
    return data


def test_plots_ivnariatmass(mass, stop):
    with su.canvas(stop=stop) as canvas:
        MassesPlot().transform(mass, canvas)


@pytest.mark.parametrize("nhists", [1, 4, 6])
def test_multiple_plotter(nhists, mass, stop=True):
    MultiplePlotter().transform([mass] * nhists, show=stop)
