import pytest

from spectrum.spectra import spectrum
from spectrum.output import open_loggs
from spectrum.pipeline import ParallelPipeline
from spectrum.input import SingleHistInput
from spectrum.comparator import Comparator
import spectrum.broot as br
from vault.datavault import DataVault
from vault.formulas import FVault


@pytest.fixture
def data():
    return (
        DataVault().input("theory", "incnlo"),
        DataVault().input("theory", "7 TeV")
    )


@pytest.mark.onlylocal
@pytest.mark.interactive
def test_simple(data):
    pion = spectrum("#pi^{0}")

    with open_loggs() as loggs:
        predictions = ParallelPipeline([
            ("mu1", SingleHistInput("#sigma_{total}")),
            ("mu2", SingleHistInput("#sigma_{total}")),
        ]).transform(data, loggs=loggs)

    histograms = [pion] + list(predictions)

    param = br.function2histogram(FVault().tf1("tcm", "#pi^{0} 13 TeV"), pion)
    ratios = [br.ratio(h, param) for h in histograms]
    labels = ["data", "NLO pQCD #mu = 1.0 p_{T}", "NLO pQCD #mu = 0.5 p_{T}"]
    for rr, label in zip(ratios, labels):
        rr.label = label
        rr.GetYaxis().SetTitle("#frac{data, predictions}{TCM fit}")
        rr.SetTitle("")

    for p in predictions:
        Comparator().compare(ratios)
