import ROOT
import pytest

import spectrum.broot as br
from spectrum.output import open_loggs
from spectrum.options import Options
from spectrum.analysis import Analysis
from spectrum.plotter import plot


@pytest.fixture
def hparms(data, particle, target):
    options = Options(particle=particle)
    with open_loggs() as loggs:
        output = Analysis(options).transform(data, loggs)
    return output._asdict()[target], options.calibration[target]


# @pytest.mark.skip
@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta"
])
@pytest.mark.parametrize("target", [
    "mass",
    "width",
])
def test_mass_width_parametrization(particle, hparms, oname, ltitle, stop):
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
        stop=stop,
        logy=False,
        ltitle=ltitle,
        oname=oname,
        yoffset=2.05,
    )
