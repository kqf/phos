import ROOT
import pytest

import spectrum.broot as br
from spectrum.output import open_loggs
from spectrum.options import Options
from spectrum.analysis import Analysis
from spectrum.plotter import plot


@pytest.fixture
def hparms(data, particle, quant):
    options = Options(particle=particle)
    with open_loggs() as loggs:
        output = Analysis(options).transform(data, loggs)
    return output._asdict()[quant], options.calibration[quant]


@pytest.fixture
def oname(particle, quant):
    pattern = "results/analysis/data/{}_{}.pdf"
    return pattern.format(quant, br.spell(particle))


@pytest.mark.skip
@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta"
])
@pytest.mark.parametrize("quant", [
    "mass",
    "width",
])
def test_mass_width_parametrization(particle, hparms, oname, ltitle):
    hist, params = hparms
    hist.SetTitle("Data")
    fitf = ROOT.TF1(hist.GetName(), params.func, *params.frange)
    fitf.SetTitle("Fit")
    fitf.SetLineColor(ROOT.kBlack)
    fitf.SetLineStyle(9)
    for i, (p, n) in enumerate(zip(params.pars, params.names)):
        fitf.SetParName(i, n)
        fitf.SetParameter(i, p)

    hist.Fit(fitf, "Q")
    br.report(fitf, particle)
    plot(
        [hist, fitf],
        logy=False,
        ltitle=ltitle,
        oname=oname,
        # more_logs=False,
        yoffset=2.05,
    )
