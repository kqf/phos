import ROOT
import pytest

import spectrum.broot as br
from spectrum.output import open_loggs
from spectrum.options import CompositeOptions
from spectrum.analysis import Analysis
from spectrum.plotter import plot


def fit(hist, quant, particle, stop):
    hist.SetTitle("Data")
    bins = br.edges(hist)
    fitf = ROOT.TF1(hist.GetName(), quant.func, min(bins), max(bins))
    # fitf = ROOT.TF1(hist.GetName(), quant.func, min(bins), 2)
    fitf.SetTitle("Fit")
    fitf.SetLineColor(ROOT.kBlack)
    fitf.SetLineStyle(9)
    for i, (p, n) in enumerate(zip(quant.pars, quant.names)):
        fitf.SetParName(i, n)
        fitf.SetParameter(i, p)

    hist.Fit(fitf, "Q")
    print(br.pars(fitf))
    br.report(fitf, particle)
    plot([hist, fitf], stop=stop, logy=False)


@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta"
])
def test_mass_width_parametrization(particle, spmc, stop):
    options = CompositeOptions(particle=particle)
    with open_loggs() as loggs:
        output = Analysis(options).transform(spmc, loggs)

    fit(output.mass, options.steps[0][1].calibration.mass, particle, stop)
    fit(output.width, options.steps[0][1].calibration.width, particle, stop)
