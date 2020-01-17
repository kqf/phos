import ROOT
import pytest

import spectrum.broot as br
import spectrum.plotter as plt
from spectrum.output import open_loggs
from spectrum.options import CompositeOptions
from spectrum.analysis import Analysis
from spectrum.ptplotter import MassesPlot


@pytest.fixture
def oname(particle):
    ofile = "results/analysis/spmc/gammagamma_{}.pdf"
    return ofile.format(br.spell(particle))


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta",
])
def test_simple(particle, spmc, oname):
    analysis = Analysis(CompositeOptions(particle=particle))
    with open_loggs() as loggs:
        with plt.pcanvas(size=(96, 128), stop=True, oname=oname) as canvas:
            ROOT.gStyle.SetStatX(0.92)
            ROOT.gStyle.SetStatW(0.15)
            ROOT.gStyle.SetStatH(0.15)

            ROOT.gStyle.SetTitleFont(62, "X")
            ROOT.gStyle.SetTitleFont(62, "Y")
            ROOT.gStyle.SetTitleFont(62, "Z")
            ROOT.gStyle.SetLabelFont(42, "X")
            ROOT.gStyle.SetLabelFont(42, "Y")
            ROOT.gStyle.SetLabelFont(42, "Z")
            ROOT.gStyle.SetStatFont(42)

            ROOT.gStyle.SetLabelSize(0.04, "X")
            ROOT.gStyle.SetLabelSize(0.04, "Y")
            ROOT.gStyle.SetLabelSize(0.04, "Z")
            ROOT.gStyle.SetTitleSize(0.04, "X")
            ROOT.gStyle.SetTitleSize(0.04, "Y")
            ROOT.gStyle.SetTitleSize(0.04, "Z")

            analysis.transform(spmc, loggs=loggs)
            data = loggs["steps"]["analysis-0"]["parametrize"]["output"].loc[9]
            MassesPlot().transform(
                pad=canvas,
                mass=data["measured"],
                signalf=data["signalf"],
                background=data["background"],
                signal=data["signal"],
                bgrf=data["measuredf"],
                fit_range=data["fit_range"],
                integration_region=data["integration_region"],
            )
