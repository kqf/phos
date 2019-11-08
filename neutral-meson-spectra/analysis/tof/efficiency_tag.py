from __future__ import print_function
import pytest

import ROOT
import spectrum.broot as br
from spectrum.options import ProbeTofOptions
from spectrum.comparator import Comparator
from vault.datavault import DataVault
from spectrum.output import open_loggs
from spectrum.tools.probe import TagAndProbe
from spectrum.tools.validate import validate


@pytest.fixture
def data():
    return (
        DataVault().input("data", listname="TagAndProbleTOF",
                          histname="MassEnergyTOF_SM0"),
        DataVault().input("data", listname="TagAndProbleTOF",
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


def efficincy_function():
    tof_eff = ROOT.TF1(
        "tof_eff",
        # "[2] * (1.+[0]*TMath::Exp(-TMath::Power(x/[1], 2.) / 2.)) "
        "1 - [2] / (1 + TMath::Exp(x * [0] + [1]))"
        " - [3] * TMath::Exp(x * [4])", 0, 20
    )

    tof_eff.SetParNames("A", "#sigma", "Eff_{scale}")
    # tof_eff.SetParameter(0, -1.30534e+00)
    # tof_eff.SetParameter(1, 1.02604e+01)
    # tof_eff.SetParameter(2, 5.70061e-01)
    # tof_eff.SetParameter(3, 1.06068e+00)
    # tof_eff.SetParameter(4, -1.62810e+00)

    # Previous
    # tof_eff.SetParameter(0, -1.02802e+00)
    # tof_eff.SetParameter(1, 8.51857e+00)
    # tof_eff.SetParameter(2, 6.19420e-01)
    # tof_eff.SetParameter(3, 1.30498e+00)
    # tof_eff.SetParameter(4, -1.78716e+00)

    tof_eff.FixParameter(0, -1.02802e+00)
    tof_eff.SetParameter(1, 8.51857e+00)
    tof_eff.SetParameter(2, 6.19420e-01)
    tof_eff.SetParameter(3, 2.15384e+00)
    tof_eff.SetParameter(4, -2.90812e+00)
    return tof_eff


def fit_tof_efficiency(dataset):
    with open_loggs() as loggs:
        options = ProbeTofOptions()
        options.fitfunc = efficincy_function()
        probe_estimator = TagAndProbe(options, False)
        efficiency = probe_estimator.transform(dataset, loggs)

    efficiency.Fit(options.fitfunc, "R")
    print("Fitted", options.fitfunc.GetChisquare() / options.fitfunc.GetNDF())
    efficiency.SetTitle(
        "%s %s" % (
            "Timing cut efficiency for efficiency",
            # options.fitfunc.GetChisquare() / options.fitfunc.GetNDF(),
            "; p_{T} (GeV/#it{c})/c; efficiency"
        )
    )
    # diff = Comparator(crange=(0.2, 1.05))
    # diff.compare(efficiency)
    return efficiency


@pytest.mark.interactive
@pytest.mark.onlylocal
def test_estimate_tof_efficiency(data):
    efficiency = fit_tof_efficiency(data)
    validate(br.hist2dict(efficiency), "efficiency_tag")
    # Comparator().compare(efficiency)


# NB: Use the following test to check chi2 value per point
@pytest.mark.skip("")
@pytest.mark.interactive
@pytest.mark.onlylocal
def test_newest_results(data):
    Comparator().compare(
        br.chi2errors(fit_tof_efficiency(data), scale=0.01)
    )
