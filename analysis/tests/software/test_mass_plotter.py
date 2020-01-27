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


@pytest.fixture(scope="module")
def title():
    title = """
        pp at #sqrt{#it{s}} = 13 TeV,|
        #pi^{0} #rightarrow #gamma#gamma,|
        15 < p_{T} < 20 GeV/#it{c} |
    """
    return title


@pytest.fixture(scope="module")
def mass(title):
    measured = generate_from_data("config/data/gaus.json")

    data = ROOT.TH1F("test", ";M_{#gamma#gamma}; counts", 400, 0, 1.5)
    data.SetTitle(title)
    data.FillRandom(measured.GetName(), 10000)
    data.Fit(measured, "Q0")

    background = measured.Clone("backgroundf")
    background.SetParameter(0, 0)

    signal = data.Clone()
    signal.Add(background, -1)

    output = {}
    output["mass"] = signal
    output["signalf"] = measured
    output["background"] = background
    output["signal"] = data
    output["measured"] = measured
    output["fit_range"] = (0.08, 0.2)
    output["integration_region"] = (0.125, 0.146)
    return output


def test_plots_ivnariatmass(mass, stop):
    with su.canvas(stop=stop) as canvas:
        canvas.Clear()
        params = dict(mass)
        params["pad"] = canvas
        MassesPlot().transform(**params)


@pytest.mark.parametrize("nhists", [1, 4, 6, 9, 12])
def test_multiple_plotter(nhists, mass, stop):
    MultiplePlotter().transform([mass] * nhists, stop=stop)
