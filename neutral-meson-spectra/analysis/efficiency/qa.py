import pytest

import ROOT
from spectrum.input import SingleHistInput
from spectrum.output import open_loggs
import spectrum.broot as br  # noqa
from spectrum.comparator import Comparator  # noqa

import spectrum.plotter as plt
from spectrum.tools.validate import validate  # noqa
from vault.datavault import DataVault


@pytest.fixture
def data(particle):
    production = "single {}".format(particle)
    return (
        DataVault().input(production, "low", "PhysEff"),
        DataVault().input(production, "high", "PhysEff"),
    )


@pytest.fixture
def oname(particle):
    return "results/analysis/spmc/eta_phi_{}.pdf".format(br.spell(particle))


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta",
])
def test_eta_phi(particle, data, oname):
    with plt.style(), plt.pcanvas(oname=oname), open_loggs() as loggs:
        ROOT.gStyle.SetPalette(ROOT.kLightTemperature)
        ROOT.gPad.SetLogz(True)
        summed = br.hsum([
            SingleHistInput("hEtaPhi_#gamma").transform(d, loggs)
            for d in data
        ])
        summed.Draw("colz")
