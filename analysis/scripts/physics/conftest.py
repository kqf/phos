import ROOT
import pytest

import spectrum.broot as br
from spectrum.constants import mass
from spectrum.output import open_loggs
from spectrum.pipeline import SingleHistReader
from spectrum.vault import DataVault
from spectrum.vault import FVault


@pytest.fixture
def tsallis(particle):
    tsallis = FVault().tf1("tsallis")
    tsallis.SetName("Tsallis")
    tsallis.SetTitle("Tsallis fit")
    # tsallis.SetLineColor(ROOT.kBlue + 1)
    tsallis.SetNpx(1000)
    tsallis.SetLineColor(ROOT.kBlack)
    tsallis.SetLineStyle(7)

    if particle == "#pi^{0}":
        tsallis.SetParameter(0, 1)
        tsallis.SetParameter(1, 0.125)
        tsallis.SetParLimits(1, 0.100, 0.300)
        tsallis.FixParameter(2, 6.500)
        tsallis.SetParLimits(2, 6.000, 8.000)
        tsallis.FixParameter(3, mass(particle))
        tsallis.SetRange(1.4, 20)

    if particle == "#eta":
        tsallis.SetParameter(0, 1)
        tsallis.SetParameter(1, 0.238)
        tsallis.SetParLimits(1, 0.200, 0.300)
        tsallis.SetParameter(2, 6.19)
        tsallis.SetParLimits(2, 5.5, 7.000)
        tsallis.FixParameter(3, mass(particle))
        tsallis.SetRange(2.2, 20)

    tsallis.FixParameter(3, mass(particle))
    tsallis.FixParameter(4, mass(particle))
    return tsallis


@pytest.fixture
def tcm(particle):
    tcm = FVault().tf1("tcm", "{} 13 TeV".format(particle))
    tcm.SetName("TCM")
    tcm.SetTitle("TCM fit")
    tcm.SetNpx(100)
    tcm.SetLineColor(ROOT.kBlack)
    tcm.SetLineWidth(2)

    if particle == "#pi^{0}":
        tcm.SetRange(0.7, 22)
        tcm.SetParameter(0, 0.1)
        tcm.SetParameter(1, 1.73e-01)
        tcm.SetParLimits(1, 0.1, 0.3)
        tcm.SetParameter(2, 0.1)
        tcm.SetParameter(3, 0.601)
        tcm.SetParLimits(3, 0.4, 1.0)
        tcm.SetParameter(4, 3.09)
        tcm.SetParLimits(4, 2.0, 4.0)

    if particle == "#eta":
        # pass
        tcm.SetParameter(0, 0.1)
        tcm.SetParLimits(0, 0, 1e4)
        tcm.SetParameter(1, 1.71e-01)
        tcm.SetParLimits(1, 0.1, 0.3)
        tcm.SetParameter(2, 0.1)
        tcm.SetParameter(3, 0.801)
        # tcm.SetParLimits(3, 0.7, 0.9)
        tcm.SetParameter(4, 3.059)
        # tcm.SetParLimits(4, 2.0, 4.0)

    tcm.FixParameter(5, mass(particle))
    return tcm


@pytest.fixture
def oname(particle):
    return "results/discussion/{{}}{}.pdf".format(br.spell(particle))


@pytest.fixture
def ltitle(particle):
    return "{} #rightarrow #gamma#gamma".format(particle)

# TODO: Fix me later


def read_pythia6(particle):
    histnames = {
        "#pi^{0}": "hxsPi0PtInv",
        "#eta": "hxsEtaPtInv"
    }
    data = DataVault().input("theory", "pythia6", histname=histnames[particle])
    with open_loggs() as loggs:
        mc = SingleHistReader().transform(data, loggs)
    mc.Scale(1e-6)
    mc.SetTitle("PYTHIA 6")
    return mc


@pytest.fixture
def pythia6(particle):
    return read_pythia6(particle)


@pytest.fixture
def pythia6_eta_pion_ratio():
    mc = br.ratio(read_pythia6("#eta"), read_pythia6("#pi^{0}"))
    mc.SetTitle("PYTHIA 6")
    return mc
