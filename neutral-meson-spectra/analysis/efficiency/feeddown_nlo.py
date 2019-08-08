import pytest
import ROOT

from spectrum.tools.feeddown import FeeddownEstimator
from vault.datavault import DataVault

from spectrum.options import FeeddownOptions
from spectrum.output import open_loggs
from spectrum.comparator import Comparator


def feeddown_paramerization():
    func_feeddown = ROOT.TF1(
        "func_feeddown",
        "[2] * (1.+[0]*TMath::Exp(-x/2*x/2/2./[1]/[1]))",
        0, 100
    )
    func_feeddown.SetParNames("A", "#sigma", "E_{scale}")
    func_feeddown.SetParameter(0, -1.4)
    func_feeddown.SetParameter(1, 0.33)
    func_feeddown.SetParLimits(1, 0, 10)
    func_feeddown.SetParameter(2, 0.02)
    return func_feeddown


@pytest.fixture
def data():
    return (
        DataVault().input(
            "pythia8",
            listname="MCStudy",
            use_mixing=False,
            histname="MassPt_#pi^{0}_primary_#omega",
        ),
        DataVault().input("pythia8", listname="FeeddownSelection"),
    )


@pytest.mark.onlylocal
@pytest.mark.interactive
def test_feeddown_correction(data):
    options = FeeddownOptions()
    options.fitf = feeddown_paramerization()
    estimator = FeeddownEstimator(options)
    with open_loggs("feeddown nlo correction") as loggs:
        output = estimator.transform(data, loggs)
        Comparator().compare(output)
    assert output.GetEntries() > 0
