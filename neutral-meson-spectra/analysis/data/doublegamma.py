import ROOT
import pytest

import spectrum.broot as br
import spectrum.plotter as plt
from spectrum.output import open_loggs
from spectrum.options import Options
from spectrum.analysis import Analysis
from spectrum.ptplotter import MassesPlot


@pytest.fixture
def oname(particle):
    ofile = "results/analysis/data/gammagamma_{}.pdf"
    return ofile.format(br.spell(particle))


@pytest.mark.onlylocal
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta",
])
def test_simple(particle, data, oname):
    analysis = Analysis(Options(particle=particle))
    with open_loggs() as loggs:
        with plt.pcanvas(size=(96, 128), stop=True, oname=oname) as canvas:
            ROOT.gStyle.SetStatY(0.88)
            ROOT.gStyle.SetStatX(0.88)
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

            analysis.transform(data, loggs=loggs)
            data = loggs["parametrize"]["output"].loc[12]
            MassesPlot().transform(data["invmasses"], canvas)
