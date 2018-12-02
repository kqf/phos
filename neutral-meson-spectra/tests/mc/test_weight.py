import pytest

import ROOT
from spectrum.options import Options
from spectrum.analysis import Analysis
from spectrum.pipeline import ComparePipeline
from spectrum.pipeline import HistogramSelector
from spectrum.pipeline import Pipeline
from spectrum.input import SingleHistInput

from vault.datavault import DataVault

# NB: MC generated pT spectrum differs from the real one
#     this should be taken into account as it might
#     affect the efficiency


@pytest.mark.onlylocal
def test_species_contributions():
    estimator = ComparePipeline([
        ("data", Pipeline([
            ("analysis", Analysis(Options())),
            ("spectrum", HistogramSelector("spectrum")),
        ])),
        ("generated", SingleHistInput("hPt_#pi^{0}_primary_")),
    ])
    estimator.transform((
        DataVault().input("data", histname="MassPtSM0"),
        DataVault().input("pythia8"),
    ), {})


def fit_function():
    func_feeddown = ROOT.TF1(
        "func_feeddown",
        "[2] * (1.+[0]*TMath::Exp(-x/2*x/2/2./[1]/[1]))", 0, 100)
    func_feeddown.SetParNames('A', '#sigma', 'scale')
    func_feeddown.SetParameter(0, -1.063)
    func_feeddown.SetParameter(1, 0.855)
    func_feeddown.SetParameter(2, 2.0)
    return func_feeddown
