import unittest

import ROOT
import json
from spectrum.broot import BROOT as br
from spectrum.options import ProbeTofOptions
from spectrum.comparator import Comparator
from spectrum.sutils import gcanvas, adjust_canvas
from vault.datavault import DataVault
from spectrum.output import AnalysisOutput
from tools.probe import TagAndProbe
from tools.validate import validate

ROOT.TH1.AddDirectory(False)


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


def fit_tof_efficiency():
    options = ProbeTofOptions()
    options.fitfunc = efficincy_function()
    probe_estimator = TagAndProbe(options, False)
    efficiency = probe_estimator.transform(
        [
            DataVault().input("data", "uncorrected",
                              "TagAndProbleTOFOnlyTender",
                              histname="MassEnergyTOF_SM0"),
            DataVault().input("data", "uncorrected",
                              "TagAndProbleTOFOnlyTender",
                              histname="MassEnergyAll_SM0"),
        ],
        loggs=AnalysisOutput("tof efficiency")
    )
    efficiency.Fit(options.fitfunc, "R")
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


class TagAndProbeEfficiencyTOF(unittest.TestCase):

    def setUp(self):
        self.canvas = gcanvas()
        with open("config/tag-and-probe-tof.json") as f:
            self.nominal_bins = json.load(f)["test_bins"]

    def test_estimate_tof_efficiency(self):
        efficiency = fit_tof_efficiency()
        bins = br.bins(efficiency)._asdict()
        bins = {k: list(v) for k, v in bins.iteritems()}
        validate(self, bins, "efficiency_tag")

    @unittest.skip("Debug")
    def test_different_modules(self):
        datafile = DataVault().file("data", "uncorrected")
        hpatterns = ["MassEnergy%s" + "_SM{0}".format(i) for i in range(1, 5)]
        estimators = [TagAndProbe(datafile, hpattern=si).eff(False)
                      for si in hpatterns]
        for i, e in enumerate(estimators):
            e.SetTitle(
                "TOF efficiency in different modules; E, GeV; TOF efficiency")
            e.label = "SM{0}".format(i + 1)
            e.logy = 0

        canvas = adjust_canvas(gcanvas())
        diff = Comparator(crange=(0, 1))
        diff.compare(estimators)

    # Test new and old tof calibrations
    @unittest.skip("Debug")
    def test_efficiencies_different(self):
        paths = {
            "/new-calibration/LHC16": "2017",
            "/uncorrected/LHC16": "2016"
        }

        def tof(dataset):
            probe_estimator = TagAndProbe(dataset)
            return probe_estimator.eff()

        efficiencies = map(tof, paths.keys())
        for e, l in zip(efficiencies, paths.values()):
            e.label = l

        diff = Comparator(rrange=(0.5, 1.5))
        diff.compare(efficiencies)
