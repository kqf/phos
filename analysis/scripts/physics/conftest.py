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
        tsallis.FixParameter(2, 6.500)
        tsallis.SetParLimits(1, 0.100, 0.630)
        tsallis.SetParLimits(2, 6.000, 9.000)
        tsallis.FixParameter(3, mass(particle))
        tsallis.SetRange(2.0, 10)

    if particle == "#eta":
        tsallis.SetParameter(0, 1)
        tsallis.SetParameter(1, 0.238)
        tsallis.SetParLimits(1, 0.238, 0.300)
        tsallis.SetParameter(2, 6.19)
        tsallis.SetParLimits(2, 6.03, 7.000)
        tsallis.FixParameter(3, mass(particle))
        tsallis.SetRange(3.0, 10)

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
        tcm.SetParameter(0, 3e5)
        # tcm.SetParLimits(0, 0, 1e6)

        # temin, temax = 0.0, 0.2
        tcm.SetParameter(1, 0.142)
        # tcm.SetParLimits(1, temin, temax)

        tcm.SetParameter(2, 3e4)
        # tcm.SetParLimits(2, 0, 1e6)

        tcm.SetParameter(3, 0.597)
        # tcm.SetParLimits(3, temin * 4.2, temax * 4.2)
        tcm.SetParameter(4, 3.028)

    if particle == "#eta":
        # pass
        tcm.SetParameter(0, 1e5)
        tcm.SetParLimits(0, 0, 1e6)

        # temin, temax = 0.0, 0.3
        tcm.SetParameter(1, 0.229)
        # tcm.SetParLimits(1, temin, temax)

        tcm.SetParameter(2, 1e4)
        tcm.SetParLimits(2, 0, 1e6)

        tcm.SetParameter(3, 0.810)
        # tcm.SetParLimits(3, temin * 4.2, temax * 4.2)

        tcm.SetParameter(4, 3.043)

    tcm.FixParameter(5, mass(particle))
    return tcm


@pytest.fixture
def tcm2(particle):
    tcm = FVault().tf1("tcm", "{} 13 TeV".format(particle))
    tcm.SetName("TCM")
    tcm.SetTitle("TCM fit")
    tcm.SetNpx(100)
    tcm.SetLineColor(ROOT.kBlack)
    tcm.SetLineWidth(2)

    if particle == "#pi^{0}":
        tcm.SetRange(0.7, 22)
        tcm.SetParameter(0, 3e5)
        tcm.SetParLimits(0, 0, 1e6)

        # temin, temax = 0.0, 0.2
        tcm.SetParameter(1, 0.142)
        # tcm.SetParLimits(1, temin, temax)

        tcm.SetParameter(2, 3e4)
        # tcm.SetParLimits(2, 0, 1e6)

        tcm.SetParameter(3, 0.597)
        # tcm.SetParLimits(3, temin * 4.2, temax * 4.2)
        tcm.SetParameter(4, 3.028)

    if particle == "#eta":
        # pass
        tcm.SetParameter(0, 1e5)
        tcm.SetParLimits(0, 0, 1e6)

        # temin, temax = 0.0, 0.3
        tcm.SetParameter(1, 0.229)
        # tcm.SetParLimits(1, temin, temax)

        tcm.SetParameter(2, 1e4)
        tcm.SetParLimits(2, 0, 1e6)

        tcm.SetParameter(3, 0.810)
        # tcm.SetParLimits(3, temin * 4.2, temax * 4.2)

        tcm.SetParameter(4, 3.043)

    tcm.FixParameter(5, mass(particle))
    return tcm


@pytest.fixture
def oname(particle):
    return "images/discussion/{{}}{}.pdf".format(br.spell(particle))


@pytest.fixture
def coname(target):
    return "images/discussion/{{}}{}.pdf".format(target)


@pytest.fixture
def ltitle(particle):
    return "{} #rightarrow #gamma#gamma".format(particle)


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


@pytest.fixture
def eta_pion_ratio_fitf(ptmin=4.5, ptmax=22):
    ff = ROOT.TF1("etaPionRatio", "[0]", ptmin, ptmax)
    ff.SetParameter(0, 0.5)
    ff.SetParName(0, "Value")
    return ff
