import unittest
import pytest

import ROOT
from spectrum.broot import BROOT as br
from spectrum.options import ProbeTofOptions
from spectrum.comparator import Comparator
from vault.datavault import DataVault
from spectrum.output import AnalysisOutput
from tools.probe import TagAndProbe
from tools.validate import validate

LATEST_DATASET = (
    DataVault().input("data",
                      listname="TagAndProbleTOF",
                      histname="MassEnergyTOF_SM0"),
    DataVault().input("data",
                      listname="TagAndProbleTOF",
                      histname="MassEnergyAll_SM0"),
)
OLD_DATASET = (
    DataVault().input("data",
                      "uncorrected",
                      "TagAndProbleTOFOnlyTender",
                      histname="MassEnergyTOF_SM0"),
    DataVault().input("data",
                      "uncorrected",
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

    tof_eff.SetParameter(0, -1.02802e+00)
    tof_eff.SetParameter(1, 8.51857e+00)
    tof_eff.SetParameter(2, 6.19420e-01)
    tof_eff.SetParameter(3, 1.30498e+00)
    tof_eff.SetParameter(4, -1.78716e+00)

    return tof_eff


def fit_tof_efficiency(dataset=LATEST_DATASET):
    options = ProbeTofOptions()
    options.fitfunc = efficincy_function()
    probe_estimator = TagAndProbe(options, False)
    efficiency = probe_estimator.transform(
        dataset,
        loggs=AnalysisOutput("tof efficiency")
    )
    efficiency.Fit(options.fitfunc, "R")
    print "Fitted", options.fitfunc.GetChisquare() / options.fitfunc.GetNDF()
    efficiency.SetTitle(
        "%s %s" % (
            "Timing cut efficiency for efficiency",
            # options.fitfunc.GetChisquare() / options.fitfunc.GetNDF(),
            "; p_{T}, GeV/c; efficiency"
        )
    )
    # diff = Comparator(crange=(0.2, 1.05))
    # diff.compare(efficiency)
    return efficiency


class ValidateDataset(unittest.TestCase):
    @pytest.mark.interactive
    @pytest.mark.onlylocal
    def test_estimate_tof_efficiency(self):
        efficiency = fit_tof_efficiency(OLD_DATASET)
        validate(br.hist2dict(efficiency), "efficiency_tag")


@pytest.mark.interactive
@pytest.mark.onlylocal
def test_old_results():
    Comparator(labels=("old", "new")).compare(
        fit_tof_efficiency(OLD_DATASET),
        fit_tof_efficiency()
    )
