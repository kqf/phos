import ROOT
import pytest

import spectrum.broot as br
from spectrum.output import open_loggs
from spectrum.options import Options
from spectrum.analysis import Analysis
from spectrum.plotter import plot


def fit(hist, quant, particle):
    hist.SetTitle("Data")
    fitf = ROOT.TF1(hist.GetName(), quant.func, *quant.frange)
    # fitf = ROOT.TF1(hist.GetName(), quant.func, min(bins), 2)
    fitf.SetTitle("Fit")
    fitf.SetLineColor(ROOT.kBlack)
    fitf.SetLineStyle(9)
    for i, (p, n) in enumerate(zip(quant.pars, quant.names)):
        fitf.SetParName(i, n)
        fitf.SetParameter(i, p)

    hist.Fit(fitf, "Q")
    # print(br.pars(fitf))
    br.report(fitf, particle)
    pattern = "results/analysis/data/{}_{}.pdf"
    plot(
        [hist, fitf],
        logy=False,
        ltitle="{} #rightarrow #gamma #gamma".format(particle),
        oname=pattern.format(hist.GetName(), br.spell(particle)),
        more_logs=False,
        yoffset=2.05,
    )


@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta"
])
def test_mass_width_parametrization(particle, data):
    options = Options(particle=particle)
    with open_loggs("test mass width parameters") as loggs:
        output = Analysis(options).transform(data, loggs)

    fit(output.mass, options.calibration.mass, particle)
    fit(output.width, options.calibration.width, particle)
