from __future__ import print_function
import pytest

import ROOT
import spectrum.broot as br
from spectrum.options import ProbeTofOptions
from vault.datavault import DataVault
from spectrum.output import open_loggs
from spectrum.tools.probe import TagAndProbe
from spectrum.tools.validate import validate # noqa
from spectrum.plotter import plot

"""
- [ ] Fix titles
- [ ] Exclude LHC18
- [ ] Try different binning
- [ ] Try different parameters

"""


@pytest.fixture
def data():
    return (
        DataVault().input("data", "staging", listname="TagAndProbleTOF",
                          histname="MassEnergyTOF_SM0"),
        DataVault().input("data", "staging", listname="TagAndProbleTOF",
                          histname="MassEnergyAll_SM0"),
    )


@pytest.fixture
def data_old():
    return (
        DataVault().input("data", "uncorrected",
                          "TagAndProbleTOFOnlyTender",
                          histname="MassEnergyTOF_SM0"),
        DataVault().input("data", "uncorrected",
                          "TagAndProbleTOFOnlyTender",
                          histname="MassEnergyAll_SM0"),
    )


@pytest.fixture
def fitfunc():
    tof_eff = ROOT.TF1(
        "tof_eff",
        # "[2] * (1.+[0]*TMath::Exp(-TMath::Power(x/[1], 2.) / 2.)) "
        "1 - [2] / (1 + TMath::Exp(x * [0] + [1]))"
        " - [3] * TMath::Exp(x * [4])", 0, 20
    )

    tof_eff.SetParNames("A", "#sigma", "Eff_{scale}")
    # tof_eff.FixParameter(0, -1.30534e+00)
    # tof_eff.FixParameter(1, 1.02604e+01)
    # tof_eff.FixParameter(2, 5.70061e-01)
    # tof_eff.FixParameter(3, 1.06068e+00)
    # tof_eff.FixParameter(4, -1.62810e+00)

    # Previous
    tof_eff.SetParameter(0, -1.02802e+00)
    tof_eff.SetParameter(1, 8.51857e+00)
    tof_eff.SetParameter(2, 6.19420e-01)
    tof_eff.SetParameter(3, 1.30498e+00)
    tof_eff.SetParameter(4, -1.78716e+00)

    # tof_eff.FixParameter(0, -1.02802e+00)
    # tof_eff.FixParameter(1, 8.51857e+00)
    # tof_eff.FixParameter(2, 6.19420e-01)
    # tof_eff.FixParameter(3, 2.15384e+00)
    # tof_eff.FixParameter(4, -2.90812e+00)
    tof_eff.SetTitle("Fit")
    tof_eff.SetLineColor(ROOT.kBlack)
    tof_eff.SetLineStyle(9)
    return tof_eff


@pytest.fixture
def efficiency(data):
    with open_loggs() as loggs:
        probe_estimator = TagAndProbe(ProbeTofOptions(), False)
        efficiency = probe_estimator.transform(data, loggs)
    return efficiency


@pytest.mark.interactive
@pytest.mark.onlylocal
def test_estimate_tof_efficiency(efficiency, fitfunc):
    bins = br.edges(efficiency)
    fitfunc.SetRange(min(bins), max(bins))
    efficiency.Fit(fitfunc, "R")
    plot(
        [efficiency, fitfunc],
        logy=False,
        legend_pos=(0.2, 0.7, 0.4, 0.85),
    )
    # validate(br.hist2dict(efficiency), "efficiency_tag")
