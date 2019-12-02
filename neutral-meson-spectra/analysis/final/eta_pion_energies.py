import ROOT
import pytest
import pandas as pd
import spectrum.broot as br
from spectrum.plotter import plot


@pytest.fixture
def data():
    raw = pd.read_json("config/physics/eta_pion_energies.json")
    return br.graph(
        "; #sqrt{s} (GeV); #eta/#pi^{0}",
        raw["energy"],
        raw["eta_pion"],
        dy=raw["eta_pion_err"])


@pytest.fixture
def delimeter(level=0.5):
    func = ROOT.TF1("const", "[0]", 13.8, 13000)
    func.SetParameter(0, level)
    func.SetLineColor(ROOT.kBlack)
    func.SetLineStyle(9)
    return func


@pytest.fixture
def oname():
    return "results/eta_pion_energies.pdf"


def test_reports_energies(data, delimeter, oname):
    plot(
        [data, delimeter],
        logy=False,
        legend_pos=None,
        ylimits=(0, 1),
        csize=(126, 96),
        oname=oname,
    )
